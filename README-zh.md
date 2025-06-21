# YscFinder 使用说明

## 关于 YscFinder

> 工具名称：YscFinder
> 作者：dikesi131 (https://github.com/dikesi131)
> 开发目的：用于发现 API Key、访问令牌（Access Token）以及敏感数据的扫描工具
> 参考项目：SecretFinder - [github.com/m4ll0k](https://github.com/m4ll0k)

---

## 📌 简介

**YscFinder** 是一款用于检测源码文件中潜在敏感信息（如 API Key、Token、密码等）的安全扫描工具。它支持关键字扫描、敏感函数调用检测以及漏洞模式匹配，并提供 CLI 命令行界面 和 GUI 图形化界面两种操作方式。

该项目灵感来源于 [SecretFinder](https://github.com/m4ll0k/SecretFinder)，并进行了本地化优化与功能增强，适配  Python 3 环境。

---

## 🔍 主要功能

- ✅ 支持关键字扫描（Keyword Scan）
- ✅ 支持敏感函数调用检测（Sensitive Function Scan）
- ✅ 支持漏洞模式匹配（Vulnerability Scan）
- ✅ 支持指定扫描特定后缀类型的文件（例如：`.js`, `.ts`）
- ✅ 支持排除某些后缀文件（例如：`.png`, `.css`）
- ✅ 支持命令行输出（CLI）和 HTML 报告导出
- ✅ 提供图形化界面（GUI），操作更友好

---

## 安装方法

1. 安装依赖：

   ```bash
   pip install -r requirements
   ```

2. 运行命令行版本：

   ```bash
   python3 ysc_finder.py -h
   
   usage: ysc_finder.py [-h] -i INPUT [-ks KEYWORD_SCAN] [-ss SENSITIVE_FUNCTION_SCAN] [-vs VULN_SCAN] [-e EXCLUDE] [-nt ONLY_TYPE] [-o OUTPUT] [-v]
   
   options:
     -h, --help            show this help message and exit
     -i INPUT, --input INPUT
                           Input file or folder, examlple: "/User/test"
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

3. 运行图形界面（GUI）版本：

   ```bash
   python3 ysc_finder_gui.py
   ```

<img src="https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250610202644369.png" alt="image-20250610202638002" style="zoom:50%;" />

---

## 命令行用法

```bash
python3 ysc_finder.py -i <输入路径或URL> [其他参数]
```

### 常用参数

| 参数                            | 说明                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| -h, --help                      | 显示帮助信息                                                 |
| -i, --input                     | 输入：URL、本地文件或文件夹                                  |
| -ks, --keyword-scan             | 启用关键词匹配模式（默认关闭）                               |
| -ss`,`--sensitive-function-scan | 启用敏感函数扫描（默认关闭）                                 |
| -vs`,`--vuln-scan               | 启用漏洞扫描（默认关闭）                                     |
| -o, --output                    | 输出文件名，cli 表示命令行输出，默认为cli输出                |
| -e, --exclude                   | 指定要排除的文件后缀(以;分隔)，默认排除了常见的静态文件（如 png;css） |
| -nt, --only-type                | 仅扫描指定后缀的文件(如 js;ts)                               |
| -v, --version                   | 输出工具版本号                                               |

### 示例

- 扫描本地文件并输出 HTML 结果到 results.html：

  ```bash
  # 单个文件
  python3 ysc_finder.py -i test.js -o results.html
  # 目录
  python ysc_finder.py -i "test_data" -o results.html
  ```

- 命令行输出（速度更快，不使用 jsbeautifier）：

  ```bash
  # 单个文件
  python3 ysc_finder.py -i test.js -o cli
  # 目录
  python ysc_finder.py -i "test_data" -o cli
  ```

- 保存命令行输出到文件

  ```bash
  # in Windows
  python3 ysc_finder.py -i test_data/test1.txt -o cli > scan_result.txt
  # in Linux/Macos
  python3 ysc_finder.py -i test_data/test1.txt -o cli | tee scan_result.txt
  ```
  
- 排除指定文件后缀

  ```sh
  # 排除test_data目录下的js和ts文件
  python ysc_finder.py -i "test_data" -e "js;ts" -o cli
  ```
  
- 仅扫描指定的文件类型

  ```sh
  # 仅扫描java和python文件(以;分隔文件后缀)
  python ysc_finder.py -i "test_data" -nt "java;py" -o cli
  ```
  
- 启用关键字匹配模式

  ```sh
  python ysc_finder.py -i "test_data" -ks True -nt java -o cli
  python ysc_finder.py -i /path/to/code -ks -ss -o cli
  ```

---

## 图形界面（GUI）用法

```bash
python3 ysc_finder_gui.py
```

### 功能介绍

- 📁 支持选择“目录”或“文件”作为输入
- 🔍 多种扫描选项可勾选（关键字、敏感函数、漏洞）
- 📊 自动分析目标路径下所有文件类型
- 💾 支持保存扫描结果为文本或 PDF 格式
- 🌗 支持切换亮色/暗色主题
- 📈 显示扫描进度条及结果详情

### 操作流程总结

1. 选择目录/文件路径
2. 选择是否启用关键字/敏感函数等扫描选项，默认不启用
3. 分析可扫描的文件类型
4. 可选仅扫描的特定类型(通常我们只关注脚本文件，如py、java等)
5. 点击开始扫描，最下方进度条显示实时进度
6. 对扫描结果进行确认和处理(可人工删除误报结果)
7. 保存扫描结果(txt和pdf)，pdf更加直观，可读性更高，txt文件便于高级用户进行进一步自动化处理

### 使用流程

1. 选择要扫描的目录/文件

![image-20250615221618463](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615221618489.png)

2. 选择要增加的其他扫描类别

![image-20250615221702900](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615221702925.png)

选中的会附加到工具的默认扫描中，什么都不选时，工具默认使用基于内容的正则表达式规则进行扫描

3. 分析可扫描的文件类型并选择指定文件进行扫描

![image-20250615222525226](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615222525261.png)

其中红色标注的为常见脚本文件格式，我们扫描时应重点关注这些文件

随后可以指定要扫描的文件类型(以;分隔)，当不指定时，工具会将分析文件类型中的文件类型进行全扫描，工具默认排除了常见的静态文件，如下所示：

```python
EXCLUDE_FILE_SUFFIEX = [
    # 图片文件
    "jpg", "jpeg", "png", "gif", "svg", "webp",
    "bmp", "tiff", "tif",
    # 样式表文件
    "css", "scss", "sass", "less",
    # 字体文件
    "ttf", "otf", "woff", "woff2", "eot",
    # 配置文件/数据文件
    "json", "yaml", "yml", "xml", "conf", "ini",
    "toml",
    # 文档文件
    "html", "htm", "pdf", "csv", "doc", "docx",
    "xls", "xlsx",
    # 证书文件
    "pem", "p12", "pfx", "crt", "cer",
    # 其他
    "ico", "mp4", "avi", "mov", "mkv", "webm",
    "mp3", "wav", "ogg", "aac", "zip", "gitignore",
    "gitkeep", "gitattributes", "helmignore", "DS_Store", "lock", "vue",
    "pack", "db", "exe", "dll", "so", "dylib",
    "pyc",
]
```

4. 开始扫描并对结果进行分析

扫描完成后用户可以看到如下结果

![image-20250615222909454](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615222909488.png)

结果说明：

- 第一行为扫描的本地文件路径，最右侧为打开文件按钮(需要注意的是，打开文件使用的当前系统的设置的默认应用，比如txt默认使用记事本打开，word等文件默认使用office打开等)
- 下面为针对这个文件扫描的结果，左侧为删除按钮，人工审查时可以删除误报的结果，第二部分为匹配结果所在的文件行数，第三部分为对应的匹配项(格式如：匹配规则名 -> 匹配的结果)

由于工具扫描存在一定误报，用户可以人工确认扫描结果是否准确，步骤如下：

- 点击打开文件按钮，打开对应的文件，根据文件行数定位到匹配项
- 确认是否为误报，为误报则点击删除按钮删除该匹配项

5. 导出结果

![image-20250615223759628](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615223759660.png)

支持用户自定义导出路径和文件名，默认导出路径为工具所在路径，默认导出文件名为scan_results，导出格式支持txt和pdf两种

- txt格式

![image-20250615223935920](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615223935946.png)

第一部分为扫描结果的统计结果，统计了每个扫描规则命中的数量，第二部分为具体的扫描结果

- pdf格式

![image-20250615224112675](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615224112703.png)

同txt格式，第一部分为统计结果

![image-20250615224147042](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250615224147070.png)

第二部分为具体的扫描结果

**值得一提的是：最终的导出结果是基于用户对页面操作后的结果，也就是说用户如果删除了误报结果，那么导出结果也不会包括误报结果**

---

## 📝 规则配置文件

所有扫描规则均以 JSON 格式存储在以下位置：

- `keywords.json` - 关键字匹配规则
- `sensitive_func.json` - 敏感函数匹配规则
- `vuln.json` - 漏洞模式匹配规则
- `regex.json` - 基础通用正则表达式

你可以根据需要自定义这些规则文件来扩展扫描能力。

---

### 添加自定义排除的文件后缀

编辑 `settings.py` 文件，添加自定义要排除的文件后缀

```python
# default exclude file suffiex
EXCLUDE_FILE_SUFFIEX = [
    # 图片文件
    "jpg", "jpeg", "png", "gif", "svg", "webp", "bmp", "tiff", "tif",
    # 样式表文件
    "css", "scss", "sass", "less",
    # 字体文件
    "ttf", "otf", "woff", "woff2", "eot",
    # 文档文件
    "html", "htm", "pdf", "csv", "doc", "docx", "xls", "xlsx",
    # 其他
    "ico", "mp4", "avi",
    ......
]
```

---

### 添加自定义强调的脚本文件

编辑 `settings.py` 文件，添加自定义的脚本文件后缀

```python
HIGHLIGHT_FILE_TYPES = [
    "js", "ts", "py", "java", "c",
    "cpp", "go", "rb", "php", "sh",
    "pl", "cs", "h", "hpp", "ps1",
    "bat", "lua"
    ......
]
```

添加后在gui界面会对它们进行红色标注强调

---

## 📤 导出报告

- **CLI 模式** ：结果默认输出到终端，也可通过 `-o` 参数保存为文本文件。
- **GUI 模式** ：点击 “保存结果” 按钮，可将结果保存为 `.txt` 或 `.pdf` 格式。

------

## 🧪 测试建议

- 在测试环境中运行，避免对生产系统造成影响。
- 可结合 Git 存储库进行历史提交扫描，查找可能泄露的敏感信息。
- 对于大型项目，推荐使用 GUI 界面查看详细结果。

---

## 📜 License

This project is licensed under the GNU General Public License v3.0 – see the [LICENSE](LICENSE) file for details.

This software uses code from [SecretFinder], which is also licensed under GPLv3.