import os
import sys
import subprocess
from urllib.parse import urlparse


class FileOpener:
    @staticmethod
    def _parse_uri(file_uri: str) -> str:
        '''parse a file URI or local path to a standard file path.
        This method handles both `file://` URIs and local file paths.
        It ensures that the path is correctly formatted for the current operating system.
        If the URI uses the `file://` scheme, it will convert it to a local file path.
        If the URI is a local path, it will return it as is.

        Args:
            file_uri (_type_): file URI or local path to be parsed.

        Returns:
            _type_: A standard file path as a string.
        '''  # noqa
        parsed = urlparse(file_uri)
        if parsed.scheme == 'file':
            path = parsed.path
            # Windows 下去掉前导斜杠
            if sys.platform.startswith("win") and path.startswith("/"):
                path = path[1:]
        else:
            path = file_uri
        return path

    @staticmethod
    def _check_file_exists(path: str):
        """check if the file exists at the given path.
        Args:
            path (str): The file path to check.
        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
        """  # noqa
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件不存在: {path}")

    @staticmethod
    def _open_on_windows(path: str):
        '''Open a file using PowerShell on Windows.

        Args:
            path (_type_): The file path to open.

        Raises:
            RuntimeError: If the file cannot be opened using PowerShell.
        '''
        try:
            # 使用 PowerShell 启动进程
            subprocess.run(['powershell', '-Command',
                            f'Start-Process "{path}"'], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"can not open file by powershell: {path}") from e  # noqa: E501

    @staticmethod
    def _open_on_macos(path: str):
        """Open a file using the default application on macOS.
        Args:
            path (str): The file path to open.
        Raises:
            RuntimeError: If the file cannot be opened.
        """
        try:
            subprocess.run(["open", path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"can not open file by open: {path}") from e

    @staticmethod
    def _open_on_linux(path: str):
        """Open a file using the default application on Linux.
        Args:
            path (str): The file path to open.
        Raises:
            RuntimeError: If the file cannot be opened.
        """
        try:
            subprocess.run(["xdg-open", path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"can not open file by xdg-open: {path}") from e

    def open_file_by_uri(self, file_uri: str):
        """ open a file by its URI or local path.
        This method checks if the file exists and then opens it using the appropriate
        method based on the operating system.
        Args:
            file_uri (str): The file URI or local path to open.
        Raises:
            RuntimeError: If the file cannot be opened or if the operating system is unsupported.
            FileNotFoundError: If the file does not exist at the specified path.
        """  # noqa
        path = self._parse_uri(file_uri)
        self._check_file_exists(path)

        try:
            if sys.platform == "darwin":
                self._open_on_macos(path)
            elif sys.platform.startswith("win"):
                self._open_on_windows(path)
            elif sys.platform.startswith("linux"):
                self._open_on_linux(path)
            else:
                raise RuntimeError("不支持的操作系统")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"无法打开文件: {path}") from e

    def open_file_at_line(self, file_uri: str, line_number: str):
        """ Open a file at a specific line number using the default editor.
        This method attempts to open the file using Visual Studio Code or Notepad++.
        If those editors are not available, it falls back to the default application
        for the file type. It raises an error if the file does not exist or if no
        suitable editor is found.
        Args:
            file_uri (str): The file URI or local path to open.
            line_number (str): The line number to jump to in the file.
        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            RuntimeError: If the file cannot be opened using the specified editors.
        """  # noqa
        path = self._parse_uri(file_uri)
        self._check_file_exists(path)

        try:
            # 尝试使用 VS Code
            subprocess.run(["code", "--goto", f"{path}:{line_number}"],
                           check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"无法使用 VS Code 打开文件：{e}")
            try:
                # 尝试使用 Notepad++（Windows）
                if sys.platform.startswith("win"):
                    subprocess.run(["notepad++.exe", path,
                                    f"-n{line_number}"], check=True)
                else:
                    # 回退到默认程序
                    self.open_file_by_uri(path)
                    print(f"已使用默认程序打开文件（不支持跳转行号）：{path}")
            except Exception as e:
                print(f"无法使用特定编辑器打开文件：{e}")
                print("请确认是否安装了支持跳转行号的编辑器（如 VS Code、Notepad++ 等）")
