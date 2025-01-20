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
"""file_utils"""
import os
import re
import stat

from typing import Tuple


def get_dir_files(path):
    """
    Recursively retrieves all directories and files from a specified path.
    """
    files = []
    dirs = []
    for dir_path, dir_names, file_names in os.walk(path):
        for dir_name in dir_names:
            dirs.append(os.path.join(dir_path, dir_name))
        for file_name in file_names:
            files.append(os.path.join(dir_path, file_name))
    return dirs, files

class PathCheck:
    """
    Provides utilities to validate, check, and manage various aspects of file system paths, including existence,
    permissions, and ownership.
    """
    @classmethod
    def check_path_full(cls, path: str, is_support_root: bool = True) -> Tuple[bool, str]:
        """
        Validates the full path by checking its validity, existence, symbolic link status, and ownership.
        """
        # 检查路径是否合法
        ret, infos = cls.check_path_valid(path)
        if not ret:
            return ret, infos
        # 检查是否为软链接
        ret, infos = cls.check_path_link(path)
        if not ret:
            return ret, infos
        # 检查路径是否存在
        ret, infos = cls.check_path_exists(path)
        if not ret:
            return ret, infos
        # 检查路径属组
        return cls.check_path_owner_group_valid(path, is_support_root)

    @classmethod
    def check_path_valid(cls, path: str) -> Tuple[bool, str]:
        """
        Checks if the path is valid, ensuring it contains no special characters and is not too long.
        """
        if not path:
            return False, "The path is empty."
        if len(path) > 1024:
            return False, " The length of path exceeds 1024 characters."
        pattern_name = re.compile(r"[^0-9a-zA-Z_./-]")
        match_name = pattern_name.findall(path)
        if match_name or ".." in path:
            return False, "The path contains special characters."
        return True, ""

    @classmethod
    def check_path_exists(cls, path: str) -> Tuple[bool, str]:
        """
        Checks if the path exists in the filesystem.
        """
        if not os.path.exists(path):
            return False, "The path is not exists."
        return True, ""

    @classmethod
    def check_path_link(cls, path: str) -> Tuple[bool, str]:
        """
        Checks if the path is a symbolic link.
        """
        if os.path.islink(path):
            return False, "The path is a soft link."
        return True, ""

    @classmethod
    def check_path_mode(cls, mode: int, path: str) -> Tuple[bool, str]:
        """
        Checks if the path has the specified mode (permissions).
        """
        cur_stat = os.stat(path)
        cur_mode = stat.S_IMODE(cur_stat.st_mode)
        if cur_mode != mode:
            return False, "Check the path mode failed."
        return True, ""

    @classmethod
    def check_path_owner_group_valid(cls, path: str, is_support_root: bool = True) -> Tuple[bool, str]:
        """
        Verifies if the path is owned by the current user or root (if supported).
        """
        cur_user_id = os.getuid()
        cur_user_grp_id = os.getgid()

        file_info = os.stat(path)
        file_user_id = file_info.st_uid
        file_user_grp_id = file_info.st_gid

        flag = file_user_id == cur_user_id and file_user_grp_id == cur_user_grp_id
        if is_support_root:
            flag = flag or (file_user_id == 0 and file_user_grp_id == 0)
        if flag:
            return True, ""
        return False, "Check the path owner and group failed."

    @classmethod
    def check_system_path(cls, path: str) -> Tuple[bool, str]:
        """
        Ensures the path is not within system directories (like /usr/bin).
        """
        system_paths = ["/usr/bin/", "/usr/sbin/", "/etc/", "usr/lib/", "/usr/lib64/"]
        real_path = os.path.realpath(path)
        for sys_prefix in system_paths:
            if real_path.startswith(sys_prefix):
                return False, f"Invalid path, it is in system path: {sys_prefix}."
        return True, ""
