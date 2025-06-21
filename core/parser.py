import jsbeautifier  # type: ignore
import re
from .context import ContextGetter  # type: ignore
import sys
import os
from typing import Any
from argparse import Namespace
import requests  # type: ignore
from requests_file import FileAdapter  # type: ignore
from typing import List, Dict


class Parser:
    def __init__(self, args: Namespace, regex: Any):
        self.args = args
        self.regex = regex
        self.MAX_FILE_LENGTH = 1000000

    def should_exclude_file(self, filename: str, exclude: List[str]) -> bool:
        """  Check if a file should be excluded based on its filename
        Args:
            filename (str): The name of the file to check.
            exclude (list): A list of file suffixes to exclude.
        Returns:
            bool: True if the file should be excluded, False otherwise."""
        if not exclude:
            return False
        # 直接遍历 exclude 列表
        exclude_suffixes = [s if s.startswith('.') else '.' + s for s in exclude]  # noqa
        return any(filename.lower().endswith(suffix.lower()) for suffix in exclude_suffixes)  # noqa

    def should_include_file(self, filename: str, include: List[str]) -> bool:
        """ Check if a file should be included based on its filename
        Args:
            filename (str): The name of the file to check.
            include (list): A list of file suffixes to include.
        Returns:
            bool: True if the file should be included, False otherwise."""
        if not include:
            return True
        # 直接遍历 include 列表
        include_suffixes = [s if s.startswith('.') else '.' + s for s in include]  # noqa
        return any(filename.lower().endswith(suffix.lower()) for suffix in include_suffixes)  # noqa

    def read_scan_file(self, url: str) -> str:
        # read local file
        # https://github.com/dashea/requests-file
        s = requests.Session()
        s.mount('file://', FileAdapter())
        return s.get(url).content.decode('utf-8', 'replace')

    def parser_error(self, msg: str) -> str:
        """ Print error message and usage information.
        Args:
            msg (str): The error message to be displayed.
        Returns:
            str: A formatted error message including usage information.
        """  # noqa
        print('Usage: python %s [OPTIONS] use -h for help' % sys.argv[0])
        return "[ - ] Error: %s" % msg  # noqa

    def parser_file(self, content: str, mode=1,
                    more_regex=None, no_dup=1) -> List[Dict[str, Any]]:
        ''' Parse the content of a file or string for regex matches.
        Args:
            content (str): The content to be parsed.
            mode (int): 1 for HTML output, 0 for CLI output.
            more_regex (str): Additional regex to filter results.
            no_dup (int): If 1, remove duplicate matches.
        Returns:
            list: A list of dictionaries containing matched items
            and their context.
        '''
        if mode == 1:
            if len(content) > self.MAX_FILE_LENGTH:
                content = content.replace(";", ";\r\n").replace(",", ",\r\n")
            else:
                content = jsbeautifier.beautify(content)
        all_items = []
        for regex in self.regex.items():
            patterns = regex[1] if isinstance(regex[1], list) else [regex[1]]
            for pattern in patterns:
                # 移除正则中的 (?i) 标志，避免与 re.I 冲突
                if isinstance(pattern, str):
                    pattern = re.sub(r'\(\?i\)', '', pattern)
                try:
                    r = re.compile(pattern, re.VERBOSE | re.I)
                except re.error as e:
                    print(f"Invalid regex pattern '{pattern}': {e}")
                    continue
                if mode == 1:
                    all_matches = [
                        (m.group(0), m.start(0), m.end(0),
                         content.count('\n', 0, m.start(0)) + 1)
                        for m in re.finditer(r, content)
                    ]
                    items = ContextGetter.get_context(all_matches,
                                                      content, regex[0])
                    if items != []:
                        all_items.append(items)
                else:
                    items = [{
                        'matched': m.group(0),
                        'context': [],
                        'name': regex[0],
                        'multi_context': False,
                        'line': content.count('\n', 0, m.start(0)) + 1  # 增加行号
                    } for m in re.finditer(r, content)]
                if items != []:
                    all_items.append(items)
        if all_items != []:
            k = []
            for i in range(len(all_items)):
                for ii in all_items[i]:
                    if ii not in k:
                        k.append(ii)
            if k != []:
                all_items = k

        if no_dup:
            all_matched = set()
            no_dup_items = []
            for item in all_items:
                if item != [] and type(item) is dict:
                    if item['matched'] not in all_matched:
                        all_matched.add(item['matched'])
                        no_dup_items.append(item)
            all_items = no_dup_items

        filtered_items = []
        if all_items != []:
            for item in all_items:
                if more_regex:
                    if re.search(more_regex, item['matched']):
                        filtered_items.append(item)
                else:
                    filtered_items.append(item)
        return filtered_items

    def parser_input(self, input: str) -> List[str]:
        ''' Parse the input string to determine if it is a file path or directory,
        and return a list of file paths that match the input criteria.
        Args:
            input (str): The input string which can be file path or directory.
        Returns:
            list: A list of file paths that match the input criteria.
        '''  # noqa
        excludes = getattr(self.args, 'exclude', None)
        includes = getattr(self.args, 'only_type', None)

        abs_input = os.path.abspath(input)
        # method 1 dictory
        if os.path.isdir(abs_input):
            file_list = []
            for root, _, files in os.walk(abs_input):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    if includes:
                        if not self.should_include_file(fpath, includes):
                            continue
                    if excludes:
                        if self.should_exclude_file(fpath, excludes):
                            continue
                    file_list.append("file:///%s" % os.path.abspath(fpath).replace('\\', '/'))  # noqa
            if not file_list:
                return [self.parser_error('no files found in the directory')]
            return file_list

        if includes:
            if not self.should_include_file(input, includes):
                return []
        if excludes:
            if self.should_exclude_file(input, excludes):
                return []

        # method 2 - file
        if os.path.isfile(abs_input):
            return ["file:///%s" % abs_input.replace('\\', '/')]

        return [("file:///%s" % abs_input.replace('\\', '/')) if os.path.exists(abs_input) else self.parser_error('file could not be found (maybe you forgot to add http/https).')]  # noqa
