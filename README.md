# YscFinder Usage Instructions

## About YscFinder

> Tool Name: YscFinder
> Author: dikesi131 (https://github.com/dikesi131)
> Development Purpose: A scanning tool for discovering API Keys, access tokens, and sensitive data
> Reference Project: SecretFinder - [github.com/m4ll0k](https://github.com/m4ll0k)

------

## 📌 Introduction

**YscFinder** is a security scanning tool designed to detect potential sensitive information (such as API Keys, Tokens, passwords, etc.) in source code files. It supports keyword scanning, detection of sensitive function calls, and vulnerability pattern matching, and provides both a CLI command-line interface and a GUI graphical interface for operation.

This project is inspired by [SecretFinder](https://github.com/m4ll0k/SecretFinder) and has undergone localization optimization and feature enhancement, making it compatible with the Python 3 environment.

------

## 🔍 Main Features

- ✅ Supports keyword scanning (Keyword Scan)
- ✅ Supports detection of sensitive function calls (Sensitive Function Scan)
- ✅ Supports vulnerability pattern matching (Vulnerability Scan)
- ✅ Allows specifying specific file suffix types for scanning (e.g., `.js`, `.ts`)
- ✅ Supports excluding certain file suffixes (e.g., `.png`, `.css`)
- ✅ Supports command-line output (CLI) and HTML report export
- ✅ Provides a graphical interface (GUI) for a more user-friendly operation

------

## Installation Method

1. Install dependencies:

   ```bash
   pip install -r requirements
   ```

2. Run the command-line version:

   ```bash
   python3 ysc_finder.py -h
   
   usage: ysc_finder.py [-h] -i INPUT [-ks KEYWORD_SCAN] [-ss SENSITIVE_FUNCTION_SCAN] [-vs VULN_SCAN] [-e EXCLUDE] [-nt ONLY_TYPE] [-o OUTPUT] [-v]
   
   options:
     -h, --help            show this help message and exit
     -i INPUT, --input INPUT
                           Input file or folder, example: "/User/test"
     -ks KEYWORD_SCAN, --keyword-scan KEYWORD_SCAN
                           Enable keyword scan, default: False
     -ss SENSITIVE_FUNCTION_SCAN, --sensitive-function-scan SENSITIVE_FUNCTION_SCAN
                           Enable sensitive function scan, default: False
     -vs VULN_SCAN, --vuln-scan VULN_SCAN
                           Enable vulnerability scan, default: False
     -e EXCLUDE, --exclude EXCLUDE
                           Exclude file suffixes (e.g: png;css)
     -nt ONLY_TYPE, --only-type ONLY_TYPE
                           Only scan files with the specified suffixes (e.g: js;ts)
     -o OUTPUT, --output OUTPUT
                           Where to save the file, including file name. Default: cli
     -v, --version         Show version of YscFinder
   ```

3. Run the graphical interface (GUI) version:

   ```bash
   python3 ysc_finder_gui.py
   ```

------

## Command-Line Usage

```bash
python3 ysc_finder.py -i <Input path or URL> [Other parameters]
```

### Common Parameters

| Parameter                      | Description                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| -h, --help                     | Display help information                                     |
| -i, --input                    | Input: URL, local file, or folder                            |
| -ks, --keyword-scan            | Enable keyword matching mode (default: disabled)             |
| -ss, --sensitive-function-scan | Enable sensitive function scanning (default: disabled)       |
| -vs, --vuln-scan               | Enable vulnerability scanning (default: disabled)            |
| -o, --output                   | Output file name. "cli" means command-line output, default is cli output |
| -e, --exclude                  | Specify file suffixes to exclude (separated by ;), default excludes common static files (e.g., png;css) |
| -nt, --only-type               | Only scan files with the specified suffixes (e.g., js;ts)    |
| -v, --version                  | Output the tool version number                               |

### Examples

- Scan a local file and output the HTML results to results.html:

  ```bash
  # Single file
  python3 ysc_finder.py -i test.js -o results.html
  # Directory
  python ysc_finder.py -i "test_data" -o results.html
  ```

- Command-line output (faster, does not use jsbeautifier):

  ```bash
  # Single file
  python3 ysc_finder.py -i test.js -o cli
  # Directory
  python ysc_finder.py -i "test_data" -o cli
  ```

- Save command-line output to a file

  ```bash
  # In Windows
  python3 ysc_finder.py -i test_data/test1.txt -o cli > scan_result.txt
  # In Linux/Macos
  python3 ysc_finder.py -i test_data/test1.txt -o cli | tee scan_result.txt
  ```

- Exclude specified file suffixes

  ```sh
  # Exclude js and ts files in the test_data directory
  python ysc_finder.py -i "test_data" -e "js;ts" -o cli
  ```

- Only scan specified file types

  ```sh
  # Only scan java and python files (separated by ;)
  python ysc_finder.py -i "test_data" -nt "java;py" -o cli
  ```

- Enable keyword matching mode

  ```sh
  python ysc_finder.py -i "test_data" -ks True -nt java -o cli
  python ysc_finder.py -i /path/to/code -ks -ss -o cli
  ```

------

## Graphical Interface (GUI) Usage

```bash
python3 ysc_finder_gui.py
```

### Function Introduction

- 📁 Supports selecting a "directory" or "file" as input
- 🔍 Multiple scanning options can be checked (keywords, sensitive functions, vulnerabilities)
- 📊 Automatically analyzes all file types in the target path
- 💾 Supports saving scan results as text or PDF format
- 🌗 Supports switching between light/dark themes
- 📈 Displays the scan progress bar and result details

### Summary of the Operation Process

1. Select the directory/file path.
2. Choose whether to enable scanning options such as keywords/sensitive functions, not enabled by default.
3. Analyze the scannable file types.
4. Optionally, specify the specific types to scan (usually we only focus on script files, such as py, java, etc.).
5. Click "Start Scan", and the progress bar at the bottom shows the real-time progress.
6. Confirm and process the scan results (manually delete false positives).
7. Save the scan results (txt and pdf). The pdf is more intuitive and readable, while the txt file is convenient for advanced users to perform further automated processing.

### Usage Process

1. Select the directory/file to scan

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615221618489.png)

1. Select additional scan categories to add

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615221702925.png)

The selected options will be appended to the tool's default scan. When nothing is selected, the tool uses content-based regular expression rules for scanning by default.

1. Analyze the scannable file types and select specific files to scan

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615222525261.png)

The ones marked in red are common script file formats, which we should focus on during scanning.

Subsequently, you can specify the file types to scan (separated by ;). When not specified, the tool will scan all file types in the analyzed file types. The tool excludes common static files by default, as shown below:

```python
EXCLUDE_FILE_SUFFIEX = [
    # Image files
    "jpg", "jpeg", "png", "gif", "svg", "webp",
    "bmp", "tiff", "tif",
    # Style sheet files
    "css", "scss", "sass", "less",
    # Font files
    "ttf", "otf", "woff", "woff2", "eot",
    # Configuration/data files
    "json", "yaml", "yml", "xml", "conf", "ini",
    "toml",
    # Document files
    "html", "htm", "pdf", "csv", "doc", "docx",
    "xls", "xlsx",
    # Certificate files
    "pem", "p12", "pfx", "crt", "cer",
    # Others
    "ico", "mp4", "avi", "mov", "mkv", "webm",
    "mp3", "wav", "ogg", "aac", "zip", "gitignore",
    "gitkeep", "gitattributes", "helmignore", "DS_Store", "lock", "vue",
    "pack", "db", "exe", "dll", "so", "dylib",
    "pyc",
]
```

1. Start scanning and analyze the results

After the scan is completed, the user can see the following results

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615222909488.png)

Result Explanation:

- The first line is the path of the scanned local file, and the rightmost is the button to open the file (note that the file is opened using the default application set by the current system. For example, txt files are opened with Notepad by default, and word files are opened with Office by default).
- Below are the scan results for this file. The left is the delete button. During manual review, false positives can be deleted. The second part is the line number of the matching result in the file, and the third part is the corresponding matching item (format: matching rule name -> matching result).

Since the tool may produce some false positives, the user can manually confirm whether the scan results are accurate. The steps are as follows:

- Click the "Open File" button to open the corresponding file, and locate the matching item based on the file line number.
- Confirm whether it is a false positive. If it is, click the delete button to delete the matching item.

1. Export the results

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615223759660.png)

The user can customize the export path and file name. The default export path is the tool's directory, and the default export file name is scan_results. The export formats support txt and pdf.

- txt format

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615223935946.png)

The first part is the statistical result of the scan results, which counts the number of hits for each scan rule. The second part is the specific scan results.

- pdf format

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615224112703.png)

Same as the txt format, the first part is the statistical result.

![image](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615224147070.png)

The second part is the specific scan results.

**It is worth mentioning that the final exported results are based on the user's operations on the page. That is, if the user deletes false positives, the exported results will not include them.**

------

## 📝 Rule Configuration Files

All scan rules are stored in JSON format in the following locations:

- `keywords.json` - Keyword matching rules
- `sensitive_func.json` - Sensitive function matching rules
- `vuln.json` - Vulnerability pattern matching rules
- `regex.json` - Basic general regular expressions

You can customize these rule files as needed to expand the scanning capabilities.

------

### Add Custom Excluded File Suffixes

Edit the `settings.py` file and add the custom file suffixes to exclude.

```python
# default exclude file suffiex
EXCLUDE_FILE_SUFFIEX = [
    # Image files
    "jpg", "jpeg", "png", "gif", "svg", "webp", "bmp", "tiff", "tif",
    # Style sheet files
    "css", "scss", "sass", "less",
    # Font files
    "ttf", "otf", "woff", "woff2", "eot",
    # Document files
    "html", "htm", "pdf", "csv", "doc", "docx", "xls", "xlsx",
    # Others
    "ico", "mp4", "avi",
    ......
]
```

------

### Add Custom Emphasized Script Files

Edit the `settings.py` file and add the custom script file suffixes.

```python
HIGHLIGHT_FILE_TYPES = [
    "js", "ts", "py", "java", "c",
    "cpp", "go", "rb", "php", "sh",
    "pl", "cs", "h", "hpp", "ps1",
    "bat", "lua"
    ......
]
```

After adding, they will be marked in red in the GUI.

------

## 📤 Report Export

- **CLI Mode**: The results are output to the terminal by default, or can be saved as a text file using the `-o` parameter.
- **GUI Mode**: Click the "Save Results" button to save the results in `.txt` or `.pdf` format.

------

## 🧪 Test Recommendations

- Run in a test environment to avoid affecting the production system.
- Combine with Git repositories for historical commit scanning to find potentially leaked sensitive information.
- For large projects, it is recommended to use the GUI to view detailed results.

------

## 📜 License

This project is licensed under the GNU General Public License v3.0 – see the LICENSE file for details.

This software uses code from [SecretFinder], which is also licensed under GPLv3.