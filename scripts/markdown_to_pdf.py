#!/usr/bin/env python3
"""
Convert a Markdown report into a clean PDF.

Usage:
    python scripts/markdown_to_pdf.py input.md output.pdf

This script intentionally supports the Markdown patterns used by the daily
market report:
- headings
- paragraphs
- bullet lists
- simple Markdown tables
- fenced code blocks
- horizontal rules

Dependency:
    reportlab
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Preformatted,
)


def clean_inline(text: str) -> str:
    """Convert small Markdown inline formatting to safe ReportLab text."""
    text = html.escape(text.strip())

    # Inline code
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)

    # Bold and italic
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)

    return text


def is_table_start(lines: List[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False

    header = lines[index].strip()
    separator = lines[index + 1].strip()

    if "|" not in header or "|" not in separator:
        return False

    separator_cells = [c.strip() for c in separator.strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in separator_cells)


def parse_table(lines: List[str], start: int):
    table_lines = []
    index = start

    while index < len(lines) and "|" in lines[index]:
        table_lines.append(lines[index].strip())
        index += 1

    # Remove separator row
    rows = []
    for i, line in enumerate(table_lines):
        if i == 1:
            continue
        cells = [clean_inline(c) for c in line.strip("|").split("|")]
        rows.append(cells)

    max_cols = max(len(row) for row in rows) if rows else 0
    for row in rows:
        while len(row) < max_cols:
            row.append("")

    return rows, index


def build_pdf(markdown_path: Path, pdf_path: Path) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            spaceAfter=12,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="H1Custom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            spaceBefore=12,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="H2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.5,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.5,
            leftIndent=14,
            firstLineIndent=-9,
            spaceAfter=3,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9,
        )
    )

    story = []
    i = 0
    in_code = False
    code_buffer = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buffer = []
            else:
                in_code = False
                if code_buffer:
                    story.append(Preformatted("\n".join(code_buffer), styles["Code"]))
                    story.append(Spacer(1, 6))
            i += 1
            continue

        if in_code:
            code_buffer.append(raw)
            i += 1
            continue

        if not line.strip():
            story.append(Spacer(1, 4))
            i += 1
            continue

        if line.strip() in {"---", "***", "___"}:
            story.append(Spacer(1, 8))
            i += 1
            continue

        if is_table_start(lines, i):
            rows, next_index = parse_table(lines, i)

            table_data = []
            for row in rows:
                table_data.append([Paragraph(cell, styles["SmallCustom"]) for cell in row])

            col_count = len(table_data[0]) if table_data else 1
            available_width = letter[0] - doc.leftMargin - doc.rightMargin
            col_widths = [available_width / col_count] * col_count

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 7),
                        ("LEADING", (0, 0), (-1, -1), 8.5),
                        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 8))
            i = next_index
            continue

        if line.startswith("# "):
            story.append(Paragraph(clean_inline(line[2:]), styles["ReportTitle"]))
            i += 1
            continue

        if line.startswith("## "):
            story.append(Paragraph(clean_inline(line[3:]), styles["H1Custom"]))
            i += 1
            continue

        if line.startswith("### "):
            story.append(Paragraph(clean_inline(line[4:]), styles["H2Custom"]))
            i += 1
            continue

        bullet_match = re.match(r"^(\s*)[-*]\s+(.+)$", line)
        numbered_match = re.match(r"^(\s*)\d+\.\s+(.+)$", line)

        if bullet_match:
            story.append(Paragraph("• " + clean_inline(bullet_match.group(2)), styles["BulletCustom"]))
            i += 1
            continue

        if numbered_match:
            story.append(Paragraph("• " + clean_inline(numbered_match.group(2)), styles["BulletCustom"]))
            i += 1
            continue

        story.append(Paragraph(clean_inline(line), styles["BodyCustom"]))
        i += 1

    doc.build(story)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/markdown_to_pdf.py input.md output.pdf", file=sys.stderr)
        return 2

    markdown_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])

    if not markdown_path.exists():
        print(f"Input file not found: {markdown_path}", file=sys.stderr)
        return 1

    try:
        build_pdf(markdown_path, pdf_path)
    except Exception as exc:
        print(f"PDF generation failed: {exc}", file=sys.stderr)
        return 1

    print(f"PDF created: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
