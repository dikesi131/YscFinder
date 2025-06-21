# Portions of this code are derived from the original work:
# Copyright (C) 2020 m4ll0k(https://github.com/m4ll0k)

# Modified and extended by:
# Copyright (C) 2025 dikesi131(https://github.com/dikesi131)



import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QMessageBox,
    QComboBox, QProgressBar, QScrollArea
)
from PyQt6.QtCore import QCoreApplication, Qt
from typing import List, Dict
from io import StringIO
import contextlib
from core.show_file_type import ShowFileType
from core.export_report import YscPdfReport
from core.open_file import FileOpener
from ysc_finder import main as ysc_main
from settings import (__VERSION__, HIGHLIGHT_FILE_TYPES,
                      LIGHT_STYLE_SHEET, DARK_STYLE_SHEET,
                      TOOL_NAME)


class Args:
    def __init__(self):
        self.input = ""
        self.keyword_scan = False
        self.sensitive_function_scan = False
        self.vuln_scan = False
        self.output = "cli"
        self.exclude = ""
        self.only_type = ""


class YscFinderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{TOOL_NAME} GUI v{__VERSION__}")
        self.resize(800, 650)
        self.is_dark_mode = False
        self.init_ui()
        self.apply_stylesheet()

    def apply_stylesheet(self):
        style = self.get_dark_stylesheet() if self.is_dark_mode else self.get_light_stylesheet()  # noqa
        self.setStyleSheet(style)

    def get_light_stylesheet(self):
        return LIGHT_STYLE_SHEET

    def get_dark_stylesheet(self):
        return DARK_STYLE_SHEET

    def init_ui(self):
        ''' Initializes the user interface of the Tool GUI.
        '''
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 输入类型选择
        type_layout = QHBoxLayout()
        self.input_type = QComboBox()
        self.input_type.addItems(["目录", "文件"])
        type_layout.addWidget(QLabel("输入类型:"))
        type_layout.addWidget(self.input_type)
        layout.addLayout(type_layout)

        # 输入路径
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        input_btn = QPushButton("选择")
        input_btn.clicked.connect(self.choose_input)
        input_layout.addWidget(QLabel("输入路径:"))
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_btn)
        layout.addLayout(input_layout)

        # 扫描说明
        self.info_label = QLabel(
            "工具默认采用基于内容的正则匹配扫描, 以下为可选的扫描类别:"
        )
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # 扫描选项
        self.keyword_cb = QCheckBox("启用关键字扫描")
        self.sensitive_function_cb = QCheckBox("启用敏感函数扫描")
        self.vuln_scan_cb = QCheckBox("启用漏洞扫描")

        scan_options_layout = QHBoxLayout()
        scan_options_layout.addWidget(self.keyword_cb)
        scan_options_layout.addWidget(self.sensitive_function_cb)
        scan_options_layout.addWidget(self.vuln_scan_cb)
        scan_options_layout.setSpacing(20)
        scan_options_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(scan_options_layout)

        # 分析文件类型按钮
        show_types_btn = QPushButton("分析文件类型")
        show_types_btn.setStyleSheet("""
            QPushButton {
                background: #48bb78;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #38a169;
            }
        """)
        show_types_btn.clicked.connect(self.show_file_types)
        layout.addWidget(show_types_btn)

        # 文件类型展示
        self.file_types_label = QLabel()
        self.file_types_label.setWordWrap(True)
        layout.addWidget(self.file_types_label)

        # 仅扫描特定类型
        self.only_type_edit = QLineEdit()
        self.only_type_edit.setPlaceholderText("以;分隔文件类型, 例如: js;ts")
        only_type_layout = QHBoxLayout()
        only_type_layout.addWidget(QLabel("仅扫描特定类型:"))
        only_type_layout.addWidget(self.only_type_edit)
        layout.addLayout(only_type_layout)

        # 操作按钮
        run_btn = QPushButton("开始扫描")
        run_btn.clicked.connect(self.run_scan)
        save_btn = QPushButton("保存结果")
        save_btn.clicked.connect(self.save_result)
        layout.addWidget(run_btn)
        layout.addWidget(save_btn)

        # 主题切换按钮
        self.theme_toggle_btn = QPushButton("切换到暗色模式")
        self.theme_toggle_btn.setCheckable(True)
        self.theme_toggle_btn.setChecked(False)
        self.theme_toggle_btn.setStyleSheet("""
            QPushButton {
                background: #cbd5e0;
                color: #1a202c;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #94a3b8;
            }
        """)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_toggle_btn)

        # 结果展示区
        self.result_area = QScrollArea()
        self.result_area.setWidgetResizable(True)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.result_area.setWidget(self.result_widget)
        layout.addWidget(QLabel("扫描结果及操作："))
        layout.addWidget(self.result_area)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def toggle_theme(self):
        ''' Toggles the application theme between light and dark modes.
        '''
        self.is_dark_mode = not self.is_dark_mode
        self.apply_stylesheet()
        self.theme_toggle_btn.setText("切换到亮色模式" if self.is_dark_mode else "切换到暗色模式")  # noqa

    def show_file_types(self):
        ''' Displays the file types found in the input path.
        '''
        input_path = self.input_edit.text().strip()
        if not input_path:
            QMessageBox.warning(self, "提示", "请输入或选择输入路径")
            self.file_types_label.setText("")
            return
        file_types = ShowFileType(input_path).get_file_types()
        if not file_types:
            self.file_types_label.setText("未找到任何文件类型或该文件类型已被排除!")
            return
        highlight_types = set(HIGHLIGHT_FILE_TYPES)
        types_html = []
        for t in sorted(file_types):
            if t in highlight_types:
                types_html.append(f'<span style="color:red;font-weight:bold">{t}</span>')  # noqa
            else:
                types_html.append(t)
        html = "将要扫描的文件类型(红色标注的为常见的脚本文件): " + ", ".join(types_html)
        self.file_types_label.setTextFormat(Qt.TextFormat.RichText)
        self.file_types_label.setText(html)

    def save_result(self):
        ''' Saves the scan results to a file.
        '''
        scan_text = self._get_scan_text_from_result_layout()
        if not scan_text.strip():
            QMessageBox.warning(self, "提示", "没有可保存的扫描结果！")
            return
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "保存扫描结果",
            "scan_results.txt",
            "Text Files (*.txt);;PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            try:
                if selected_filter.startswith("Text"):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(scan_text)
                    QMessageBox.information(self, "保存成功",
                                            f"结果已保存到:\n{file_path}")
                elif selected_filter.startswith("PDF"):
                    lines = scan_text.splitlines()
                    pdf_report = YscPdfReport()
                    pdf_report.export_pdf_report(lines, file_path)
                    QMessageBox.information(self, "保存成功",
                                            f"PDF报告已保存到:\n{file_path}")
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(scan_text)
                    QMessageBox.information(self, "保存成功",
                                            f"结果已保存到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"保存文件时出错: {e}")

    def _get_scan_text_from_result_layout(self) -> str:
        ''' Extracts scan results from the result layout.
        This method iterates through the result layout, collecting text from each file block
        and its associated matches. It formats the results into a string that can be saved or displayed.

        Returns:
            str: A formatted string containing the scan results, including file URIs and matches.
        Raises:
            ValueError: If the result layout is empty or contains no matches.
        Raises:
            Exception: If an error occurs while processing the result layout.
        '''  # noqa
        lines = []
        current_file = None
        type_count: Dict[str, int] = {}
        for i in range(self.result_layout.count()):
            item = self.result_layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if isinstance(widget, QWidget):
                file_label = widget.findChild(QLabel, "file_label")
                if file_label:
                    if current_file is not None:
                        lines.append("")
                    lines.append(f"[ + ] URL: {file_label.text()}")
                    current_file = file_label.text()
                match_labels = widget.findChildren(QLabel, "match_label")
                for match_label in match_labels:
                    text = match_label.property("original_text")
                    if text:
                        lines.append(text)
                        if "\t->\t" in text:
                            type_name = text.split("\t->\t")[0].strip()
                            type_count[type_name] = type_count.get(type_name, 0) + 1  # noqa
        stat_lines = []
        if type_count:
            stat_lines.append("[ - ] Counts of keys")
            for k, v in sorted(type_count.items(), key=lambda x: x[1],
                               reverse=True):
                stat_lines.append(f"[ matched ] {k}: {v}")
            stat_lines.append("")
        return "\n".join(stat_lines + lines)

    def choose_input(self):
        ''' Opens a file or directory selection dialog based on the input type.
        This method checks the current input type selected in the combo box.
        '''
        if self.input_type.currentText() == "文件":
            files, _ = QFileDialog.getOpenFileNames(self, "选择文件")
            if files:
                self.input_edit.setText(";".join(files))
        else:
            dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
            if dir_path:
                self.input_edit.setText(dir_path)

    def show_scan_results(self, scan_result_text: str):
        ''' Displays the scan results in the results layout.
        This method processes the scan result text, extracting file URIs and matches,
        and populates the results layout with formatted rows for each file and its matches.
        It clears any previous results before displaying the new ones.
        If no matches are found, it displays a message indicating no results.
        This method is designed to handle the output format of the scan results,
        which typically includes lines starting with "[ + ] URL:" for file URIs
        and lines containing matches with a tab character ("\t") indicating the match details.
        It also handles the case where multiple matches are found for a single file,
        '''  # noqa
        for i in reversed(range(self.result_layout.count())):
            item = self.result_layout.takeAt(i)
            if item is not None:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        lines = scan_result_text.splitlines()
        current_file = None
        current_matches: list[str] = []
        file_count = 0
        for line in lines + [""]:
            line = line.strip()
            if line.startswith("[ + ] URL:"):
                if current_file is not None:
                    self._add_file_result_row(current_file, current_matches)
                    file_count += 1
                current_file = line.split(":", 1)[1].strip()
                current_matches = []
            elif line and "\t->\t" in line:
                current_matches.append(line)
            elif not line and current_file is not None:
                self._add_file_result_row(current_file, current_matches)
                file_count += 1
                current_file = None
                current_matches = []
        if file_count == 0:
            label = QLabel("无匹配结果")
            label.setStyleSheet("color: #888; font-size: 15px; padding: 20px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.result_layout.addWidget(label)

    def _add_file_result_row(self, file_uri: str, matches: List[str]):
        ''' Adds a file result row to the results layout.
        This method creates a block for a file with its URI and associated matches.
        It constructs a layout with a label for the file URI and buttons to open the file.
        Each match is displayed with a delete button to remove it from the results.

        Args:
            file_uri (str): The URI of the file being displayed.
            matches (List[str]): A list of matches found in the file.
        Raises:
            ValueError: If the file URI is empty or matches are not provided.
        '''  # noqa
        file_block = QWidget()
        file_block.setObjectName("file_block")
        file_block_layout = QVBoxLayout(file_block)
        file_block_layout.setContentsMargins(10, 10, 10, 10)
        file_block_layout.setSpacing(6)

        # 文件名 + 打开按钮
        file_row = QWidget()
        file_row_layout = QHBoxLayout(file_row)
        file_row_layout.setContentsMargins(0, 0, 0, 0)
        file_row_layout.setSpacing(10)

        label = QLabel(file_uri)
        label.setObjectName("file_label")
        label.setStyleSheet("font-weight: bold; color: #2d3748;")
        btn = QPushButton("打开文件")
        btn.setFixedWidth(90)
        btn.setStyleSheet("""
            QPushButton {
                background: #3182ce;
                color: white;
                border-radius: 4px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        btn.clicked.connect(lambda _,
                            uri=file_uri: FileOpener().open_file_by_uri(uri))
        file_row_layout.addWidget(label)
        file_row_layout.addStretch()
        file_row_layout.addWidget(btn)
        file_block_layout.addWidget(file_row)

        for match in matches:
            match_widget = QWidget()
            match_layout = QHBoxLayout(match_widget)
            match_layout.setContentsMargins(20, 2, 2, 2)
            match_layout.setSpacing(8)

            # 删除按钮
            del_btn = QPushButton("删除")
            del_btn.setFixedWidth(48)
            del_btn.setStyleSheet("""
                QPushButton {
                    background: #e53e3e;
                    color: white;
                    border-radius: 3px;
                    padding: 2px 8px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background: #c53030;
                }
            """)
            del_btn.clicked.connect(lambda _,
                                    w=match_widget: self._delete_match_row(w))

            # 解析匹配内容与行号
            m = re.match(r"^(.*?)\t->\t(.*)\(Line: (\d+)\)$", match.strip())
            if m:
                main_text = f"{m.group(1)} → {m.group(2)}"
                line_number = m.group(3) or ""
            else:
                main_text = match.strip()
                line_number = ""

            # 构造原始文本用于保存
            original_text = match.strip()

            # 匹配内容标签
            match_label = QLabel(main_text)
            match_label.setObjectName("match_label")
            match_label.setProperty("original_text", original_text)
            match_label.setWordWrap(True)
            match_label.setStyleSheet("""
                QLabel {
                    color: #374151;
                    background: #e0e7ef;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 13px;
                }
                QLabel:hover {
                    background: #c7d2fe;
                }
            """)

            # 行号标签
            line_label = QLabel(f"Line: {line_number}" if line_number else "")
            line_label.setStyleSheet("""
                QLabel {
                    color: #888;
                    font-size: 13px;
                    min-width: 60px;
                }
            """)
            line_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)  # noqa

            # 设置布局顺序：[删除] [空格] [行号] [空格] [匹配内容]
            match_layout.addWidget(del_btn)
            match_layout.addSpacing(5)
            match_layout.addWidget(line_label)
            match_layout.addSpacing(10)
            match_layout.addWidget(match_label, 1)

            match_widget.setLayout(match_layout)
            file_block_layout.addWidget(match_widget)

        file_block.setLayout(file_block_layout)
        self.result_layout.addWidget(file_block)

    def _delete_match_row(self, widget: QWidget):
        ''' Deletes a match row widget from the results layout.

        Args:
            widget (QWidget): The widget to be deleted, typically a match row.
        '''
        widget.setParent(None)
        widget.deleteLater()

    def run_scan(self):
        ''' Starts the scan based on user input and options.
        Validates input, sets up arguments, and calls the main scan function.
        Displays progress and results in the GUI.
        Raises:
            QMessageBox: If input is invalid or scan fails.
        Raises:
            Exception: If an error occurs during the scan.
        '''  # noqa
        args = Args()
        args.input = self.input_edit.text().strip()
        args.keyword_scan = self.keyword_cb.isChecked()
        args.sensitive_function_scan = self.sensitive_function_cb.isChecked()
        args.vuln_scan = self.vuln_scan_cb.isChecked()
        only_type_text = self.only_type_edit.text().strip()
        args.only_type = only_type_text if only_type_text else ""
        args.output = "cli"

        if not args.input:
            QMessageBox.warning(self, "提示", "请输入或选择输入路径")
            return

        self.progress_bar.setValue(0)

        def progress_callback(current, total):
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
            percent = int(current / total * 100) if total else 0
            self.progress_bar.setFormat(f"已完成 {current}/{total} ({percent}%)")
            QCoreApplication.processEvents()

        buffer = StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                ysc_main(args, progress_callback=progress_callback)
            result = buffer.getvalue()
            self.show_scan_results(result)
            self.progress_bar.setFormat("扫描完成")
            QMessageBox.information(self, "完成", "扫描完成！")
        except Exception as e:
            self.show_scan_results(str(e))
            self.progress_bar.setFormat("扫描出错")
            QMessageBox.critical(self, "错误", f"扫描出错: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YscFinderGUI()
    window.show()
    sys.exit(app.exec())
