from reportlab.lib.pagesizes import A4  # type: ignore
from reportlab.lib import colors  # type: ignore
from reportlab.platypus import (SimpleDocTemplate, Paragraph,  # type: ignore
                                Spacer, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore
from reportlab.pdfbase import pdfmetrics  # type: ignore
from reportlab.pdfbase.ttfonts import TTFont  # type: ignore
from typing import Any, List, Tuple
from settings import TOOL_NAME
import html
import os
import sys
import re


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


PAGE_WIDTH = A4[0] - 2 * 40  # 40pt 左右边距
FONT_NAME = "Microsoft-YaHei"
FONT_PATH = resource_path("core/fonts/Microsoft-YaHei.ttf")
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


class YscPdfReport:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        for style_name in self.styles.byName:
            self.styles[style_name].fontName = FONT_NAME
        # 单独设置标题和小标题为Helvetica
        self.styles['Title'].fontName = 'Helvetica'
        self.styles['Heading2'].fontName = 'Helvetica'

    def parse_scan_results(self, contents: List[str]) -> Tuple[List[Tuple[str, List[Any]]],  # noqa
                                                               List[List[str]]]:  # noqa
        ''' Parse the scan results from the given contents.
        Args:
            contents (List[str]): The lines of the scan results file.
        Returns:
            Tuple[List[Tuple[str, List[Any]]], List[List[str]]]: A tuple containing:
                - A list of tuples where each tuple contains a file path and a list of matches.
                - A list of statistics where each entry is a list containing the type and hit count.
        '''  # noqa

        files_and_matches = []
        stats = []
        current_file = None
        current_matches: List[Any] = []
        section = 0  # 0: files, 1: matches, 2: stats

        for line in contents:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[ + ] URL:"):
                if current_file is not None:
                    files_and_matches.append((current_file, current_matches))
                current_file = line.replace("[ + ] URL: ", "")
                current_matches = []
                section = 1
            elif line.startswith("[ - ] Counts of keys"):
                if current_file is not None:
                    files_and_matches.append((current_file, current_matches))
                section = 2
            elif section == 1 and "\t->\t" in line:
                m = re.match(r"(.+?)\t->\t(.+?)\t\(Line: (\d+)\)", line)
                if m:
                    current_matches.append([m.group(1), m.group(2),
                                            m.group(3)])
            elif section == 2 and line.startswith("[ matched ]"):
                m = re.match(r"\[ matched \] (.*?): (\d+)", line)
                if m:
                    stats.append([m.group(1), m.group(2)])

        if current_file is not None and (current_file, current_matches) not in files_and_matches:  # noqa
            files_and_matches.append((current_file, current_matches))

        return files_and_matches, stats

    def export_pdf_report(self, results: List[str], pdf_file: str):
        ''' Export the scan results to a PDF file.

        Args:
            results (List[str]): The lines of the scan results file.
            pdf_file (str): The path to save the PDF report.
        '''
        files_and_matches, stats = self.parse_scan_results(results)
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        story = []

        # Title
        story.append(Paragraph(f"{TOOL_NAME} Scan Report",
                               self.styles['Title']))
        story.append(Spacer(1, 18))

        # 1. 统计部分
        story.append(Paragraph("1. Sensitive Information Type Statistics",
                               self.styles['Heading2']))
        if stats:
            stat_table = [["Type", "Hit Count"]]
            stat_table.extend(stats)
            table = Table(stat_table, repeatRows=1, colWidths=[200, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke,
                                                      colors.lightgrey]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No statistics data.",
                                   self.styles['Normal']))
        story.append(Spacer(1, 12))

        # 2. 按文件分组展示匹配项
        idx = 1
        story.append(Paragraph("2. Scan Results by File",
                               self.styles['Heading2']))
        if files_and_matches:
            for file_path, matches in files_and_matches:
                if matches:
                    story.append(Paragraph(f"{idx}. <b>{html.escape(file_path)}</b>",  # noqa
                                           self.styles['Heading3']))
                    table_data = [["Type", "Content", "Line"]]
                    for row in matches:
                        table_data.append([
                            Paragraph(html.escape(row[0]),
                                      self.styles['Normal']),
                            Paragraph(html.escape(row[1]),
                                      self.styles['Normal']),
                            row[2]
                        ])  # type: ignore
                    table = Table(table_data, repeatRows=1,
                                  colWidths=[80, PAGE_WIDTH-160, 60])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
                        ('FONTSIZE', (0, 0), (-1, 0), 11),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                         [colors.whitesmoke, colors.lightgrey]),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ]))
                    story.append(table)
                    idx += 1

                # add a spacer after each file section
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph("No scanned files.", self.styles['Normal']))
        story.append(Spacer(1, 12))

        doc.build(story)
