"""
Generate professional PDF version of the Complete Technical Handover Document.
Target: docs/PROJECT_TECHNICAL_HANDOVER.pdf
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 45
MARGIN_Y = 40
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN_X


class HandoverNumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page count and headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Subtle border on cover page
            self.saveState()
            self.setStrokeColor(colors.HexColor("#1F2937"))
            self.setLineWidth(1.5)
            self.rect(30, 30, PAGE_WIDTH - 60, PAGE_HEIGHT - 60)
            self.setStrokeColor(colors.HexColor("#9CA3AF"))
            self.setLineWidth(0.5)
            self.rect(34, 34, PAGE_WIDTH - 68, PAGE_HEIGHT - 68)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))

        # Running Header
        self.drawString(MARGIN_X, PAGE_HEIGHT - 28, "DATA STREAM ANALYTICS - COMPLETE TECHNICAL HANDOVER")
        self.drawRightString(PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 28, "GROUP NO: 3")
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(MARGIN_X, PAGE_HEIGHT - 32, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 32)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(MARGIN_X, 32, PAGE_WIDTH - MARGIN_X, 32)
        self.drawString(MARGIN_X, 22, "REAL-TIME IoT SENSOR STREAMING ANALYTICS & ANOMALY DETECTION")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(PAGE_WIDTH - MARGIN_X, 22, page_text)
        self.restoreState()


def build_handover_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_Y,
        bottomMargin=MARGIN_Y,
    )

    styles = getSampleStyleSheet()

    c_black = colors.HexColor("#111827")
    c_dark_gray = colors.HexColor("#1F2937")
    c_text = colors.HexColor("#2B3441")
    c_border = colors.HexColor("#CBD5E1")
    c_bg_light = colors.HexColor("#F8FAFC")
    c_bg_code = colors.HexColor("#F1F5F9")

    # Typography
    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13.5, leading=17,
        textColor=c_dark_gray, spaceBefore=12, spaceAfter=5, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10.8, leading=14.5,
        textColor=c_dark_gray, spaceBefore=9, spaceAfter=3.5, keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=9.6, leading=13,
        textColor=c_dark_gray, spaceBefore=7, spaceAfter=2.5, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9.0, leading=13.0,
        textColor=c_text, spaceAfter=4.5
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=c_text, leftIndent=12, firstLineIndent=-8, spaceAfter=3.0
    )
    code_style = ParagraphStyle(
        'Code', parent=styles['Normal'], fontName='Courier', fontSize=7.8, leading=10.5,
        textColor=colors.HexColor("#1E293B"), spaceAfter=4.0
    )
    caption_style = ParagraphStyle(
        'Caption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.2, leading=11,
        alignment=1, textColor=colors.HexColor("#4B5563"), spaceBefore=3, spaceAfter=5
    )
    th_style = ParagraphStyle(
        'TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.2, leading=10.8,
        alignment=1, textColor=colors.white
    )
    tc_style = ParagraphStyle(
        'TC', parent=styles['Normal'], fontName='Helvetica', fontSize=8.0, leading=10.8,
        textColor=c_text
    )
    tc_bold = ParagraphStyle(
        'TC_Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.0, leading=10.8,
        textColor=c_black
    )
    tc_center = ParagraphStyle(
        'TC_Center', parent=styles['Normal'], fontName='Helvetica', fontSize=8.0, leading=10.8,
        alignment=1, textColor=c_text
    )

    def make_table(data, widths, align='CENTER', pad=3.5):
        t = Table(data, colWidths=widths, hAlign=align)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_dark_gray),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), pad),
            ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ]))
        return t

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 55))
    story.append(Paragraph("DATA STREAM ANALYTICS", ParagraphStyle(
        'CP_Course', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=19,
        alignment=1, textColor=c_dark_gray, spaceAfter=4
    )))
    story.append(Paragraph("DSA MINI PROJECT - COMPREHENSIVE TECHNICAL HANDOVER", ParagraphStyle(
        'CP_Type', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15,
        alignment=1, textColor=colors.HexColor("#4B5563"), spaceAfter=18
    )))

    story.append(HRFlowable(width="65%", thickness=1.5, color=c_dark_gray, spaceAfter=20, spaceBefore=0))

    story.append(Paragraph("REAL-TIME IoT SENSOR STREAMING ANALYTICS<br/>AND ANOMALY DETECTION SYSTEM", ParagraphStyle(
        'CP_Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=19, leading=25,
        alignment=1, textColor=c_black, spaceAfter=14
    )))
    story.append(Paragraph("Full Architecture, Source Code Analysis, DSA Guarantees, ML Model, and Viva Guide", ParagraphStyle(
        'CP_Sub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, leading=14,
        alignment=1, textColor=colors.HexColor("#4B5563"), spaceAfter=18
    )))

    story.append(HRFlowable(width="45%", thickness=0.8, color=colors.HexColor("#6B7280"), spaceAfter=22, spaceBefore=2))

    story.append(Paragraph("GROUP NO: 3", ParagraphStyle(
        'CP_Grp', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16,
        alignment=1, textColor=c_dark_gray, spaceAfter=8
    )))

    members_data = [
        [Paragraph("<b>USN</b>", th_style), Paragraph("<b>STUDENT NAME</b>", th_style)],
        [Paragraph("23BTRCL227", tc_center), Paragraph("P CHETHAN", tc_center)],
        [Paragraph("23BTRCL217", tc_center), Paragraph("MUKKAMALLA LOKESHWAR REDDY", tc_center)],
        [Paragraph("23BTRCL221", tc_center), Paragraph("NADAKUDURU SRINIVAS", tc_center)],
        [Paragraph("23BTRCL233", tc_center), Paragraph("SOMISETTY JAGANNADA KAILASH", tc_center)],
    ]
    story.append(make_table(members_data, [155, 245], pad=5))

    story.append(Spacer(1, 40))

    story.append(Paragraph("SUBMITTED TO:", ParagraphStyle(
        'CP_SubHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        alignment=1, textColor=c_dark_gray, spaceAfter=4
    )))
    story.append(Paragraph("DR. ARCHANA SASI", ParagraphStyle(
        'CP_Faculty', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=17,
        alignment=1, textColor=c_black, spaceAfter=3
    )))
    story.append(Paragraph("Course Coordinator / Faculty, Data Stream Analytics", ParagraphStyle(
        'CP_Dept', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5,
        alignment=1, textColor=colors.HexColor("#4B5563"), spaceAfter=38
    )))

    story.append(Paragraph(
        "Complete Technical Specification & Code-Verified Handover Guide<br/>"
        "for Developers, Faculty Review, and Viva Voce Examination",
        ParagraphStyle(
            'CP_Note', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14,
            alignment=1, textColor=colors.HexColor("#4B5563")
        )
    ))

    story.append(PageBreak())

    # Read and parse Markdown handover file into structured report sections
    md_path = os.path.join(os.path.dirname(__file__), "..", "docs", "PROJECT_TECHNICAL_HANDOVER.md")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    lines = md_text.splitlines()
    in_code_block = False
    code_buffer = []
    in_table = False
    table_rows = []

    # Skip title and metadata at the very beginning of the MD since we have a dedicated cover page
    start_parsing = False

    for line in lines:
        stripped = line.strip()

        if "# PART 1 — COMPLETE PROJECT INVENTORY" in line:
            start_parsing = True

        if not start_parsing:
            continue

        # Code blocks
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_text = "<br/>".join(code_buffer)
                story.append(Table([[Paragraph(code_text, code_style)]], colWidths=[USABLE_WIDTH],
                                   style=[('BACKGROUND', (0,0), (-1,-1), c_bg_code),
                                          ('BOX', (0,0), (-1,-1), 0.5, c_border),
                                          ('TOPPADDING', (0,0), (-1,-1), 4),
                                          ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
                story.append(Spacer(1, 4))
                code_buffer = []
            else:
                in_code_block = True
                code_buffer = []
            continue

        if in_code_block:
            safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
            code_buffer.append(safe_line)
            continue

        # Tables in Markdown
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue  # separator row
            table_rows.append(cells)
            in_table = True
            continue
        elif in_table:
            in_table = False
            if table_rows:
                num_cols = len(table_rows[0])
                col_w = USABLE_WIDTH / num_cols
                t_data = []
                for r_idx, row in enumerate(table_rows):
                    row_data = []
                    for c in row:
                        if r_idx == 0:
                            row_data.append(Paragraph(f"<b>{c}</b>", th_style))
                        else:
                            row_data.append(Paragraph(c, tc_style))
                    t_data.append(row_data)
                story.append(make_table(t_data, [col_w] * num_cols))
                story.append(Spacer(1, 5))
                table_rows = []

        if not stripped:
            continue

        # Headings
        if stripped.startswith("# PART "):
            story.append(Spacer(1, 8))
            clean_h1 = stripped.lstrip("#").strip()
            story.append(Paragraph(clean_h1, h1_style))
            story.append(HRFlowable(width="100%", thickness=1.0, color=c_dark_gray, spaceAfter=6, spaceBefore=1))
        elif stripped.startswith("### "):
            clean_h2 = stripped.lstrip("#").strip()
            story.append(Paragraph(clean_h2, h2_style))
        elif stripped.startswith("#### "):
            clean_h3 = stripped.lstrip("#").strip()
            story.append(Paragraph(clean_h3, h3_style))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = stripped[2:].strip()
            story.append(Paragraph(f"&bull; {bullet_text}", bullet_style))
        elif stripped.startswith("> "):
            quote_text = stripped[2:].strip()
            story.append(Paragraph(f"<i>{quote_text}</i>", body_style))
        else:
            story.append(Paragraph(stripped, body_style))

    # Flush any remaining table
    if table_rows:
        num_cols = len(table_rows[0])
        col_w = USABLE_WIDTH / num_cols
        t_data = []
        for r_idx, row in enumerate(table_rows):
            row_data = []
            for c in row:
                if r_idx == 0:
                    row_data.append(Paragraph(f"<b>{c}</b>", th_style))
                else:
                    row_data.append(Paragraph(c, tc_style))
            t_data.append(row_data)
        story.append(make_table(t_data, [col_w] * num_cols))
        story.append(Spacer(1, 5))

    doc.build(story, canvasmaker=HandoverNumberedCanvas)
    print(f"Technical handover PDF successfully compiled to: {output_path}")


if __name__ == "__main__":
    out_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "PROJECT_TECHNICAL_HANDOVER.pdf"))
    build_handover_pdf(out_pdf)
