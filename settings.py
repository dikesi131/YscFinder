__VERSION__ = "1.0"
KEYWORDS_FILE = "keywords.json"
BASIC_REGEX_FILE = "regex.json"
SENSITIVE_FUNC_FILE = "sensitive_func.json"
VULN_FILE = "vuln.json"
TOOL_NAME = "YscFinder"

# default exclude file suffiex
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

HIGHLIGHT_FILE_TYPES = [
    "js", "ts", "py", "java", "c",
    "cpp", "go", "rb", "php", "sh",
    "pl", "cs", "h", "hpp", "ps1",
    "bat", "lua"
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
       h1 {
          font-family: sans-serif;
       }
       a {
          color: #000;
       }
       .text {
          font-size: 16px;
          font-family: Helvetica, sans-serif;
          color: #323232;
          background-color: white;
       }
       .container {
          background-color: #e9e9e9;
          padding: 10px;
          margin: 10px 0;
          font-family: helvetica;
          font-size: 13px;
          border-width: 1px;
          border-style: solid;
          border-color: #8a8a8a;
          color: #323232;
          margin-bottom: 15px;
       }
       .button {
          padding: 17px 60px;
          margin: 10px 10px 10px 0;
          display: inline-block;
          background-color: #f4f4f4;
          border-radius: .25rem;
          text-decoration: none;
          -webkit-transition: .15s ease-in-out;
          transition: .15s ease-in-out;
          color: #333;
          position: relative;
       }
       .button:hover {
          background-color: #eee;
          text-decoration: none;
       }
       .github-icon {
          line-height: 0;
          position: absolute;
          top: 14px;
          left: 24px;
          opacity: 0.7;
       }
  </style>
  <title>LinkFinder Output</title>
</head>
<body contenteditable="true">
  $$content$$

</body>
</html>
'''

LIGHT_STYLE_SHEET = """
QWidget {
    background-color: #f9fafb;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: 14px;
    color: #2d3748;
}
QLabel {
    color: #2d3748;
}
QLineEdit, QComboBox {
    padding: 8px 12px;
    border: 1px solid #cbd5e0;
    border-radius: 6px;
    background: white;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #3182ce;
    outline: none;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #cbd5e0;
    background: white;
}
QCheckBox::indicator:checked {
    background: #3182ce;
    border: 2px solid #2563eb;
}
QPushButton {
    background: #3182ce;
    color: white;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background: #2563eb;
}
QPushButton:pressed {
    background: #1a56db;
}
QProgressBar {
    border: 1px solid #cbd5e0;
    border-radius: 6px;
    text-align: center;
    height: 24px;
    font-size: 13px;
}
QProgressBar::chunk {
    background-color: #3182ce;
    border-radius: 6px;
}
QScrollArea {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}
QWidget#file_block {
    border: 1px solid #b0b0b0;
    border-radius: 6px;
    background: #f8fafc;
    margin-bottom: 10px;
}
QLabel#match_label {
    color: #374151;
    background: #e0e7ef;
    border-radius: 3px;
    padding: 2px 6px;
}
QLabel#match_label:hover {
    background: #c7d2fe;
}
"""

DARK_STYLE_SHEET = """
QWidget {
    background-color: #1e293b;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: 14px;
    color: #e2e3e5;
}
QLabel {
    color: #e2e3e5;
}
QLineEdit, QComboBox {
    padding: 8px 12px;
    border: 1px solid #475569;
    border-radius: 6px;
    background: #334155;
    color: #f1f5f9;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #667eea;
    outline: none;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #475569;
    background: #334155;
}
QCheckBox::indicator:checked {
    background: #667eea;
    border: 2px solid #5a67d8;
}
QPushButton {
    background: #667eea;
    color: white;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background: #5a67d8;
}
QPushButton:pressed {
    background: #434fd9;
}
QProgressBar {
    border: 1px solid #475569;
    border-radius: 6px;
    text-align: center;
    height: 24px;
    font-size: 13px;
    color: #cbd5e0;
}
QProgressBar::chunk {
    background-color: #667eea;
    border-radius: 6px;
}
QScrollArea {
    background: #334155;
    border: 1px solid #475569;
    border-radius: 8px;
}
QWidget#file_block {
    border: 1px solid #475569;
    border-radius: 6px;
    background: #334155;
    margin-bottom: 10px;
}
QLabel#match_label {
    color: #f8fafc;
    background: #475569;
    border-radius: 3px;
    padding: 2px 6px;
}
QLabel#match_label:hover {
    background: #64748b;
}
"""
