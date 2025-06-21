# Portions of this code are derived from the original work:
# Copyright (C) 2020 m4ll0k(https://github.com/m4ll0k)

# Modified and extended by:
# Copyright (C) 2025 dikesi131(https://github.com/dikesi131)


import json
import argparse
from html import escape
import urllib3
import os
import sys

from core.parser import Parser
from core.html_output import HtmlOutput
from core.cli_output import CliOutput
from core.decorators import timing_decorator
from settings import (KEYWORDS_FILE, BASIC_REGEX_FILE, __VERSION__,
                      EXCLUDE_FILE_SUFFIEX, HTML_TEMPLATE,
                      SENSITIVE_FUNC_FILE, VULN_FILE, TOOL_NAME)

if not sys.version_info.major >= 3:
    print("[ + ] Run this tool with python version 3.+")
    sys.exit(0)
os.environ["BROWSER"] = "open"


def resource_path(relative_path: str) -> str:
    """ Get the absolute path to the resource, works for both development and PyInstaller. 
    Args:
        relative_path (str): The relative path to the resource.
    Returns:
        str: The absolute path to the resource.
    """  # noqa
    # If the application is run as a bundle (e.g., PyInstaller),
    # the _MEIPASS attribute is set.
    # This allows us to find the resource in the temporary directory
    # where PyInstaller extracts it.
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        return os.path.join(meipass, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# basic regex
basic_regex_path = resource_path(BASIC_REGEX_FILE)
basic_regex = json.load(open(basic_regex_path, 'r', encoding='utf-8'))  # noqa

# keywords regex
keyword_regex_path = resource_path(KEYWORDS_FILE)
keywords_regex = json.load(open(keyword_regex_path, 'r', encoding='utf-8'))  # noqa

# sensitive function regex
sensitive_func_path = resource_path(SENSITIVE_FUNC_FILE)
sensitive_func_regex = json.load(open(sensitive_func_path, 'r', encoding='utf-8'))  # noqa

# vulnerability regex
vuln_path = resource_path(VULN_FILE)
vuln_regex = json.load(open(vuln_path, 'r', encoding='utf-8'))  # noqa

# default HTML template
_template = HTML_TEMPLATE


@timing_decorator
def main(args, progress_callback=None):
    """ Main function to run the YscFinder tool.
    Args:
        args (argparse.Namespace): Parsed command line arguments.
        progress_callback (callable, optional): A callback function to report progress.
    Returns:
        None
    """  # noqa
    # Combine all regexes based on scan options
    _regex = basic_regex.copy()
    if args.keyword_scan:
        _regex.update(keywords_regex)
    if args.sensitive_function_scan:
        _regex.update(sensitive_func_regex)
    if args.vuln_scan:
        _regex.update(vuln_regex)
    parser = Parser(args, _regex)

    if args.input[-1:] == "/":
        # /aa/ -> /aa
        args.input = args.input[:-1]

    if args.only_type:
        # convert only type file suffixes to list
        if ';' in args.only_type:
            args.only_type = args.only_type.split(';')
        else:
            args.only_type = [args.only_type]
        # remove empty strings
        args.only_type = [s.strip() for s in args.only_type if s]

    if args.exclude:
        # convert exclude file suffixes to list
        if ';' in args.exclude:
            args.exclude = args.exclude.split(';')
        else:
            args.exclude = [args.exclude]
    # remove empty strings
    args.exclude = [s.strip() for s in args.exclude if s]
    # add default exclude file suffixes
    args.exclude.extend(EXCLUDE_FILE_SUFFIEX)

    regex_keys = list(basic_regex.keys())
    keywords_keys = list(keywords_regex.keys())
    sensitive_func_keys = list(sensitive_func_regex.keys())
    vuln_keys = list(vuln_regex.keys())
    # combine regex keys and keyword keys
    all_keys = regex_keys + keywords_keys + sensitive_func_keys + vuln_keys

    # mode 1 is HTML output, mode 0 is CLI output
    mode = 1
    if args.output == "cli":
        #  create CliOutput object
        cli_output = CliOutput(all_keys)
        mode = 0

    # convert input to files
    urls = parser.parser_input(args.input)
    total = len(urls)
    # conver URLs to js file
    output = ''
    for idx, url in enumerate(urls, 1):
        file = parser.read_scan_file(url)

        matched = parser.parser_file(file, mode)
        if not matched:
            if progress_callback:
                progress_callback(idx, total)
            continue
        print(f'[ + ] URL: {url}')
        if args.output == 'cli':
            cli_output.cli_print(matched)
        else:
            output += '<h1>File: <a href="%s" target="_blank" rel="nofollow noopener noreferrer">%s</a></h1>' % (escape(url), escape(url))  # noqa
            for match in matched:
                # _matched = match.get('matched')
                _named = match.get('name')
                header = '<div class="text">%s (Line: %s)' % ((_named.replace('_', ' ') if _named else ''), match.get('line', '-'))  # noqa
                body = ''
                # find same thing in multiple context
                if match.get('multi_context'):
                    no_dup = []
                    contexts = match.get('context')
                    if contexts is not None:
                        for context in contexts:
                            if context and context not in no_dup:  # 只处理非空内容
                                body += '</a><div class="container">%s</div></div>' % (escape(context))  # noqa
                                no_dup.append(context)
                else:
                    ctx = match.get('context')
                    if ctx and len(ctx) > 0 and ctx[0]:
                        body += '</a><div class="container">%s</div></div>' % (escape(ctx[0]))  # noqa
                output += header + body
                if progress_callback:
                    progress_callback(idx, total)
    if args.output != 'cli':
        HtmlOutput(_template, args).save(output)
    print(f'[ - ] A total of {len(urls)} files were scanned')

    # print statistics
    positive_counts = cli_output.get_positive_counts()
    if not positive_counts:
        print("[ - ] No keys with occurrences greater than 0 found.")
        return
    print("[ - ] Counts of keys with occurrences greater than 0:")
    # arrange keys by count in descending order
    positive_counts = {k: v for k, v in sorted(positive_counts.items(),
                                               key=lambda item: item[1],
                                               reverse=True)}
    # print each key and its count
    for key, count in positive_counts.items():
        print(f"[ matched ] {key}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="Input file or folder, examlple: \"/User/test\"",  # noqa
                        required=True, action="store")
    parser.add_argument("-ks", "--keyword-scan",
                        help="Enable keyword scan, default: False",
                        action="store", default=False)
    parser.add_argument("-ss", "--sensitive-function-scan",
                        help="Enable sensitive function scan, default: False",  # noqa
                        action="store", default=False)
    parser.add_argument("-vs", "--vuln-scan",
                        help="Enable vulnerability scan, default: False",
                        action="store", default=False)
    parser.add_argument("-e", "--exclude",
                        help="Exclude file suffixes (e.g: png;css)",
                        action="store", default="")
    parser.add_argument("-nt", "--only-type",
                        help="Only scan files with the specified suffixes (e.g: js;ts)",  # noqa
                        action="store", default="")
    parser.add_argument("-o", "--output",
                        help="Where to save the file, including file name. Default: cli",  # noqa
                        action="store", default="cli")
    parser.add_argument("-v", "--version",
                        help=f"Show version of {TOOL_NAME}",
                        action="version",
                        version=f"{TOOL_NAME} v{__VERSION__}")
    args, unknown = parser.parse_known_args()
    main(args)
