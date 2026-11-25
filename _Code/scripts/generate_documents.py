"""
Document Generation Script
Generates the four mandatory project PDFs:
1. Storyboard.pdf
2. Narration_Script.pdf
3. Code_Walkthrough.pdf
4. Viva_Prep.pdf

Using ReportLab with clean academic styling, professional color palette,
headers, footers, and structured tables.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Colors
C_PRIMARY = colors.HexColor("#0F172A")    # Deep Navy
C_SECONDARY = colors.HexColor("#0284C7")  # Cyan / Blue
C_ACCENT = colors.HexColor("#D97706")     # Amber / Gold
C_DARK = colors.HexColor("#1E293B")       # Slate Dark
C_LIGHT = colors.HexColor("#F8FAFC")      # Off White
C_MUTED = colors.HexColor("#64748B")      # Muted Slate
C_ROW1 = colors.HexColor("#2563EB")       # Blue
C_ROW2 = colors.HexColor("#059669")       # Green
C_ROW3 = colors.HexColor("#EA580C")       # Orange
C_BORDER = colors.HexColor("#CBD5E1")     # Border Gray

class NumberedCanvas(canvas.Canvas):
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
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(C_MUTED)
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "M3 Internal Assessment — Gaussian Elimination (3x3 System)")
            self.drawRightString(558, 750, "Arjav Jain (E25B070861)")
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Linear Algebra and Calculus (M3) • Batch: Ramanujan")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_base_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=C_PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=C_PRIMARY,
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_SECONDARY,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_DARK,
        spaceAfter=6
    )

    bold_body = ParagraphStyle(
        'BoldBody_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=C_DARK
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=C_MUTED
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_PRIMARY
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=C_PRIMARY
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'h1': h1_style,
        'h2': h2_style,
        'body': body_style,
        'bold': bold_body,
        'code': code_style,
        'meta_label': meta_label,
        'meta_val': meta_val,
        'callout': callout_style
    }

def build_metadata_header(styles, doc_name):
    elements = []
    elements.append(Paragraph(doc_name, styles['title']))
    elements.append(Paragraph("Mathematics 3 Internal Assessment — Animation Video Project", styles['subtitle']))

    meta_data = [
        [Paragraph("Student Name:", styles['meta_label']), Paragraph("Arjav Jain", styles['meta_val']),
         Paragraph("Student ID:", styles['meta_label']), Paragraph("E25B070861", styles['meta_val'])],
        [Paragraph("Subject:", styles['meta_label']), Paragraph("Mathematics 3 – Linear Algebra & Calculus", styles['meta_val']),
         Paragraph("Batch:", styles['meta_label']), Paragraph("Ramanujan", styles['meta_val'])],
        [Paragraph("Topic:", styles['meta_label']), Paragraph("Gaussian Elimination: Solving a 3×3 System", styles['meta_val']),
         Paragraph("Target Duration:", styles['meta_label']), Paragraph("~5 Minutes (Strictly ≤ 7 min)", styles['meta_val'])]
    ]
    meta_table = Table(meta_data, colWidths=[80, 180, 70, 174])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 10))
    return elements

# =========================================================================
# 1. STORYBOARD PDF
# =========================================================================
def generate_storyboard_pdf():
    pdf_path = os.path.join(PROJECT_ROOT, "Storyboard.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = create_base_styles()
    story = []

    story.extend(build_metadata_header(styles, "Official Project Storyboard"))

    # Learning Objective Callout Box
    lo_title = Paragraph("<b>CORE LEARNING OBJECTIVE (MANDATORY):</b>", styles['bold'])
    lo_text = Paragraph(
        "\"By the end of this video, the viewer will be able to explain how Gaussian elimination uses "
        "row operations to reduce a 3×3 system to row echelon form, why those operations do not change "
        "the solution set, and what the solution means geometrically.\"",
        styles['callout']
    )
    lo_box = Table([[lo_title], [lo_text]], colWidths=[504])
    lo_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, C_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(lo_box)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Six-Scene Storyboard Matrix", styles['h1']))
    story.append(Paragraph("Structured sequence following the official M3 Animation Video Assessment guidelines:", styles['body']))

    table_data = [
        [
            Paragraph("<b>Scene</b>", styles['bold']),
            Paragraph("<b>Purpose</b>", styles['bold']),
            Paragraph("<b>Visuals & Animations</b>", styles['bold']),
            Paragraph("<b>Narration Summary</b>", styles['bold']),
            Paragraph("<b>Mathematics Covered</b>", styles['bold']),
            Paragraph("<b>Duration</b>", styles['bold'])
        ],
        [
            Paragraph("<b>1. Hook / Context</b>", styles['body']),
            Paragraph("Motivate the problem and introduce academic credentials.", styles['body']),
            Paragraph("Title card with student credentials; sequential reveal of 3 simultaneous equations; tangled trial-and-error arrows; glowing reveal of Gaussian Elimination.", styles['body']),
            Paragraph("Welcome and introduction; presentation of the 3-equation system; failure of informal trial/error; motivation for a systematic algorithm.", styles['body']),
            Paragraph("System setup:<br/>x + y + z = 6<br/>2x + 3y + z = 11<br/>x + 2y + 3z = 14", styles['code']),
            Paragraph("34.50s<br/><i>(Audio: 34.23s)</i>", styles['body'])
        ],
        [
            Paragraph("<b>2. Concept Introduction</b>", styles['body']),
            Paragraph("Establish matrix notation and elementary row operations.", styles['body']),
            Paragraph("Compact matrix equation Ax = b; side-by-side [A|b] augmented matrix; learning objective banner; cards detailing the 3 row operations.", styles['body']),
            Paragraph("Defining A, x, and b; forming the augmented matrix; reciting learning objective; explaining row swaps, scaling, and replacement; proving reversibility.", styles['body']),
            Paragraph("Ax = b representation;<br/>Augmented matrix [A|b];<br/>Three elementary row operations;<br/>Row Echelon Form criteria.", styles['body']),
            Paragraph("46.50s<br/><i>(Audio: 46.21s)</i>", styles['body'])
        ],
        [
            Paragraph("<b>3. Visual Intuition</b>", styles['body']),
            Paragraph("Bridge algebra to 3D geometry.", styles['body']),
            Paragraph("ThreeDAxes with labelled X,Y,Z; three semi-transparent colored planes (Blue, Green, Orange); golden sphere at (1,2,3); 360° camera orbit; plane tilt transformation.", styles['body']),
            Paragraph("Each linear equation is an infinite flat plane; two planes intersect in a line; all three intersect at (1,2,3); why linear combinations preserve intersection line.", styles['body']),
            Paragraph("Plane 1: x+y+z=6<br/>Plane 2: 2x+3y+z=11<br/>Plane 3: x+2y+3z=14<br/>Unique point: (1, 2, 3)", styles['code']),
            Paragraph("41.30s<br/><i>(Audio: 41.01s)</i>", styles['body'])
        ],
        [
            Paragraph("<b>4. Worked Example</b>", styles['body']),
            Paragraph("Execute complete Gaussian elimination step by step.", styles['body']),
            Paragraph("Augmented matrix with colored rows; side arithmetic calculations; in-place entry animations; yellow pivot boxes; echelon staircase; back substitution callouts.", styles['body']),
            Paragraph("Walking through R2->R2-2R1, R3->R3-R1, and R3->R3-R2; identifying pivots 1, 1, 3; explaining REF; back substitution solving for z=3, y=2, x=1.", styles['body']),
            Paragraph("Op 1: R2→R2−2R1<br/>Op 2: R3→R3−R1<br/>Op 3: R3→R3−R2<br/>Pivots: 1, 1, 3<br/>z=3, y=2, x=1", styles['code']),
            Paragraph("84.80s<br/><i>(Audio: 84.50s)</i>", styles['body'])
        ],
        [
            Paragraph("<b>5. Interpretation</b>", styles['body']),
            Paragraph("Verify solution and analyze special cases.", styles['body']),
            Paragraph("Direct substitution into all 3 original equations with animated green checkmarks; side-by-side comparison cards for inconsistent vs dependent systems.", styles['body']),
            Paragraph("Verifying 6=6, 11=11, 14=14; confirming point (1,2,3) lies on all planes; explaining 0=5 contradiction (no solution) and 0=0 free variables (infinite solutions).", styles['body']),
            Paragraph("Eq 1: 6 = 6 ✓<br/>Eq 2: 11 = 11 ✓<br/>Eq 3: 14 = 14 ✓<br/>[0 0 0 | 5] → 0 = 5 (No sol)<br/>[0 0 0 | 0] → 0 = 0 (Inf sol)", styles['code']),
            Paragraph("55.30s<br/><i>(Audio: 55.10s)</i>", styles['body'])
        ],
        [
            Paragraph("<b>6. Summary & Credits</b>", styles['body']),
            Paragraph("Reinforce takeaways, cite sources, and conclude.", styles['body']),
            Paragraph("Three takeaway cards with bullet points; final solution banner; academic citations; AI tool disclosure card; closing academic thank you card.", styles['body']),
            Paragraph("Recapping algorithmic reduction, preservation of solutions, and back substitution; acknowledging Strang, Lay, and Manim; disclosing Antigravity and human voiceover; final sign-off.", styles['body']),
            Paragraph("Key takeaways 1, 2, 3;<br/>Solution: (1, 2, 3);<br/>NumPy verification;<br/>Full academic citations.", styles['body']),
            Paragraph("54.20s<br/><i>(Audio: 53.92s)</i>", styles['body'])
        ]
    ]

    sb_table = Table(table_data, colWidths=[65, 75, 115, 115, 85, 49])
    sb_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(sb_table)
    story.append(Spacer(1, 10))

    # Total Duration Summary Table
    total_summary = [
        [Paragraph("<b>Calibrated Scene Duration</b>", styles['bold']), Paragraph("<b>316.60s (5 min 16.60s)</b> — Sum of 6 calibrated visual scenes", styles['body'])],
        [Paragraph("<b>Total Spoken Audio</b>", styles['bold']), Paragraph("<b>314.96s (5 min 14.96s)</b> — Total human speech duration across 6 scenes", styles['body'])],
        [Paragraph("<b>Final MP4 Video Duration</b>", styles['bold']), Paragraph("<b>316.63s (5 min 16.63s)</b> — Within strict ~5 min recommendation & < 7-min ceiling", styles['body'])],
        [Paragraph("<b>Resolution & Codec</b>", styles['bold']), Paragraph("1080p (1920×1080), 30 FPS, H.264 Video, AAC Audio, 16:9 Landscape", styles['body'])],
        [Paragraph("<b>Voice Narration</b>", styles['bold']), Paragraph("Original Human Voiceover by Arjav Jain — EBU R128 loudness standardized", styles['body'])]
    ]
    summary_table = Table(total_summary, colWidths=[150, 354])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.8, C_SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(summary_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("-> Generated Storyboard.pdf")

# =========================================================================
# 2. NARRATION SCRIPT PDF
# =========================================================================
def generate_narration_script_pdf():
    pdf_path = os.path.join(PROJECT_ROOT, "Narration_Script.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = create_base_styles()
    story = []

    story.extend(build_metadata_header(styles, "Official Narration Script"))

    overview_p = Paragraph(
        "<b>Voice Specification:</b> Original human voice recording by Arjav Jain (Student ID: E25B070861, Batch: Ramanujan)<br/>"
        "<b>Audio Format & Pacing:</b> Standardized 44.1 kHz 16-bit mono PCM WAV, gentle EBU R128 loudness normalization "
        "(integrated -18 LUFS, -1.5 dB true peak headroom). Total spoken voice duration: 314.96 seconds (5m 14.96s).<br/>"
        "<b>Video Synchronization:</b> Scene animations are calibrated directly to 316.60 seconds total, resulting in an exact "
        "final MP4 video duration of 316.63 seconds (5m 16.63s).",
        styles['body']
    )
    story.append(overview_p)
    story.append(Spacer(1, 8))

    scenes_data = [
        ("Scene 1: Hook and Context + Opening Credentials", "34.23s (Scene: 34.50s)", 68,
         "Opening title card displays student credentials. Equations appear sequentially. Central question posed.",
         "Welcome to this Mathematics 3 assessment on Gaussian Elimination, presented by Arjav Jain, Student ID E25B070861, from the Ramanujan batch.\n\n"
         "Consider this system of three simultaneous equations: x plus y plus z equals 6, 2x plus 3y plus z equals 11, and x plus 2y plus 3z equals 14.\n\n"
         "Solving by trial and error or repeated substitution quickly becomes tangled.\n\n"
         "Is there a systematic method to solve all three equations efficiently?\n\n"
         "The answer is Gaussian Elimination."),

        ("Scene 2: Concept Introduction & Matrix Formulation", "46.21s (Scene: 46.50s)", 112,
         "Matrix equation Ax = b. Augmented matrix [A|b]. Learning objective box. Three row operation cards.",
         "We represent our linear system compactly as A x equals b, where A is the coefficient matrix, x is the variable vector, and b is the constant vector. Combining them forms the augmented matrix.\n\n"
         "Our learning objective: By the end of this video, the viewer will be able to explain how Gaussian elimination uses row operations to reduce a 3 by 3 system to row echelon form, why those operations do not change the solution set, and what the solution means geometrically.\n\n"
         "We use three elementary row operations: row swap, row scaling, and row replacement.\n\n"
         "Because each operation is reversible, they strictly preserve the solution set.\n\n"
         "Our goal is Row Echelon Form: a staircase pattern where leading pivots advance to the right, with zeros everywhere below."),

        ("Scene 3: Visual Intuition & 3D Geometry", "41.01s (Scene: 41.30s)", 108,
         "ThreeDAxes with blue, green, orange planes. Golden sphere at (1,2,3). Orbiting 3D camera. Plane tilt card.",
         "In three dimensions, each linear equation represents a plane.\n\n"
         "The blue plane is x plus y plus z equals 6.\n\n"
         "The green plane is 2x plus 3y plus z equals 11.\n\n"
         "And the orange plane is x plus 2y plus 3z equals 14.\n\n"
         "Two non-parallel planes intersect along a line. When the third plane crosses that line, all three meet at a single point: (1, 2, 3). This is our unique solution.\n\n"
         "Why do row operations preserve this solution?\n\n"
         "Adding a multiple of one row to another replaces a plane with a linear combination. The plane tilts, but it still passes through the common intersection line.\n\n"
         "Row operations simplify our view without altering where the planes intersect."),

        ("Scene 4: Worked Example — Step-by-Step Row Elimination", "84.50s (Scene: 84.80s)", 205,
         "Augmented matrix [A|b]. In-place entry morphing. Side arithmetic cards. Yellow pivot boxes. Staircase. Back substitution.",
         "Let us execute Gaussian elimination.\n\n"
         "We begin with the augmented matrix: Row 1 is [1, 1, 1 | 6], Row 2 is [2, 3, 1 | 11], and Row 3 is [1, 2, 3 | 14].\n\n"
         "Our first pivot is 1 in row 1.\n\n"
         "Operation 1: R2 becomes R2 minus 2 R1.\n"
         "[2, 3, 1 | 11] minus 2 times [1, 1, 1 | 6] equals [0, 1, minus 1 | minus 1].\n\n"
         "Operation 2: R3 becomes R3 minus R1.\n"
         "[1, 2, 3 | 14] minus [1, 1, 1 | 6] equals [0, 1, 2 | 8]. Column 1 is cleared.\n\n"
         "Now, row 2 pivot is 1.\n\n"
         "Operation 3: R3 becomes R3 minus R2.\n"
         "[0, 1, 2 | 8] minus [0, 1, minus 1 | minus 1] equals [0, 0, 3 | 9].\n\n"
         "The matrix is in Row Echelon Form! The three pivots are 1, 1, and 3, highlighted along the staircase.\n\n"
         "Now, back substitution.\n\n"
         "Row 3 gives: 3z equals 9, so z equals 3.\n\n"
         "Row 2 gives: y minus z equals minus 1. Substituting z equals 3 gives y equals 2.\n\n"
         "Row 1 gives: x plus y plus z equals 6. Substituting y and z gives x equals 1.\n\n"
         "Our final solution is (1, 2, 3)."),

        ("Scene 5: Verification & Geometric Interpretation", "55.10s (Scene: 55.30s)", 136,
         "Substitution into Eq 1, 2, 3 with green checkmarks. Cards for inconsistent (0=5) and dependent (0=0) systems.",
         "Let us verify our solution by substituting x equals 1, y equals 2, and z equals 3 into all three original equations.\n\n"
         "Equation 1: 1 plus 2 plus 3 equals 6. Verified!\n\n"
         "Equation 2: 2 times 1 plus 3 times 2 plus 3 equals 11. Verified!\n\n"
         "Equation 3: 1 plus 2 times 2 plus 3 times 3 equals 14. Verified!\n\n"
         "All three equations hold. Geometrically, (1, 2, 3) is the exact point where all three planes intersect.\n\n"
         "Consider two special cases.\n\n"
         "An inconsistent system produces a row like [0, 0, 0 | 5], meaning 0 equals 5. This contradiction means no solution exists.\n\n"
         "A dependent system produces a row like [0, 0, 0 | 0], meaning 0 equals 0. With free variables, this indicates infinitely many solutions along an intersecting line."),

        ("Scene 6: Summary, Academic References & Credits", "53.92s (Scene: 54.20s)", 102,
         "Three takeaway cards. Academic citations. AI disclosure card. Closing thank you card.",
         "To summarize, here are three key takeaways:\n\n"
         "One: Gaussian elimination systematically transforms a linear system into row echelon form.\n\n"
         "Two: Elementary row operations preserve the solution set because they are reversible.\n\n"
         "Three: Back substitution easily reveals the unknown variables from bottom to top.\n\n"
         "Our verified solution is (1, 2, 3).\n\n"
         "References include Strang's Introduction to Linear Algebra, Lay's Linear Algebra and Its Applications, and Manim documentation.\n\n"
         "AI disclosure: AI tools assisted in preparing the script, animation code and visual design. Voiceover: Original narration recorded by Arjav Jain. All mathematical calculations were independently verified.\n\n"
         "Thank you. Arjav Jain, Student ID E25B070861.")
    ]

    for title, dur, wc, cues, text in scenes_data:
        scene_header = [
            [Paragraph(f"<b>{title}</b>", styles['h1']),
             Paragraph(f"<b>Duration:</b> {dur}  |  <b>Words:</b> {wc}", styles['meta_val'])]
        ]
        sh_table = Table(scene_header, colWidths=[350, 154])
        sh_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('LINEBELOW', (0,0), (-1,-1), 1, C_SECONDARY)
        ]))
        story.append(sh_table)
        story.append(Paragraph(f"<i>Visual Cues: {cues}</i>", styles['meta_label']))
        story.append(Spacer(1, 4))

        # Format paragraphs
        for para in text.split("\n\n"):
            story.append(Paragraph(para, styles['body']))
        story.append(Spacer(1, 8))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("-> Generated Narration_Script.pdf")

# =========================================================================
# 3. CODE WALKTHROUGH PDF
# =========================================================================
def generate_code_walkthrough_pdf():
    pdf_path = os.path.join(PROJECT_ROOT, "Code_Walkthrough.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = create_base_styles()
    story = []

    story.extend(build_metadata_header(styles, "Code Walkthrough & Architecture Guide"))

    intro_p = Paragraph(
        "This document provides a beginner-friendly, comprehensive architectural walkthrough of the complete "
        "animation codebase. It is designed to prepare the student (Arjav Jain) to confidently explain the "
        "programming decisions, mathematical representations, and video production pipeline during the individual viva.",
        styles['body']
    )
    story.append(intro_p)
    story.append(Spacer(1, 8))

    sections = [
        ("1. Technology Stack & Framework Selection",
         "The project is engineered with an entirely programmatic, reproducible technology stack:<br/>"
         "• <b>Manim Community Edition (v0.22.1):</b> Used for high-precision mathematical vector animations. Unlike static video editors, Manim renders equations and matrices as true vector paths with mathematical positioning.<br/>"
         "• <b>ThreeDScene & ThreeDAxes:</b> Manim's 3D engine computes parametric surfaces and renders camera orbits to display intersecting geometric planes.<br/>"
         "• <b>NumPy (v2.5.5):</b> Performs automated verification of matrix determinants, solves, step-by-step row operations, and residuals prior to rendering.<br/>"
         "• <b>Human Voiceover Audio:</b> Original narration recorded by Arjav Jain (Student ID: E25B070861), standardized to 44.1 kHz 16-bit mono PCM with gentle EBU R128 loudness normalization and exact animation timing synchronization.<br/>"
         "• <b>FFmpeg (v9.0.2):</b> Handles audio-video multiplexing, duration padding, concatenation, H.264 video encoding, and AAC audio compression."),

        ("2. Visual Hierarchy & Color Philosophy",
         "A strict, mathematically meaningful colour palette is enforced across all scenes:<br/>"
         "• <b>Row 1 / Equation 1:</b> Blue (<code>#3B82F6</code>) — Represents the initial constraint plane.<br/>"
         "• <b>Row 2 / Equation 2:</b> Emerald Green (<code>#10B981</code>) — Represents the second intersecting constraint.<br/>"
         "• <b>Row 3 / Equation 3:</b> Vivid Orange (<code>#F97316</code>) — Represents the third constraint completing the intersection.<br/>"
         "• <b>Pivot Elements:</b> Golden Yellow (<code>#FBBF24</code>) — Bounded with pulsating yellow rectangles to spotlight leading coefficients.<br/>"
         "• <b>Background:</b> Deep Navy (<code>#0B1120</code>) — Provides optimal contrast against high-saturation colored vector shapes without eye fatigue.<br/>"
         "• <b>Verification Checkmarks:</b> Bright Green (<code>#22C55E</code>) — Signifies exact mathematical satisfaction."),

        ("3. Matrix Building Helper (`matrix_helpers.py`)",
         "Instead of relying on fragile external LaTeX installations that can break across platforms, the project implements a custom <code>build_augmented_matrix()</code> helper:<br/>"
         "• Constructs a visual 3×4 augmented matrix grid with aligned column offsets: <code>[0.0, 1.0, 2.0, 3.4]</code>.<br/>"
         "• Places an augmented vertical dividing bar between columns 3 and 4.<br/>"
         "• Renders outer left and right bracket delimiters with clean rounded line vectors.<br/>"
         "• Enables smooth in-place entry transformations using <code>Transform(grid[r][c], new_text)</code> so unchanged entries remain rock-solid stable on screen while changed row entries animate smoothly.<br/>"
         "• <code>create_staircase()</code> automatically connects pivot corners to visualize Row Echelon Form."),

        ("4. Scene-by-Scene Implementation Architecture",
         "• <b>Scene 1 (scene_01_hook.py):</b> Renders the mandatory opening title card with student name, ID, and batch. Sequences the 3 equations one by one and transitions to the Gaussian elimination reveal.<br/>"
         "• <b>Scene 2 (scene_02_concepts.py):</b> Groups coefficient matrix A, vector x, and vector b into styled cards. Highlights the exact learning objective in a rounded amber callout box. Explains the 3 elementary row operations and their reversibility.<br/>"
         "• <b>Scene 3 (scene_03_geometry.py):</b> Subclasses <code>ThreeDScene</code>. Constructs three parametric surfaces for equations z = 6-x-y, z = 11-2x-3y, and z = (14-x-2y)/3 with semi-transparent opacity (0.35). Places a golden <code>Sphere</code> at (1, 2, 3) and executes an ambient camera rotation (<code>rate=0.25</code>) to demonstrate the intersection line and common point.<br/>"
         "• <b>Scene 4 (scene_04_worked_example.py):</b> The computational core. Animates the 3 row operations with dedicated side-panel arithmetic showing the exact vector subtractions. Highlights pivots in yellow boxes and executes back substitution from Row 3 to Row 1.<br/>"
         "• <b>Scene 5 (scene_05_interpretation.py):</b> Verifies the solution by substituting (1, 2, 3) into all three equations, rendering animated green checkmarks. Contrasts inconsistent systems ([0 0 0 | 5] → 0 = 5) and dependent systems ([0 0 0 | 0] → 0 = 0).<br/>"
         "• <b>Scene 6 (scene_06_summary.py):</b> Presents three core takeaway cards, final solution re-statement, academic citations, AI disclosure, and closing thank you card."),

        ("5. Audio-Video Synchronization Pipeline (`merge_video_audio.py`)",
         "A critical requirement of the project is ensuring human narration is never cut off and contains no unnatural dead silence:<br/>"
         "1. Original human voiceover recordings by Arjav Jain (in <code>Arjav_M3_Voiceovers/</code>) are standardized by <code>process_audio.py</code> into 44.1 kHz 16-bit mono WAV files with gentle EBU R128 loudness normalization (-18 LUFS, -1.5 dB true peak headroom).<br/>"
         "2. Exact spoken durations are measured via <code>analyze_audio.py</code> and logged to <code>durations.txt</code> and <code>scene_audio_manifest.json</code> (total human voice: 314.96s).<br/>"
         "3. Manim scene durations are calibrated to match or slightly exceed spoken duration (total calibrated scene duration: 316.60s).<br/>"
         "4. <code>merge_video_audio.py</code> inspects both streams. If video slightly exceeds audio, it adds brief silence padding via FFmpeg <code>apad</code>. If video is shorter, it holds the final video frame via <code>tpad=stop_mode=clone</code>.<br/>"
         "5. The 6 synchronized scenes are concatenated into <code>_Video.mp4</code> using the FFmpeg concat demuxer (final container duration: 316.63s)."),

        ("6. Mathematical Verification Suite (`verify_mathematics.py`)",
         "Guarantees 100% mathematical accuracy before any video rendering takes place:<br/>"
         "• Checks <code>det(A) = 3.0 ≠ 0</code>, proving non-singularity and uniqueness.<br/>"
         "• Solves Ax = b using <code>np.linalg.solve</code> to confirm (1, 2, 3).<br/>"
         "• Performs manual elementary row operations on the augmented matrix array and verifies equality with expected echelon matrix [U | c].<br/>"
         "• Evaluates residuals <code>A @ x - b</code>, confirming they equal exactly 0.0.<br/>"
         "• Tests all three original equations individually.")
    ]

    for title, content in sections:
        story.append(Paragraph(f"<b>{title}</b>", styles['h1']))
        story.append(Paragraph(content, styles['body']))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("-> Generated Code_Walkthrough.pdf")

# =========================================================================
# 4. VIVA PREPARATION PDF
# =========================================================================
def generate_viva_prep_pdf():
    pdf_path = os.path.join(PROJECT_ROOT, "Viva_Prep.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = create_base_styles()
    story = []

    story.extend(build_metadata_header(styles, "Viva Voce Examination Preparation Guide"))

    intro_p = Paragraph(
        "This guide compiles 15 essential viva voce questions spanning linear algebra theory, "
        "geometric intuition, Gaussian elimination algorithms, and animation implementation details. "
        "Answers are concise, mathematically rigorous, and easy to memorize for the oral examination.",
        styles['body']
    )
    story.append(intro_p)
    story.append(Spacer(1, 8))

    q_and_a = [
        ("Q1. What is Gaussian Elimination, and what is its primary objective?",
         "Gaussian elimination is a systematic algorithm for solving systems of linear equations. Its primary objective is to apply elementary row operations to an augmented matrix to transform it into an upper-triangular Row Echelon Form (REF), from which the unknowns can be solved easily via back substitution."),

        ("Q2. What is an augmented matrix [A | b], and why is it preferred over working with equations?",
         "An augmented matrix combines the coefficient matrix A and the constant vector b into a single compact array [A | b]. It separates the algebraic coefficients from the variable names, allowing systematic row operations without writing out variable symbols repeatedly, preventing clerical errors."),

        ("Q3. What are the three elementary row operations?",
         "1. <b>Row Swap:</b> Interchanging two rows (R_i ↔ R_j).<br/>"
         "2. <b>Row Scaling:</b> Multiplying all entries in a row by a non-zero scalar (R_i → k·R_i, k ≠ 0).<br/>"
         "3. <b>Row Replacement:</b> Adding a scalar multiple of one row to another row (R_i → R_i + k·R_j)."),

        ("Q4. Why do elementary row operations strictly preserve the solution set of a linear system?",
         "Because every elementary row operation is fully reversible. Each operation corresponds to an invertible matrix transformation. Since we can undo any row operation by another elementary row operation, no solutions are added and no solutions are lost."),

        ("Q5. What is a pivot element, and why can a pivot never equal zero?",
         "A pivot is the first non-zero leading entry in a row of a matrix during elimination. It is used to eliminate entries beneath it. A pivot cannot be zero because division by zero is undefined during scaling or row elimination; if a pivot is zero, a row swap with a lower row possessing a non-zero entry must be performed."),

        ("Q6. What defines Row Echelon Form (REF), and how does Gaussian Elimination compare with Gauss-Jordan Elimination (RREF)?",
         "A matrix is in Row Echelon Form (REF) if: (1) all zero rows are at the bottom, (2) each leading non-zero entry (pivot) is strictly to the right of the pivot above it, and (3) all entries below each pivot are zero. Reduced Row Echelon Form (RREF) further requires every pivot to equal 1 and every entry <i>above and below</i> each pivot to be zero.<br/><br/>"
         "<b>Computational Complexity & Operation Comparison:</b> Both algorithms have an asymptotic time complexity of O(n³) for an n×n system. However, their operation distribution differs:<br/>"
         "• <b>Gaussian Elimination</b> performs forward elimination to reach upper-triangular REF (requiring ~2/3 n³ arithmetic operations) followed by backward substitution (requiring ~n² operations).<br/>"
         "• <b>Gauss-Jordan Elimination</b> eliminates coefficients both above and below each pivot during matrix reduction (requiring ~n³ arithmetic operations), directly producing RREF without back-substitution.<br/>"
         "• When solving a single standard system Ax = b, Gaussian elimination requires fewer total arithmetic operations because back-substitution is computationally cheaper than eliminating above all pivots. Gauss-Jordan is preferred when computing matrix inverses ([A | I] → [I | A⁻¹]) or solving for multiple right-hand-side vectors simultaneously."),

        ("Q7. How does back substitution work?",
         "Once a matrix is in Row Echelon Form, the bottom equation has only one unknown (e.g., 3z = 9 ⇒ z = 3). We substitute that value into the equation above (y − z = −1 ⇒ y = 2), and finally substitute both values into the top equation (x + y + z = 6 ⇒ x = 1), solving the system bottom-to-top."),

        ("Q8. What does a single linear equation in three variables represent geometrically?",
         "In three-dimensional Euclidean space (R³), a single linear equation ax + by + cz = d represents an infinite, flat, two-dimensional plane. The vector (a, b, c) is the normal vector perpendicular to the plane."),

        ("Q9. How do planes intersect in 3D, and what does a unique solution mean geometrically?",
         "Two non-parallel planes intersect along a continuous straight line. A third non-parallel plane crosses that line at exactly one point. A unique solution to a 3×3 system represents the single point in 3D space where all three planes simultaneously meet, here (1, 2, 3)."),

        ("Q10. What is the geometric interpretation of elementary row operations?",
         "An elementary row operation replaces one plane with an equivalent linear combination of planes. Geometrically, the transformed plane tilts or rotates, but it continues to pass through the exact same line of intersection as the original plane. Thus, the common point of intersection remains strictly invariant."),

        ("Q11. What matrix row pattern indicates an inconsistent system, and what is its geometry?",
         "A row of the form [0 0 0 | k] where k ≠ 0 represents 0x + 0y + 0z = k, or 0 = k (a contradiction). This means the system has no solution. Geometrically, the three planes do not have a mutual intersection (e.g., two are parallel, or they intersect pairwise in three parallel lines like a triangular prism)."),

        ("Q12. What matrix row pattern indicates a dependent system, and does [0 0 0 | 0] always guarantee infinite solutions?",
         "A row of the form [0 0 0 | 0] represents 0 = 0 (a tautology), providing no constraint. When remaining rows leave free variables, the system has infinitely many solutions (intersecting along an entire line or plane). However, [0 0 0 | 0] does <i>not</i> guarantee infinite solutions if another row in the same matrix contradicts with [0 0 0 | k]."),

        ("Q13. How does the determinant of the coefficient matrix det(A) relate to the solution?",
         "If det(A) ≠ 0, matrix A is invertible (non-singular), guaranteeing that the system Ax = b has a unique solution. In our project, det(A) = 3.0 ≠ 0, confirming before elimination that exactly one solution exists."),

        ("Q14. How does Manim's ThreeDScene render 3D geometry programmatically?",
         "Manim's <code>ThreeDScene</code> uses <code>ThreeDAxes</code> to define a 3D coordinate frame. Surfaces are defined parametrically using lambda functions mapping (u, v) coordinates to 3D space points (c2p). Camera orientation is controlled via spherical angles: <code>phi</code> (elevation from z-axis) and <code>theta</code> (azimuth in x-y plane)."),

        ("Q15. How did you verify the mathematical calculations in your project?",
         "Using an automated NumPy verification script: (1) verified det(A) = 3 ≠ 0, (2) solved Ax = b via <code>numpy.linalg.solve</code> yielding [1, 2, 3], (3) computed step-by-step row operations matching our manual arithmetic, (4) evaluated residuals A@x - b = [0, 0, 0], and (5) verified all three original equations: 6=6, 11=11, and 14=14.")
    ]

    for q, a in q_and_a:
        q_p = Paragraph(f"<b>{q}</b>", styles['h2'])
        a_p = Paragraph(a, styles['body'])
        box = Table([[q_p], [a_p]], colWidths=[504])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(box)
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("-> Generated Viva_Prep.pdf")

def main():
    print("=" * 60)
    print("GENERATING ALL FOUR ACADEMIC PROJECT PDFS")
    print("=" * 60)
    generate_storyboard_pdf()
    generate_narration_script_pdf()
    generate_code_walkthrough_pdf()
    generate_viva_prep_pdf()
    print("=" * 60)
    print("All 4 PDFs generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
