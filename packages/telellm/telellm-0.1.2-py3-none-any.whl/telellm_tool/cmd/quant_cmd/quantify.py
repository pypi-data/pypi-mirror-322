# Copyright 2024 State Cloud.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""quantify"""
import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from telellm_tool.cmd.quant_cmd.quant_utils import load_jsonl, copy_tokenizer_files, modify_config, check_directory, disable_layers

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

class Quantifier:
    """The `Quantifier` class initializes a model for quantization and provides methods for
       tokenizing data and converting it to quantized format."""
    def __init__(self, model_path_or_name, quant_config=None, anti_outlier_config=None):
        self.dev_type = quant_config.dev_type
        device_map = "cpu" if self.dev_type == "cpu" else "auto"

        self.quant_config = quant_config
        self.anti_outlier_config = anti_outlier_config
        self.model_path_or_name = model_path_or_name
        self.config = AutoConfig.from_pretrained(self.model_path_or_name, trust_remote_code=True)
        self.dtype = self.config.torch_dtype if self.dev_type == "npu" else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=model_path_or_name,
            low_cpu_mem_usage=True, torch_dtype=self.dtype,
            device_map=device_map,
            trust_remote_code=True,
            use_safetensors=True)
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path_or_name, trust_remote_code=True
        )

    def get_tokenized_data(self, calib_list,
                           input_ids_name='input_ids',
                           attention_mask_name='attention_mask'):
        """
        The function `get_tokenized_data` tokenizes a list of calibration data using a tokenizer and
        returns the tokenized dataset.
        """
        calib_dataset = []
        for calib_data in calib_list:
            inputs = self.tokenizer(calib_data, return_tensors='pt').to(self.dev_type)
            calib_dataset.append(
                [inputs.data[input_ids_name], None, inputs.data[attention_mask_name]])
        return calib_dataset

    def convert(self, tokenized_data, save_path, disable_level):
        """
        The function `convert` processes tokenized data, applies anti-outlier filtering if configured,
        calibrates the model, and saves the calibrated model.
        """
        from modelslim.pytorch.llm_ptq.anti_outlier import AntiOutlier
        from modelslim.pytorch.llm_ptq.llm_ptq_tools import Calibrator
        if self.dev_type == "npu":
            # 避免在线编译算子，使用二进制编译的算子
            torch.npu.set_compile_mode(jit_compile=False)

        if self.anti_outlier_config is not None:
            logging.info("start anti outlier")
            anti_outlier = AntiOutlier(self.model, calib_data=tokenized_data, cfg=self.anti_outlier_config)
            anti_outlier.process()
            logging.info("anti outlier successfully")

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        logging.info("start calibrator")
        calibrator = Calibrator(self.model, self.quant_config, calib_data=tokenized_data, disable_level=disable_level)
        calibrator.run()
        logging.info("calibrator successfully")
        calibrator.save(save_path, save_type=["safe_tensor"])

def start_quant_llm(config):
    """
    This function `start_quant_llm` performs quantization of a language model using specified
    configurations and saves the quantized model to a specified directory.
    """
    from modelslim.pytorch.llm_ptq.anti_outlier import AntiOutlierConfig
    from modelslim.pytorch.llm_ptq.llm_ptq_tools import QuantConfig
    # 使用npu量化需要引入以下环境变量
    # os.environ["PYTORCH_NPU_ALLOC_CONF"] = "expandable_segments:False"
    # os.system('export PYTORCH_NPU_ALLOC_CONF')
    rank = int(os.getenv("RANK", "0"))

    calib_texts = None
    if config.calib_file is not None:
        calib_texts = load_jsonl(config.calib_file)
    model_path = config.model_path
    save_directory = config.save_directory

    disable_names = None
    if config.disable_names is not None:
        disable_names = disable_layers(model_path, config.disable_names)
        logging.info(f'disable_names are: {disable_names}')

    quant_conf = QuantConfig(
        w_bit=config.w_bit,
        a_bit=config.a_bit,
        w_sym=config.w_sym,
        act_method=config.act_method,
        disable_names=disable_names,
        pr=config.pr,
        mm_tensor=config.mm_tensor,
        dev_type=config.dev_type,
        dev_id=rank,
        co_sparse=config.co_sparse,
        fraction=config.fraction,
        nonuniform=config.nonuniform,
        w_method=config.w_method,
        is_lowbit=config.is_lowbit,
        do_smooth=config.do_smooth,
        sigma_factor=config.sigma_factor,
        use_sigma=config.use_sigma
    )

    anti_outlier_conf = None
    if config.anti_method is not None:
        anti_outlier_conf = AntiOutlierConfig(
            w_bit=config.w_bit,
            a_bit=config.a_bit,
            dev_type=config.dev_type,
            dev_id=rank,
            anti_method = config.anti_method,
            w_sym=config.w_sym
        )

    quantifier = Quantifier(model_path, quant_conf, anti_outlier_conf)

    tokenized_calib_data = None
    if calib_texts is not None:
        tokenized_calib_data = quantifier.get_tokenized_data(
            calib_texts,
            input_ids_name="input_ids",
            attention_mask_name="attention_mask"
        )

    # check save directory
    check_directory(save_directory)

    logging.info('start quantize')
    quantifier.convert(tokenized_calib_data, save_directory, config.disable_level)
    auto_config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
    # 如原有权重配置文件无，默认使用fp16
    if auto_config.torch_dtype is None:
        auto_config.torch_dtype = "float16"
    modify_config(model_path, save_directory, auto_config.torch_dtype,
                  f"w{config.w_bit}a{config.a_bit}" + ("s" if config.co_sparse else ""))
    copy_tokenizer_files(model_path, save_directory)
    logging.info("saved successfully, end quantize!")
