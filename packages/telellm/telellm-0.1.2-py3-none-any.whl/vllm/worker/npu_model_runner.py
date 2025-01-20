import dataclasses
# import gc
# import inspect
# import itertools
# import time
import warnings
import weakref
from dataclasses import dataclass
from typing import (TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Type,
                    TypeVar, Union)

import numpy as np
import torch
import torch.distributed
# import torch.nn as nn

import vllm.envs as envs
from vllm.config import (CacheConfig, DeviceConfig, LoadConfig, LoRAConfig,
                         ModelConfig, ObservabilityConfig, ParallelConfig,
                         PromptAdapterConfig, SchedulerConfig)
from vllm.distributed import get_pp_group
# from vllm.distributed.parallel_state import graph_capture
from vllm.inputs import INPUT_REGISTRY, InputRegistry
from vllm.logger import init_logger
from vllm.lora.layers import LoRAMapping
from vllm.lora.request import LoRARequest
from vllm.lora.worker_manager import LRUCacheWorkerLoRAManager
from vllm.model_executor import SamplingMetadata, SamplingMetadataCache
from vllm.model_executor.model_loader import get_model
from vllm.model_executor.model_loader.tensorizer import TensorizerConfig
from vllm.model_executor.models.interfaces import (supports_lora,
                                                   supports_multimodal)
from vllm.model_executor.models.utils import set_cpu_offload_max_bytes
from vllm.multimodal import (MULTIMODAL_REGISTRY, BatchedTensorInputs,
                             MultiModalInputs, MultiModalRegistry)
from vllm.prompt_adapter.layers import PromptAdapterMapping
from vllm.prompt_adapter.request import PromptAdapterRequest
from vllm.prompt_adapter.worker_manager import (
    LRUCacheWorkerPromptAdapterManager)
from vllm.sampling_params import SamplingParams
from vllm.sequence import (IntermediateTensors, SamplerOutput,
                           SequenceGroupMetadata)
from vllm.utils import (CudaMemoryProfiler, PyObjectCache, async_tensor_h2d, make_tensor_with_pad,
                        flatten_2d_lists, is_hip, is_pin_memory_available)
from vllm.worker.model_runner_base import (
    ModelRunnerBase, ModelRunnerInputBase, ModelRunnerInputBuilderBase,
    _add_attn_metadata_broadcastable_dict,
    _add_sampling_metadata_broadcastable_dict,
    _init_attn_metadata_from_tensor_dict,
    _init_sampling_metadata_from_tensor_dict)

if TYPE_CHECKING:
    from vllm.attention.backends.abstract import AttentionBackend

from atb_llm.utils.cpu_binding import NpuHbmInfo
# from atb_llm.runner import ModelRunner as atb_model
from atb_llm.runner.model_runner import ModelRunner as atb_model

import math
from vllm.model_executor.layers.sampler import Sampler

logger = init_logger(__name__)

LORA_WARMUP_RANK = 8
_BATCH_SIZE_ALIGNMENT = 8
# Capture graphs for token size 1, 2, 4, 8, 16, 24, 32, 40, ..., 256.
# NOTE: _get_graph_batch_size needs to be updated if this list is changed.
_BATCH_SIZES_TO_CAPTURE = [1, 2, 4] + [
    _BATCH_SIZE_ALIGNMENT * i for i in range(1, 33)
]
_NUM_WARMUP_ITERS = 2

TModelInputForNPU = TypeVar('TModelInputForNPU', bound="ModelInputForNPU")


@dataclass(frozen=True)
class ModelInputForNPU(ModelRunnerInputBase):
    """
    This base class contains metadata needed for the base model forward pass
    but not metadata for possible additional steps, e.g., sampling. Model
    runners that run additional steps should subclass this method to add
    additional fields.
    """
    input_tokens: Optional[torch.Tensor] = None
    input_positions: Optional[torch.Tensor] = None
    input_block_tables: Optional[torch.Tensor] = None
    input_slot_tables: Optional[torch.Tensor] = None
    input_seq_lens: Optional[torch.Tensor] = None
    input_lm_head_indices: Optional[torch.Tensor] = None
    seq_lens: Optional[List[int]] = None
    query_lens: Optional[List[int]] = None
    lora_mapping: Optional["LoRAMapping"] = None
    lora_requests: Optional[Set[LoRARequest]] = None
    is_prompt: Optional[bool] = None
    prompt_adapter_mapping: Optional[PromptAdapterMapping] = None
    prompt_adapter_requests: Optional[Set[PromptAdapterRequest]] = None
    multi_modal_kwargs: Optional[BatchedTensorInputs] = None
    request_ids_to_seq_ids: Optional[Dict[str, List[int]]] = None
    finished_requests_ids: Optional[List[str]] = None
    virtual_engine: int = 0

    def as_broadcastable_tensor_dict(self) -> Dict[str, Any]:
        tensor_dict = {
            "input_tokens": self.input_tokens,
            "input_positions": self.input_positions,
            "input_block_tables": self.input_block_tables,
            "input_slot_tables": self.input_slot_tables,
            "input_seq_lens": self.input_seq_lens,
            "input_lm_head_indices": self.input_lm_head_indices,
            "query_lens":self.query_lens,
            "is_prompt":self.is_prompt
        }
        _add_attn_metadata_broadcastable_dict(tensor_dict, None)
        return tensor_dict

    @classmethod
    def from_broadcasted_tensor_dict(
        cls: Type[TModelInputForNPU],
        tensor_dict: Dict[str, Any],
        attn_backend: Optional["AttentionBackend"] = None,
    ) -> TModelInputForNPU:
        if attn_backend is not None:
            tensor_dict = _init_attn_metadata_from_tensor_dict(
                attn_backend, tensor_dict)
        return cls(**tensor_dict)


@dataclass(frozen=True)
class ModelInputForNPUWithSamplingMetadata(ModelInputForNPU):
    """
    Used by the ModelRunner.
    """
    sampling_metadata: Optional["SamplingMetadata"] = None
    # Used for speculative decoding. We do not broadcast it because it is only
    # used by the driver worker.
    # is_prompt: Optional[bool] = None

    def as_broadcastable_tensor_dict(self) -> Dict[str, Any]:
        tensor_dict = {
            "input_tokens": self.input_tokens,
            "input_positions": self.input_positions,
            "input_block_tables": self.input_block_tables,
            "input_slot_tables": self.input_slot_tables,
            "input_seq_lens": self.input_seq_lens,
            "input_lm_head_indices": self.input_lm_head_indices,
            "query_lens":self.query_lens,
            "is_prompt":self.is_prompt
        }
        _add_attn_metadata_broadcastable_dict(tensor_dict, None)
        _add_sampling_metadata_broadcastable_dict(tensor_dict,
                                                  self.sampling_metadata)
        return tensor_dict

    @classmethod
    def from_broadcasted_tensor_dict(
        cls,
        tensor_dict: Dict[str, Any],
        attn_backend: Optional["AttentionBackend"] = None,
    ) -> "ModelInputForNPUWithSamplingMetadata":
        tensor_dict = _init_sampling_metadata_from_tensor_dict(tensor_dict)
        if attn_backend is not None:
            tensor_dict = _init_attn_metadata_from_tensor_dict(
                attn_backend, tensor_dict)
        return cls(**tensor_dict)


class ModelInputForNPUBuilder(ModelRunnerInputBuilderBase[ModelInputForNPU]):
    """Build ModelInputForGPU from SequenceGroupMetadata."""

    # Note: ideally we would be using a dataclass(kw_only=True)
    # here, so that this can be subclassed easily,
    # but kw_only is not supported in python<3.10.
    class InterDataForSeqGroup:
        """Intermediate data for the current sequence group."""

        def simple_reinit(self):
            self.input_tokens[0].clear()  # type: ignore
            self.input_positions[0].clear()  # type: ignore
            self.seq_lens[0] = 0  # type: ignore
            self.orig_seq_lens[0] = 0  # type: ignore
            self.query_lens[0] = 0  # type: ignore
            self.context_lens[0] = 0  # type: ignore
            self.curr_sliding_window_blocks[0] = 0  # type: ignore
            self.lora_index_mapping.clear()  # type: ignore
            self.lora_prompt_mapping.clear()  # type: ignore
            self.lora_requests.clear()  # type: ignore
            self.prompt_adapter_index_mapping.clear()  # type: ignore
            self.prompt_adapter_prompt_mapping.clear()  # type: ignore

        def __init__(
            self,
            *,
            # From sequence group metadata.
            request_id: str,
            seq_ids: List[int],
            is_prompt: bool,
            block_tables: Optional[Dict[int, List[int]]],
            computed_block_nums: List[int],
            n_seqs: int = 0,

            # Input tokens and positions.
            input_tokens: Optional[List[List[int]]] = None,
            input_positions: Optional[List[List[int]]] = None,

            # The sequence length (may be capped to the sliding window).
            seq_lens: Optional[List[int]] = None,
            # The original sequence length (before applying sliding window).
            # This is used to compute slot mapping.
            orig_seq_lens: Optional[List[int]] = None,
            # The query length.
            query_lens: Optional[List[int]] = None,
            # The number of tokens that are already computed.
            context_lens: Optional[List[int]] = None,
            # The current sliding window block.
            curr_sliding_window_blocks: Optional[List[int]] = None,

            # LoRA inputs.
            lora_index_mapping: Optional[List[List[int]]] = None,
            lora_prompt_mapping: Optional[List[List[int]]] = None,
            lora_requests: Optional[Set[LoRARequest]] = None,

            # Prompt adapter inputs.
            prompt_adapter_index_mapping: Optional[List[int]] = None,
            prompt_adapter_prompt_mapping: Optional[List[int]] = None,
            prompt_adapter_request: Optional[PromptAdapterRequest] = None,

            # Multi-modal inputs.
            multi_modal_inputs: Optional[MultiModalInputs] = None,

            # Whether the prefix cache is hit (prefill only).
            prefix_cache_hit: bool = False,
            reinit: bool = False,
            reinit_use_defaults: bool = False,
        ):
            if reinit:
                assert len(self.seq_ids) == len(seq_ids)  # type: ignore
                for i, seq_id in enumerate(seq_ids):
                    self.seq_ids[i] = seq_id  # type: ignore
            else:
                self.seq_ids = seq_ids

            self.request_id = request_id
            self.is_prompt = is_prompt
            self.block_tables = block_tables
            self.computed_block_nums = computed_block_nums
            self.n_seqs = n_seqs

            if reinit:
                if len(self.seq_ids) == 1 and reinit_use_defaults:
                    self.simple_reinit()
                else:
                    if input_tokens:
                        self.input_tokens = input_tokens
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.input_tokens[seq_id].clear()

                    if input_positions:
                        self.input_positions = input_positions
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.input_positions[seq_id].clear()

                    if seq_lens:
                        self.seq_lens = seq_lens
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.seq_lens[seq_id] = 0

                    if orig_seq_lens:
                        self.orig_seq_lens = orig_seq_lens
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.orig_seq_lens[seq_id] = 0

                    if query_lens:
                        self.query_lens = query_lens
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.query_lens[seq_id] = 0

                    if context_lens:
                        self.context_lens = context_lens
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.context_lens[seq_id] = 0

                    if curr_sliding_window_blocks:
                        self.curr_sliding_window_blocks = \
                            curr_sliding_window_blocks
                    else:
                        for seq_id in range(len(self.seq_ids)):
                            self.curr_sliding_window_blocks[seq_id] = 0

                    if lora_index_mapping:
                        self.lora_index_mapping = lora_index_mapping
                    else:
                        self.lora_index_mapping.clear()

                    if lora_prompt_mapping:
                        self.lora_prompt_mapping = lora_prompt_mapping
                    else:
                        self.lora_prompt_mapping.clear()

                    if lora_requests:
                        self.lora_requests = lora_requests
                    else:
                        self.lora_requests.clear()

                    if prompt_adapter_index_mapping:
                        self.prompt_adapter_index_mapping = \
                            prompt_adapter_index_mapping
                    else:
                        self.prompt_adapter_index_mapping.clear()

                    if prompt_adapter_prompt_mapping:
                        self.prompt_adapter_prompt_mapping = \
                            prompt_adapter_prompt_mapping
                    else:
                        self.prompt_adapter_prompt_mapping.clear()

            else:
                self.input_tokens = input_tokens or []
                self.input_positions = input_positions or []
                self.seq_lens = seq_lens or []
                self.orig_seq_lens = orig_seq_lens or []
                self.query_lens = query_lens or []
                self.context_lens = context_lens or []
                self.curr_sliding_window_blocks = \
                    curr_sliding_window_blocks or []

                self.lora_index_mapping = lora_index_mapping or []
                self.lora_prompt_mapping = lora_prompt_mapping or []
                self.lora_requests = lora_requests or set()

                self.prompt_adapter_index_mapping = (
                    prompt_adapter_index_mapping or [])
                self.prompt_adapter_prompt_mapping = (
                    prompt_adapter_prompt_mapping or [])

            self.prompt_adapter_request = prompt_adapter_request
            self.multi_modal_inputs = multi_modal_inputs
            self.prefix_cache_hit = prefix_cache_hit

            self.n_seqs = len(self.seq_ids)

            if not reinit:
                self.__post_init__()

        def __post_init__(self):
            self.n_seqs = len(self.seq_ids)

            self.input_tokens = [[] for _ in range(self.n_seqs)]
            self.input_positions = [[] for _ in range(self.n_seqs)]
            self.seq_lens = [0] * self.n_seqs
            self.orig_seq_lens = [0] * self.n_seqs
            self.query_lens = [0] * self.n_seqs
            self.context_lens = [0] * self.n_seqs
            self.curr_sliding_window_blocks = [0] * self.n_seqs

            self.lora_index_mapping = []
            self.lora_prompt_mapping = []

    def gen_inter_data_builder(self, num_seqs: int):
        return lambda: ModelInputForNPUBuilder.InterDataForSeqGroup(
            request_id="",
            seq_ids=[0] * num_seqs,
            is_prompt=True,
            block_tables=None,
            computed_block_nums=[])

    def init_cached_inter_data(self, *args, **kwargs):
        assert len(args) == 0
        assert "seq_ids" in kwargs
        seq_ids = kwargs["seq_ids"]
        num_seqs = len(seq_ids)

        # The inter-data cache is per model_runner
        inter_data_cache = self.runner.inter_data_cache
        if num_seqs not in inter_data_cache: #
            inter_data_cache[num_seqs] = PyObjectCache(
                self.gen_inter_data_builder(num_seqs)) #

        obj = inter_data_cache[num_seqs].get_object() #
        obj.__init__(*args, **kwargs)
        return obj #

    def reset_cached_inter_data(self):
        for cache in self.runner.inter_data_cache.values():
            cache.reset()

    def __init__(self,
                 runner: "NPUModelRunnerBase",
                 finished_requests_ids: Optional[List[str]] = None):
        super().__init__()
        # Compute functions for each sequence in a sequence group.
        # WARNING: The order of the functions matters!
        self.per_seq_compute_fns = [
            self._compute_lens,
            self._compute_for_prefix_cache_hit,
            self._compute_for_sliding_window,
            self._compute_lora_input,
        ]
        # Compute functions for each sequence group.
        # WARNING: The order of the functions matters!
        self.per_seq_group_compute_fns = [
            self._compute_prompt_adapter_input,
            self._compute_multi_modal_input,
        ]

        self.runner = runner
        self.model_input_cls = self.runner._model_input_cls
        self.scheduler_config = self.runner.scheduler_config
        self.sliding_window = self.runner.sliding_window
        self.block_size = self.runner.block_size
        self.enable_lora = self.runner.lora_config is not None
        self.enable_prompt_adapter = (self.runner.prompt_adapter_config
                                      is not None)
        self.multi_modal_input_mapper = self.runner.multi_modal_input_mapper
        self.finished_requests_ids = finished_requests_ids
        self.decode_only = True

        # Intermediate data (data in CPU before going to GPU) for
        # the current sequence group.
        self.inter_data_list: List[
            ModelInputForNPUBuilder.InterDataForSeqGroup] = []

        # Engine/Model configurations.
        self.chunked_prefill_enabled = (
            self.scheduler_config is not None
            and self.scheduler_config.chunked_prefill_enabled)
        if self.sliding_window is not None:
            self.sliding_window_blocks = (
                self.sliding_window + self.block_size - 1) // self.block_size
            self.block_aligned_sliding_window = \
                self.sliding_window_blocks * self.block_size

    def _compute_lens(self, inter_data: InterDataForSeqGroup, seq_idx: int,
                      seq_group_metadata: SequenceGroupMetadata):
        """Compute context length, sequence length and tokens
        for the given sequence data.
        """
        seq_data = seq_group_metadata.seq_data[inter_data.seq_ids[seq_idx]]
        token_chunk_size = seq_group_metadata.token_chunk_size

        # Compute context length (the number of tokens that are
        # already computed) and sequence length (total number of tokens).
        seq_len = seq_data.get_len()
        if inter_data.is_prompt:
            context_len = seq_data.get_num_computed_tokens()
        else:
            # get_num_computed_tokens is incorrect for spec decoding.
            # So, we should have a special logic here.
            # TODO(sang): Fix it.
            context_len = seq_len - 1
        seq_len = min(seq_len, context_len + token_chunk_size)

        # Compute tokens.
        if inter_data.is_prompt:
            tokens = seq_data.get_token_ids()
            if context_len != 0 or seq_len < len(tokens):
                tokens = tokens[context_len:seq_len]
        else:
            # Optimization. get_token_ids requires the entire copy of
            # tokens.
            tokens = seq_data.get_last_token_id()

        inter_data.seq_lens[seq_idx] = seq_len
        inter_data.orig_seq_lens[seq_idx] = seq_len
        inter_data.context_lens[seq_idx] = context_len

        if isinstance(tokens, list):
            inter_data.input_tokens[seq_idx].extend(tokens)
        else:
            inter_data.input_tokens[seq_idx].append(tokens)

        if (seq_len - context_len) == 1:
            inter_data.input_positions[seq_idx].append(seq_len - 1)
        else:
            inter_data.input_positions[seq_idx].extend(
                range(context_len, seq_len))

        inter_data.query_lens[
            seq_idx] = seq_len - context_len if inter_data.is_prompt else 1

    def _compute_for_prefix_cache_hit(
            self, inter_data: InterDataForSeqGroup, seq_idx: int,
            seq_group_metadata: SequenceGroupMetadata):
        """Check if hit prefix cache (i.e., some blocks are already computed).
        If hit, update input tokens and positions to only compute the
        remaining blocks.
        """
        computed_block_nums = inter_data.computed_block_nums

        # Note that prefix caching does not support sliding window.
        prefix_cache_hit = (computed_block_nums is not None
                            and len(computed_block_nums) > 0
                            and self.sliding_window is None
                            and inter_data.is_prompt)
        inter_data.prefix_cache_hit = prefix_cache_hit
        if self.chunked_prefill_enabled and prefix_cache_hit:
            raise RuntimeError(
                "chunked prefill cannot be used with prefix caching now.")

        # If prefix cache is hit, advance context length to bypass
        # hit blocks. Accordingly, input tokens, position and query length
        # have to be updated.
        if prefix_cache_hit:
            assert computed_block_nums is not None
            context_len = len(computed_block_nums) * self.block_size
            inter_data.input_tokens[seq_idx] = inter_data.input_tokens[
                seq_idx][context_len:]
            inter_data.input_positions[seq_idx] = inter_data.input_positions[
                seq_idx][context_len:]
            inter_data.context_lens[seq_idx] = context_len
            inter_data.query_lens[
                seq_idx] = inter_data.seq_lens[seq_idx] - context_len

    def _compute_for_sliding_window(self, inter_data: InterDataForSeqGroup,
                                    seq_idx: int,
                                    seq_group_metadata: SequenceGroupMetadata):
        """Update seq_len and curr_sliding_window_block for the given
        sequence data (only required by decoding) if sliding window is enabled.
        """
        curr_sliding_window_block = 0
        sliding_seq_len = inter_data.seq_lens[seq_idx]
        if not inter_data.is_prompt and self.sliding_window is not None:
            # TODO(sang): This is a hack to make sliding window work with
            # paged attn. We can remove it if we make paged attn kernel
            # to properly handle slinding window attn.
            curr_sliding_window_block = self.sliding_window_blocks
            if self.scheduler_config.use_v2_block_manager:
                # number of elements in last block
                suff_len = inter_data.seq_lens[seq_idx] % self.block_size
                sliding_seq_len = min(
                    inter_data.seq_lens[seq_idx],
                    self.block_aligned_sliding_window + suff_len)
                if suff_len > 0:
                    curr_sliding_window_block += 1
            else:
                sliding_seq_len = min(inter_data.seq_lens[seq_idx],
                                      self.sliding_window)

        inter_data.curr_sliding_window_blocks[
            seq_idx] = curr_sliding_window_block
        inter_data.seq_lens[seq_idx] = sliding_seq_len

    def _compute_lora_input(self, inter_data: InterDataForSeqGroup,
                            seq_idx: int,
                            seq_group_metadata: SequenceGroupMetadata):
        """If LoRA is enabled, compute LoRA index and prompt mapping."""
        if not self.enable_lora:
            return

        lora_id = seq_group_metadata.lora_int_id
        if lora_id > 0:
            inter_data.lora_requests.add(seq_group_metadata.lora_request)
        query_len = inter_data.query_lens[seq_idx]
        inter_data.lora_index_mapping.append([lora_id] * query_len)
        inter_data.lora_prompt_mapping.append(
            [lora_id] *
            (query_len if seq_group_metadata.sampling_params
             and seq_group_metadata.sampling_params.prompt_logprobs is not None
             else 1))

    def _compute_prompt_adapter_input(
            self, inter_data: InterDataForSeqGroup,
            seq_group_metadata: SequenceGroupMetadata):
        """If prompt adapter is enabled, compute index and prompt mapping.
        """
        # Note that when is_prompt=True, we expect only one sequence
        # in the group.
        if not self.enable_prompt_adapter:
            return

        prompt_adapter_id = seq_group_metadata.prompt_adapter_id
        if prompt_adapter_id <= 0 or not inter_data.is_prompt:
            return

        # We expect only one sequence in the group when is_prompt=True.
        assert inter_data.n_seqs == 1
        query_len = inter_data.query_lens[0]
        inter_data.prompt_adapter_request = (
            seq_group_metadata.prompt_adapter_request)

        num_tokens = seq_group_metadata.prompt_adapter_num_virtual_tokens
        inter_data.prompt_adapter_index_mapping = [
            prompt_adapter_id
        ] * num_tokens + [0] * (query_len - num_tokens)
        inter_data.prompt_adapter_prompt_mapping = [prompt_adapter_id] * (
            query_len if seq_group_metadata.sampling_params
            and seq_group_metadata.sampling_params.prompt_logprobs else 1)

    def _compute_multi_modal_input(self, inter_data: InterDataForSeqGroup,
                                   seq_group_metadata: SequenceGroupMetadata):
        """If multi-modal data is given, add it to the input."""
        mm_data = seq_group_metadata.multi_modal_data
        if not mm_data:
            return

        mm_kwargs = self.multi_modal_input_mapper(mm_data)
        inter_data.multi_modal_inputs = mm_kwargs

    def add_seq_group(self, seq_group_metadata: SequenceGroupMetadata):
        """Add a sequence group to the builder."""
        seq_ids = seq_group_metadata.seq_data.keys()
        n_seqs = len(seq_ids) #
        is_prompt = seq_group_metadata.is_prompt

        if is_prompt:
            assert n_seqs == 1
            self.decode_only = False

        inter_data = self.init_cached_inter_data(
            request_id=seq_group_metadata.request_id,
            seq_ids=seq_ids,
            is_prompt=is_prompt,
            block_tables=seq_group_metadata.block_tables,
            computed_block_nums=seq_group_metadata.computed_block_nums,
            reinit=True,
            reinit_use_defaults=True)

        self.inter_data_list.append(inter_data) #

        #
        for seq_idx in range(n_seqs):
            for per_seq_fn in self.per_seq_compute_fns:
                per_seq_fn(inter_data, seq_idx, seq_group_metadata)
        for per_seq_group_fn in self.per_seq_group_compute_fns:
            per_seq_group_fn(inter_data, seq_group_metadata)

    def _use_captured_graph(self, batch_size: int,
                            max_decode_seq_len: int) -> bool:
        return (self.decode_only and not self.runner.model_config.enforce_eager
                and batch_size <= _BATCH_SIZES_TO_CAPTURE[-1]
                and max_decode_seq_len <= self.runner.max_seq_len_to_capture)

    def build(self) -> ModelInputForNPU: 
        """Finalize the builder intermediate data and
        create on-device tensors.
        """
        # Combine and flatten intermediate data.
        input_tokens = []
        for inter_data in self.inter_data_list:
            for cur_input_tokens in inter_data.input_tokens:
                input_tokens.extend(cur_input_tokens) #

        if not input_tokens:
            # This may happen when all prefill requests hit
            # prefix caching and there is no decode request.
            return self.model_input_cls()

        input_positions = []
        for inter_data in self.inter_data_list:
            for cur_input_positions in inter_data.input_positions:
                input_positions.extend(cur_input_positions)
                
        # npu
        input_block_tables: List[List[int]] = []
        input_slot_tables: List[torch.Tensor] = []
        input_slot_indices: List[torch.Tensor] = []
        slot_offset = 0
        for inter_data in self.inter_data_list:
            for i in range(inter_data.n_seqs):
                # input_slot_indices
                cur_input_positions = inter_data.input_positions[i]
                cur_input_positions_tensor = torch.tensor(cur_input_positions, dtype=torch.long, device="cpu")
                cur_input_positions_tensor += slot_offset
                input_slot_indices.append(cur_input_positions_tensor)
                # input_block_table
                seq_id = inter_data.seq_ids[i]
                input_block_table = inter_data.block_tables[seq_id]
                input_block_tables.append(input_block_table)
                # input_slot_tables
                if(self.runner.total_slots is None):
                    slot_table = torch.arange(len(input_block_table)*self.block_size, dtype=torch.long) + slot_offset
                    input_slot_tables.append(slot_table)
                else:
                    slot_table = self.runner.total_slots[torch.tensor(input_block_table)].flatten() #
                    input_slot_tables.append(slot_table)
                slot_offset += len(input_block_table)*self.block_size
                
        seq_lens = []
        max_decode_seq_len = 0
        for inter_data in self.inter_data_list:
            seq_lens.extend(inter_data.seq_lens)
            if not inter_data.is_prompt:
                max_decode_seq_len = max(max_decode_seq_len,
                                         max(inter_data.seq_lens))
        query_lens = []
        for inter_data in self.inter_data_list:
            query_lens.extend(inter_data.query_lens)

        # Mapping from request IDs to sequence IDs. Used for Jamba models
        # that manages the cache by itself.
        request_ids_to_seq_ids = {
            data.request_id: data.seq_ids
            for data in self.inter_data_list
        }

        batch_size = len(input_tokens)
        
        assert self.runner.device is not None
        input_tokens_tensor = async_tensor_h2d(input_tokens, torch.long,
                                               self.runner.device,
                                               self.runner.pin_memory)
        input_positions_tensor = async_tensor_h2d(input_positions, torch.long,
                                                  self.runner.device,
                                                  self.runner.pin_memory)
        max_len_block_table = max(len(block_table) for block_table in input_block_tables)
        input_block_tables_tensor = make_tensor_with_pad(input_block_tables, 0, torch.long,
                                                         max_len=max_len_block_table,
                                                         device=self.runner.device)
        input_slot_indices_tensor = torch.concat(input_slot_indices, dim=0)
        input_slot_tables_tensor = torch.concat(input_slot_tables, 
                                                dim=0)[input_slot_indices_tensor].to(device=self.runner.device, 
                                                                                     non_blocking=True)
        input_seq_lens_tensor = async_tensor_h2d(seq_lens, torch.long,
                                               self.runner.device,
                                               self.runner.pin_memory)
        input_lm_head_indices_tensor = torch.cumsum(input_seq_lens_tensor, dim=0) - 1

        # LoRA data.
        lora_requests = set()
        lora_mapping = None
        if self.enable_lora:
            lora_requests = set(r for data in self.inter_data_list
                                for r in data.lora_requests)
            lora_index_mapping = flatten_2d_lists([
                flatten_2d_lists(inter_data.lora_index_mapping)
                for inter_data in self.inter_data_list
            ])
            lora_prompt_mapping = flatten_2d_lists([
                flatten_2d_lists(inter_data.lora_prompt_mapping)
                for inter_data in self.inter_data_list
            ])

            lora_mapping = LoRAMapping(
                **dict(index_mapping=lora_index_mapping,
                       prompt_mapping=lora_prompt_mapping,
                       is_prefill=not self.decode_only))

        # Prompt adapter data.
        prompt_adapter_requests: Set[PromptAdapterRequest] = set()
        prompt_adapter_mapping = None
        if self.enable_prompt_adapter:
            prompt_adapter_requests = set(
                data.prompt_adapter_request for data in self.inter_data_list
                if data.prompt_adapter_request is not None)
            prompt_adapter_index_mapping = flatten_2d_lists([
                inter_data.prompt_adapter_index_mapping
                for inter_data in self.inter_data_list
            ])
            prompt_adapter_prompt_mapping = flatten_2d_lists([
                inter_data.prompt_adapter_prompt_mapping
                for inter_data in self.inter_data_list
            ])
            prompt_adapter_mapping = PromptAdapterMapping(
                prompt_adapter_index_mapping,
                prompt_adapter_prompt_mapping,
            )

        # Multi-modal data.
        multi_modal_inputs_list = [
            data.multi_modal_inputs for data in self.inter_data_list
            if data.multi_modal_inputs is not None
        ]
        multi_modal_kwargs = MultiModalInputs.batch(multi_modal_inputs_list)

        return self.model_input_cls(
            input_tokens=input_tokens_tensor,
            input_positions=input_positions_tensor,
            input_block_tables=input_block_tables_tensor, # 
            input_slot_tables=input_slot_tables_tensor, #
            input_seq_lens=input_seq_lens_tensor,
            input_lm_head_indices=input_lm_head_indices_tensor,
            seq_lens=seq_lens, 
            query_lens=query_lens,
            is_prompt=inter_data.is_prompt
        )


class NPUModelRunnerBase(ModelRunnerBase[TModelInputForNPU]):
    """
    Helper class for shared methods between GPU model runners.
    """
    _model_input_cls: Type[TModelInputForNPU]
    _builder_cls: Type[ModelInputForNPUBuilder]

    def __init__(
        self,
        model_config: ModelConfig,
        parallel_config: ParallelConfig,
        scheduler_config: SchedulerConfig,
        device_config: DeviceConfig,
        cache_config: CacheConfig,
        load_config: LoadConfig,
        lora_config: Optional[LoRAConfig],
        local_rank: int,
        rank: int,
        kv_cache_dtype: Optional[str] = "auto",
        is_driver_worker: bool = False,
        prompt_adapter_config: Optional[PromptAdapterConfig] = None,
        return_hidden_states: bool = False,
        observability_config: Optional[ObservabilityConfig] = None,
        input_registry: InputRegistry = INPUT_REGISTRY,
        mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY,
    ):
        self.model_config = model_config
        self.parallel_config = parallel_config
        self.scheduler_config = scheduler_config
        self.device_config = device_config
        self.cache_config = cache_config
        self.lora_config = lora_config
        self.load_config = load_config
        self.local_rank = local_rank
        self.rank = rank
        self.is_driver_worker = is_driver_worker
        self.prompt_adapter_config = prompt_adapter_config
        self.return_hidden_states = return_hidden_states
        self.observability_config = observability_config

        # self.device = self.device_config.device
        self.pin_memory = is_pin_memory_available()

        self.kv_cache_dtype = kv_cache_dtype
        self.sliding_window = model_config.get_sliding_window()
        self.block_size = cache_config.block_size
        self.max_seq_len_to_capture = self.model_config.max_seq_len_to_capture

        self.graph_memory_pool: Optional[Tuple[
            int, int]] = None  # Set during graph capture.

        self.has_seqlen_agnostic = model_config.contains_seqlen_agnostic_layers(
            parallel_config)

        # When using CUDA graph, the input block tables must be padded to
        # max_seq_len_to_capture. However, creating the block table in
        # Python can be expensive. To optimize this, we cache the block table
        # in numpy and only copy the actual input content at every iteration.
        # The shape of the cached block table will be
        # (max batch size to capture, max context len to capture / block size).
        self.graph_block_tables = np.zeros(
            (max(_BATCH_SIZES_TO_CAPTURE), self.get_max_block_per_batch()),
            dtype=np.int32)
        num_attn_heads = self.model_config.get_num_attention_heads(
            self.parallel_config)

        # Multi-modal data support
        self.input_registry = input_registry
        self.mm_registry = mm_registry
        self.multi_modal_input_mapper = mm_registry \
            .create_input_mapper(model_config)
        self.mm_registry.init_mm_limits_per_prompt(self.model_config)

        # Lazy initialization
        #
        self.model = atb_model(
            model_config.model, rank=rank, world_size=parallel_config.world_size,
            local_rank=local_rank,
            max_position_embeddings=None
        )
        self.device = self.model.device
        self.sampler = Sampler()
        
        # Set after load_model.
        self.lora_manager: Optional[LRUCacheWorkerLoRAManager] = None
        self.prompt_adapter_manager: LRUCacheWorkerPromptAdapterManager = None

        set_cpu_offload_max_bytes(
            int(self.cache_config.cpu_offload_gb * 1024**3))

        # Used to cache python objects
        self.inter_data_cache: Dict[int, PyObjectCache] = {}
        self.sampling_metadata_cache: SamplingMetadataCache = \
            SamplingMetadataCache()
            
        # Set after initial profiling.
        self.total_slots = None 

    def load_model(self) -> None:
        logger.info("Starting to load model %s...", self.model_config.model)
        self.model.load_weights()
        # load_weights以后才有soc_info
        self.max_memory = NpuHbmInfo.get_hbm_capacity(self.local_rank, self.parallel_config.world_size, self.model.soc_info.need_nz)
        self.model_memory_usage = int(
            self.max_memory * NpuHbmInfo.get_hbm_usage(self.local_rank, self.parallel_config.world_size, self.model.soc_info.need_nz))
        logger.info("Loading model weights took %.4f GB",
                    self.model_memory_usage / float(2**30))

        if self.lora_config:
            assert supports_lora(self.model), "Model does not support LoRA"
            assert not supports_multimodal(
                self.model
            ), "To be tested: Multi-modal model with LoRA settings."

            self.lora_manager = LRUCacheWorkerLoRAManager(
                self.scheduler_config.max_num_seqs,
                self.scheduler_config.max_num_batched_tokens,
                self.vocab_size,
                self.lora_config,
                self.device,
                self.model.embedding_modules,
                self.model.embedding_padding_modules,
                max_position_embeddings=self.model.config.
                max_position_embeddings,
            )
            self.model = self.lora_manager.create_lora_manager(self.model)

        if self.prompt_adapter_config:
            self.prompt_adapter_manager = LRUCacheWorkerPromptAdapterManager(
                self.scheduler_config.max_num_seqs,
                self.scheduler_config.max_num_batched_tokens, self.device,
                self.prompt_adapter_config)
            self.model = (
                self.prompt_adapter_manager.create_prompt_adapter_manager(
                    self.model))

        if self.kv_cache_dtype == "fp8" and is_hip():
            # Currently only ROCm accepts kv-cache scaling factors
            # via quantization_param_path and this will be deprecated
            # in the future.
            if self.model_config.quantization_param_path is not None:
                if callable(getattr(self.model, "load_kv_cache_scales", None)):
                    warnings.warn(
                        "Loading kv cache scaling factor from JSON is "
                        "deprecated and will be removed. Please include "
                        "kv cache scaling factors in the model checkpoint.",
                        FutureWarning,
                        stacklevel=2)
                    self.model.load_kv_cache_scales(
                        self.model_config.quantization_param_path)
                    logger.info("Loaded KV cache scaling factors from %s",
                                self.model_config.quantization_param_path)
                else:
                    raise RuntimeError(
                        "Using FP8 KV cache and scaling factors provided but "
                        "model %s does not support loading scaling factors.",
                        self.model.__class__)
            else:
                logger.warning(
                    "Using FP8 KV cache but no scaling factors "
                    "provided. Defaulting to scaling factors of 1.0. "
                    "This may lead to less accurate results!")

        if envs.VLLM_TEST_DYNAMO_GRAPH_CAPTURE:
            self.model = torch.compile(self.model,
                                       fullgraph=True,
                                       backend="eager")

    def save_sharded_state(
        self,
        path: str,
        pattern: Optional[str] = None,
        max_size: Optional[int] = None,
    ) -> None:
        from vllm.model_executor.model_loader.loader import ShardedStateLoader
        ShardedStateLoader.save_model(
            self.model,
            path,
            pattern=pattern,
            max_size=max_size,
        )

    def save_tensorized_model(
        self,
        tensorizer_config: TensorizerConfig,
    ) -> None:
        from vllm.model_executor.model_loader.loader import TensorizerLoader
        TensorizerLoader.save_model(
            self.model,
            tensorizer_config=tensorizer_config,
        )

    def get_max_block_per_batch(self) -> int:
        block_size = self.block_size
        return (self.max_seq_len_to_capture + block_size - 1) // block_size

    def _prepare_model_input_tensors(
        self,
        seq_group_metadata_list: List[SequenceGroupMetadata],
        finished_requests_ids: Optional[List[str]] = None
    ) -> TModelInputForNPU:
        """Helper method to prepare the model input based on a given sequence
        group. Prepares metadata needed for the base model forward pass but not
        metadata for possible additional steps, e.g., sampling.

        The API assumes seq_group_metadata_list is sorted by prefill -> decode.

        The result tensors and data structure also batches input in prefill
        -> decode order. For example,

        - input_tokens[:num_prefill_tokens] contains prefill tokens.
        - input_tokens[num_prefill_tokens:] contains decode tokens.

        If cuda graph is required, this API automatically pads inputs.
        """
        #
        builder = self._builder_cls(weakref.proxy(self), finished_requests_ids)
        for seq_group_metadata in seq_group_metadata_list:
            builder.add_seq_group(seq_group_metadata)

        builder.reset_cached_inter_data()

        return builder.build()  # type: ignore

    @torch.inference_mode()
    def profile_run(self) -> None:
        # Enable top-k sampling to reflect the accurate memory usage.
        sampling_params = SamplingParams(top_p=0.99, top_k=self.vocab_size - 1)
        max_num_batched_tokens = self.scheduler_config.max_num_batched_tokens
        max_num_seqs = self.scheduler_config.max_num_seqs
        # This represents the maximum number of different requests
        # that will have unique loras, an therefore the max amount of memory
        # consumption create dummy lora request copies from the lora request
        # passed in, which contains a lora from the lora warmup path.
        dummy_lora_requests: List[LoRARequest] = []
        dummy_lora_requests_per_seq: List[LoRARequest] = []
        if self.lora_config:
            assert self.lora_manager is not None
            with self.lora_manager.dummy_lora_cache():
                for idx in range(self.lora_config.max_loras):
                    lora_id = idx + 1
                    dummy_lora_request = LoRARequest(
                        lora_name=f"warmup_{lora_id}",
                        lora_int_id=lora_id,
                        lora_path="/not/a/real/path",
                    )
                    self.lora_manager.add_dummy_lora(dummy_lora_request,
                                                     rank=LORA_WARMUP_RANK)
                    dummy_lora_requests.append(dummy_lora_request)
                dummy_lora_requests_per_seq = [
                    dummy_lora_requests[idx % len(dummy_lora_requests)]
                    for idx in range(max_num_seqs)
                ]

        # Profile memory usage with max_num_sequences sequences and the total
        # number of tokens equal to max_num_batched_tokens.
        seqs: List[SequenceGroupMetadata] = []
        # Additional GPU memory may be needed for multi-modal encoding, which
        # needs to be accounted for when calculating the GPU blocks for
        # vLLM blocker manager.
        # To exercise the worst scenario for GPU memory consumption,
        # the number of seqs (batch_size) is chosen to maximize the number
        # of images processed.

        max_mm_tokens = self.mm_registry.get_max_multimodal_tokens(
            self.model_config)
        if max_mm_tokens > 0:
            max_num_seqs_orig = max_num_seqs
            max_num_seqs = min(max_num_seqs,
                               max_num_batched_tokens // max_mm_tokens)
            if max_num_seqs < 1:
                expr = (f"min({max_num_seqs_orig}, "
                        f"{max_num_batched_tokens} // {max_mm_tokens})")
                logger.warning(
                    "Computed max_num_seqs (%s) to be less than 1. "
                    "Setting it to the minimum value of 1.", expr)
                max_num_seqs = 1

        batch_size = 0
        block_index = 0
        for group_id in range(max_num_seqs):
            seq_len = (max_num_batched_tokens // max_num_seqs +
                       (group_id < max_num_batched_tokens % max_num_seqs))
            batch_size += seq_len

            seq_data, dummy_multi_modal_data = self.input_registry \
                .dummy_data_for_profiling(self.model_config,
                                          seq_len,
                                          self.mm_registry)
            block_tables = {}
            block_num = math.ceil(seq_len / self.block_size)
            block_tables[group_id] = list(range(block_index, block_index+block_num))
            block_index += block_num
            seq = SequenceGroupMetadata(
                request_id=str(group_id),
                is_prompt=True,
                seq_data={group_id: seq_data},
                sampling_params=sampling_params,
                block_tables=block_tables,
                lora_request=dummy_lora_requests_per_seq[group_id]
                if dummy_lora_requests_per_seq else None,
                multi_modal_data=dummy_multi_modal_data,
            )
            seqs.append(seq)

        # Run the model with the dummy inputs.
        num_layers = self.model_config.get_num_layers(self.parallel_config)
        # npu
        num_kv_heads = self.model_config.get_num_kv_heads(self.parallel_config)
        head_size = self.model_config.get_head_size()
        from vllm.utils import STR_DTYPE_TO_TORCH_DTYPE
        if self.kv_cache_dtype == "auto":
            dtype = self.model_config.dtype
        else:
            dtype = STR_DTYPE_TO_TORCH_DTYPE[self.kv_cache_dtype]
        if self.model.soc_info.need_nz:
            kv_cache_shape = (block_index, num_kv_heads * head_size // 16, self.block_size, 16)
        else:
            kv_cache_shape = (block_index, self.block_size, num_kv_heads, head_size)
        kv_caches = [
            (
                torch.empty(
                    kv_cache_shape,
                    dtype=dtype,
                    device=self.device,
                ),
                torch.empty(
                    kv_cache_shape,
                    dtype=dtype,
                    device=self.device,
                ),
            )
            for _ in range(num_layers)
        ]
        # 
        finished_requests_ids = [seq.request_id for seq in seqs]
        model_input = self.prepare_model_input(
            seqs, finished_requests_ids=finished_requests_ids)
        intermediate_tensors = None
        self.execute_model(model_input, kv_caches, intermediate_tensors)
        logger.info(f"block_num of profile_run is: {block_index}")
        return block_index

    def set_total_slots(self, num_gpu_blocks: int) -> None:
        self.total_slots = torch.arange(num_gpu_blocks * self.block_size, dtype=torch.long)
        self.total_slots = self.total_slots.view(num_gpu_blocks, self.block_size) #
    
    def remove_all_loras(self):
        if not self.lora_manager:
            raise RuntimeError("LoRA is not enabled.")
        self.lora_manager.remove_all_adapters()

    def set_active_loras(self, lora_requests: Set[LoRARequest],
                         lora_mapping: LoRAMapping) -> None:
        if not self.lora_manager:
            raise RuntimeError("LoRA is not enabled.")
        self.lora_manager.set_active_adapters(lora_requests, lora_mapping)

    def add_lora(self, lora_request: LoRARequest) -> bool:
        if not self.lora_manager:
            raise RuntimeError("LoRA is not enabled.")
        return self.lora_manager.add_adapter(lora_request)

    def remove_lora(self, lora_id: int) -> bool:
        if not self.lora_manager:
            raise RuntimeError("LoRA is not enabled.")
        return self.lora_manager.remove_adapter(lora_id)

    def pin_lora(self, lora_id: int) -> bool:
        if not self.lora_manager:
            raise RuntimeError("LoRA is not enabled.")
        return self.lora_manager.pin_adapter(lora_id)

    def list_loras(self) -> Set[int]:
        if not self.lora_manager:
            raise RuntimeError("LoRA is not enabled.")
        return self.lora_manager.list_adapters()

    def remove_all_prompt_adapters(self):
        if not self.prompt_adapter_manager:
            raise RuntimeError("PromptAdapter is not enabled.")
        self.prompt_adapter_manager.remove_all_adapters()

    def set_active_prompt_adapters(
            self, prompt_adapter_requests: Set[PromptAdapterRequest],
            prompt_adapter_mapping: PromptAdapterMapping) -> None:
        if not self.prompt_adapter_manager:
            raise RuntimeError("PromptAdapter is not enabled.")
        self.prompt_adapter_manager.set_active_adapters(
            prompt_adapter_requests, prompt_adapter_mapping)

    def add_prompt_adapter(
            self, prompt_adapter_request: PromptAdapterRequest) -> bool:
        if not self.prompt_adapter_manager:
            raise RuntimeError("PromptAdapter is not enabled.")
        return self.prompt_adapter_manager.add_adapter(prompt_adapter_request)

    def remove_prompt_adapter(self, prompt_adapter_id: int) -> bool:
        if not self.prompt_adapter_manager:
            raise RuntimeError("PromptAdapter is not enabled.")
        return self.prompt_adapter_manager.remove_adapter(prompt_adapter_id)

    def pin_prompt_adapter(self, prompt_adapter_id: int) -> bool:
        if not self.prompt_adapter_manager:
            raise RuntimeError("PromptAdapter is not enabled.")
        return self.prompt_adapter_manager.pin_adapter(prompt_adapter_id)

    def list_prompt_adapters(self) -> Set[int]:
        if not self.prompt_adapter_manager:
            raise RuntimeError("PromptAdapter is not enabled.")
        return self.prompt_adapter_manager.list_adapters()

    @property
    def vocab_size(self) -> int:
        return self.model_config.get_vocab_size()


class NPUModelRunner(NPUModelRunnerBase[ModelInputForNPUWithSamplingMetadata]):
    """
    GPU model runner with sampling step.
    """
    _model_input_cls: Type[ModelInputForNPUWithSamplingMetadata] = (
        ModelInputForNPUWithSamplingMetadata)
    _builder_cls: Type[ModelInputForNPUBuilder] = ModelInputForNPUBuilder

    def make_model_input_from_broadcasted_tensor_dict(
        self,
        tensor_dict: Dict[str, Any],
    ) -> ModelInputForNPUWithSamplingMetadata:
        model_input = \
            ModelInputForNPUWithSamplingMetadata.from_broadcasted_tensor_dict(
                tensor_dict,
                # attn_backend=self.attn_backend,
            )
        return model_input

    def prepare_model_input(
        self,
        seq_group_metadata_list: List[SequenceGroupMetadata],
        virtual_engine: int = 0,
        finished_requests_ids: Optional[List[str]] = None
    ) -> ModelInputForNPUWithSamplingMetadata:
        """Prepare the model input based on a given sequence group, including
        metadata for the sampling step.

        The API assumes seq_group_metadata_list is sorted by prefill -> decode.

        The result tensors and data structure also batches input in prefill
        -> decode order. For example,

        - input_tokens[:num_prefill_tokens] contains prefill tokens.
        - input_tokens[num_prefill_tokens:] contains decode tokens.

        If cuda graph is required, this API automatically pads inputs.
        """
        model_input = self._prepare_model_input_tensors(
            seq_group_metadata_list, finished_requests_ids)
        if get_pp_group().is_last_rank:
            # Sampling metadata is only required for the final pp group
            generators = self.get_generators(finished_requests_ids)
            sampling_metadata = SamplingMetadata.prepare(
                seq_group_metadata_list, model_input.seq_lens,
                model_input.query_lens, self.device, self.pin_memory,
                generators, self.sampling_metadata_cache)
        else:
            sampling_metadata = None
        # is_prompt = (seq_group_metadata_list[0].is_prompt
        #              if seq_group_metadata_list else None)
        return dataclasses.replace(model_input,
                                   sampling_metadata=sampling_metadata,
                                   virtual_engine=virtual_engine)

    @torch.inference_mode()
    def execute_model(
        self,
        model_input: ModelInputForNPUWithSamplingMetadata,
        kv_caches: List[Tuple[torch.Tensor, torch.Tensor]],
        intermediate_tensors: Optional[IntermediateTensors] = None,
        num_steps: int = 1,
    ) -> Optional[Union[List[SamplerOutput], IntermediateTensors]]:
        if num_steps > 1:
            raise ValueError("num_steps > 1 is not supported in ModelRunner")

        if self.lora_config:
            assert model_input.lora_requests is not None
            assert model_input.lora_mapping is not None
            self.set_active_loras(model_input.lora_requests,
                                  model_input.lora_mapping)

        if self.prompt_adapter_config:
            assert model_input.prompt_adapter_requests is not None
            assert model_input.prompt_adapter_mapping is not None
            self.set_active_prompt_adapters(
                model_input.prompt_adapter_requests,
                model_input.prompt_adapter_mapping)

        # Currently cuda graph is only supported by the decode phase.
        # assert model_input.attn_metadata is not None
        # prefill_meta = model_input.attn_metadata.prefill_metadata
        # decode_meta = model_input.attn_metadata.decode_metadata
                
        max_seq_len = max(model_input.query_lens)
        #
        logits = self.model.forward(
            input_ids=model_input.input_tokens,
            position_ids=model_input.input_positions,
            is_prefill=model_input.is_prompt,
            block_tables=model_input.input_block_tables,
            kv_cache=kv_caches,
            slots=model_input.input_slot_tables,
            input_lengths=model_input.input_seq_lens,
            max_seq_len=max_seq_len,
            lm_head_indices=model_input.input_lm_head_indices
        )
        torch.npu.synchronize()
        
        if not self.is_driver_worker:
            return []
        
        output = self.sampler(logits, model_input.sampling_metadata)
        return [output]

