import os
from settings import EXCLUDE_FILE_SUFFIEX  # type: ignore
from typing import Set


class ShowFileType:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_file_types(self) -> Set[str]:
        """return a set of file types (extensions) from the given file path or directory.
        If the path is a directory, it recursively collects all file extensions.
        If the path is a file, it returns the extension of that file.
        Returns:
            set[str]: A set of file extensions (without leading dot).
        """  # noqa
        file_types: Set[str] = set()

        if not self.file_path:
            return file_types

        if os.path.isdir(self.file_path):
            # 递归遍历目录，收集所有文件后缀
            for root, _, files in os.walk(self.file_path):
                for fname in files:
                    _, ext = os.path.splitext(fname)
                    if ext:
                        file_types.add(ext.lower().strip('.'))
        elif os.path.isfile(self.file_path):
            # 单个文件，直接获取后缀
            _, ext = os.path.splitext(self.file_path)
            if ext:
                file_types.add(ext.lower().strip('.'))

        # minus any excluded suffixes
        file_types = {ft for ft in file_types if ft not in EXCLUDE_FILE_SUFFIEX}  # noqa

        return file_types
