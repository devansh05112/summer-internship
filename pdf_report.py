from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT
)

from reportlab.lib.colors import (
    HexColor,
    white,
    black
)

from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime
import os

# =====================================================
# FONT
# =====================================================

try:

    pdfmetrics.registerFont(
        TTFont(
            "Cerebra",
            "C:/Windows/Fonts/arial.ttf"
        )
    )

    FONT = "Cerebra"

except:

    FONT = "Helvetica"

# =====================================================
# COLORS
# =====================================================

PRIMARY = HexColor("#2563EB")
PRIMARY_LIGHT = HexColor("#DBEAFE")

SUCCESS = HexColor("#16A34A")
WARNING = HexColor("#F59E0B")
DANGER = HexColor("#DC2626")

TEXT = HexColor("#1F2937")
MUTED = HexColor("#6B7280")

CARD = HexColor("#F8FAFC")
BORDER = HexColor("#E5E7EB")

# =====================================================
# STYLES
# =====================================================

styles = getSampleStyleSheet()

TITLE = ParagraphStyle(

    "TITLE",

    parent=styles["Heading1"],

    fontName=FONT,

    fontSize=30,

    alignment=TA_CENTER,

    textColor=PRIMARY,

    spaceAfter=12

)

SUBTITLE = ParagraphStyle(

    "SUBTITLE",

    parent=styles["Heading2"],

    fontName=FONT,

    fontSize=15,

    alignment=TA_CENTER,

    textColor=MUTED,

    spaceAfter=30

)

SECTION = ParagraphStyle(

    "SECTION",

    parent=styles["Heading2"],

    fontName=FONT,

    fontSize=18,

    textColor=PRIMARY,

    spaceBefore=16,

    spaceAfter=10

)

NORMAL = ParagraphStyle(

    "NORMAL",

    parent=styles["BodyText"],

    fontName=FONT,

    fontSize=11,

    leading=20,

    textColor=TEXT

)

SMALL = ParagraphStyle(

    "SMALL",

    parent=styles["BodyText"],

    fontName=FONT,

    fontSize=9,

    textColor=MUTED

)

CENTER = ParagraphStyle(

    "CENTER",

    parent=NORMAL,

    alignment=TA_CENTER

)

# =====================================================
# HEADER / FOOTER
# =====================================================

def add_header_footer(canvas, doc):

    canvas.saveState()

    width, height = doc.pagesize

    canvas.setFillColor(PRIMARY)

    canvas.rect(
        0,
        height - 35,
        width,
        35,
        fill=1,
        stroke=0
    )

    canvas.setFont(FONT, 18)

    canvas.setFillColor(white)

    canvas.drawString(
        40,
        height - 24,
        "Cerebra AI"
    )

    canvas.setFont(FONT, 10)

    canvas.setFillColor(MUTED)

    canvas.drawRightString(

        width - 40,

        20,

        f"Page {doc.page}"

    )

    canvas.restoreState()

# =====================================================
# COVER PAGE
# =====================================================

def build_cover(story, report):

    story.append(
        Spacer(1, 0.7 * inch)
    )

    story.append(
        Paragraph(
            "Cerebra AI",
            TITLE
        )
    )

    story.append(
        Paragraph(
            "Professional Quiz Performance Report",
            SUBTITLE
        )
    )

    story.append(
        HRFlowable(
            width="90%",
            thickness=2,
            color=PRIMARY
        )
    )

    story.append(
        Spacer(1, 0.4 * inch)
    )

    story.append(

        Paragraph(

            f"<b>Study Material:</b> {report.get('filename','Uploaded PDF')}",

            NORMAL

        )

    )

    story.append(
        Spacer(1, 0.15 * inch)
    )

    story.append(

        Paragraph(

            f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y • %I:%M %p')}",

            NORMAL

        )

    )

    story.append(
        Spacer(1, 0.5 * inch)
    )

    story.append(

        Paragraph(

            "This report contains detailed quiz statistics, "
            "performance analysis, charts, and question-by-question review.",

            CENTER

        )

    )

    story.append(
        PageBreak()
    )

    # =====================================================
# PERFORMANCE BADGE
# =====================================================

def get_badge(accuracy):

    if accuracy >= 90:
        return (
            "🏆 Outstanding",
            SUCCESS,
            "Excellent mastery of the topic."
        )

    elif accuracy >= 75:
        return (
            "🥇 Excellent",
            PRIMARY,
            "Very strong understanding with minor mistakes."
        )

    elif accuracy >= 50:
        return (
            "👍 Good",
            WARNING,
            "Decent understanding. More revision is recommended."
        )

    else:
        return (
            "📘 Needs Improvement",
            DANGER,
            "Review the study material and attempt the quiz again."
        )


# =====================================================
# SCORE CARDS
# =====================================================

def build_score_cards(story, report):

    data = [

        [
            Paragraph("<b>Score</b>", CENTER),
            Paragraph("<b>Accuracy</b>", CENTER)
        ],

        [
            Paragraph(
                f"<font color='#2563EB'><b>{report['score']} / {report['total']}</b></font>",
                CENTER
            ),

            Paragraph(
                f"<font color='#16A34A'><b>{report['accuracy']}%</b></font>",
                CENTER
            )

        ],

        [
            Paragraph("<b>Correct</b>", CENTER),
            Paragraph("<b>Wrong</b>", CENTER)
        ],

        [
            Paragraph(
                f"<font color='#16A34A'><b>{report['correct']}</b></font>",
                CENTER
            ),

            Paragraph(
                f"<font color='#DC2626'><b>{report['wrong']}</b></font>",
                CENTER
            )

        ],

        [
            Paragraph("<b>Skipped</b>", CENTER),
            Paragraph("<b>Total Questions</b>", CENTER)
        ],

        [
            Paragraph(
                f"<font color='#F59E0B'><b>{report['skipped']}</b></font>",
                CENTER
            ),

            Paragraph(
                f"<b>{report['total']}</b>",
                CENTER
            )

        ]

    ]

    table = Table(

        data,

        colWidths=[3.1 * inch, 3.1 * inch]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), CARD),

            ("GRID", (0, 0), (-1, -1), 1, BORDER),

            ("BOX", (0, 0), (-1, -1), 1, BORDER),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),

            ("TOPPADDING", (0, 0), (-1, -1), 12),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")

        ])

    )

    story.append(
        Paragraph("Quiz Performance", SECTION)
    )

    story.append(table)

    story.append(
        Spacer(1, 0.35 * inch)
    )


# =====================================================
# PIE CHART
# =====================================================

def build_pie_chart(story, report):

    drawing = Drawing(400, 230)

    pie = Pie()

    pie.x = 110
    pie.y = 10

    pie.width = 170
    pie.height = 170

    pie.data = [

        report["correct"],
        report["wrong"],
        report["skipped"]

    ]

    pie.labels = [

        "Correct",
        "Wrong",
        "Skipped"

    ]

    pie.slices[0].fillColor = SUCCESS
    pie.slices[1].fillColor = DANGER
    pie.slices[2].fillColor = WARNING

    pie.slices.strokeWidth = 0.5

    drawing.add(pie)

    story.append(
        Paragraph("Answer Distribution", SECTION)
    )

    story.append(drawing)

    story.append(
        Spacer(1, 0.3 * inch)
    )


# =====================================================
# BAR CHART
# =====================================================

def build_bar_chart(story, report):

    drawing = Drawing(420, 240)

    chart = VerticalBarChart()

    chart.x = 60
    chart.y = 40

    chart.width = 300
    chart.height = 150

    chart.data = [[

        report["correct"],
        report["wrong"],
        report["skipped"]

    ]]

    chart.categoryAxis.categoryNames = [

        "Correct",
        "Wrong",
        "Skipped"

    ]

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max(report["total"], 5)
    chart.valueAxis.valueStep = 1

    chart.bars[0].fillColor = PRIMARY

    drawing.add(chart)

    story.append(
        Paragraph("Performance Graph", SECTION)
    )

    story.append(drawing)

    story.append(
        Spacer(1, 0.35 * inch)
    )


# =====================================================
# PERFORMANCE BADGE
# =====================================================

def build_badge(story, report):

    badge, color, message = get_badge(
        report["accuracy"]
    )

    badge_style = ParagraphStyle(

        "BADGE",

        parent=CENTER,

        fontName=FONT,

        fontSize=16,

        textColor=color,

        spaceAfter=8

    )

    story.append(
        Paragraph(
            "AI Performance Analysis",
            SECTION
        )
    )

    story.append(
        Paragraph(
            badge,
            badge_style
        )
    )

    story.append(
        Paragraph(
            message,
            CENTER
        )
    )

    story.append(
        Spacer(1, 0.4 * inch)
    )

    # =====================================================
# STATUS COLORS
# =====================================================

def get_status_color(status):

    status = status.lower()

    if status == "correct":
        return SUCCESS

    elif status == "wrong":
        return DANGER

    return WARNING


# =====================================================
# REVIEW CARD
# =====================================================

def build_review_card(story, item, number):

    status_color = get_status_color(item["status"])

    # ---------------------------------------
    # Question Heading
    # ---------------------------------------

    question_style = ParagraphStyle(

        "QUESTION",

        parent=NORMAL,

        fontName=FONT,

        fontSize=13,

        leading=22,

        textColor=TEXT,

        spaceAfter=8

    )

    story.append(

        Paragraph(

            f"<b>Question {number}</b>",

            SECTION

        )

    )

    story.append(

        Paragraph(

            item["question"],

            question_style

        )

    )

    # ---------------------------------------
    # Status Badge
    # ---------------------------------------

    badge = Table(

        [[

            Paragraph(

                f"<font color='white'><b>{item['status']}</b></font>",

                CENTER

            )

        ]],

        colWidths=[1.4 * inch]

    )

    badge.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), status_color),

            ("BOX", (0, 0), (-1, -1), 0, status_color),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("TOPPADDING", (0, 0), (-1, -1), 6),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

        ])

    )

    story.append(badge)

    story.append(Spacer(1, 0.12 * inch))

    # ---------------------------------------
    # Answer Table
    # ---------------------------------------

    answer_data = [

        [

            Paragraph("<b>Your Answer</b>", NORMAL),

            Paragraph(item["user_answer"], NORMAL)

        ],

        [

            Paragraph("<b>Correct Answer</b>", NORMAL),

            Paragraph(item["correct_answer"], NORMAL)

        ]

    ]

    table = Table(

        answer_data,

        colWidths=[1.8 * inch, 4.6 * inch]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), CARD),

            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),

            ("BOX", (0, 0), (-1, -1), 1, BORDER),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("LEFTPADDING", (0, 0), (-1, -1), 10),

            ("RIGHTPADDING", (0, 0), (-1, -1), 10),

            ("VALIGN", (0, 0), (-1, -1), "TOP")

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.15 * inch))

    # =====================================================
# EXPLANATION CARD
# =====================================================

def build_explanation(story, explanation):

    explanation_style = ParagraphStyle(

        "EXPLANATION",

        parent=NORMAL,

        fontName=FONT,

        fontSize=10,

        leading=18,

        backColor=PRIMARY_LIGHT,

        borderPadding=10,

        borderColor=BORDER,

        borderWidth=1,

        spaceBefore=6,

        spaceAfter=14

    )

    story.append(

        Paragraph(

            "<b>AI Explanation</b>",

            NORMAL

        )

    )

    story.append(

        Paragraph(

            explanation,

            explanation_style

        )

    )


# =====================================================
# REVIEW SECTION
# =====================================================

def build_review_section(story, report):

    story.append(PageBreak())

    story.append(

        Paragraph(

            "Question by Question Review",

            TITLE

        )

    )

    story.append(

        Paragraph(

            "Review every question along with your answer, the correct answer and a short explanation.",

            CENTER

        )

    )

    story.append(

        Spacer(1, 0.25 * inch)

    )

    review = report.get("review", [])

    for index, item in enumerate(review, start=1):

        build_review_card(

            story,

            item,

            index

        )

        build_explanation(

            story,

            item.get(

                "explanation",

                "No explanation available."

            )

        )

        story.append(

            HRFlowable(

                width="100%",

                thickness=0.6,

                color=BORDER,

                spaceBefore=8,

                spaceAfter=12

            )

        )

        # Page break every 2 questions
        if index % 2 == 0 and index != len(review):

            story.append(

                PageBreak()

            )


# =====================================================
# BUILD COMPLETE PDF
# =====================================================

def generate_quiz_report(report, output_path):

    doc = SimpleDocTemplate(

        output_path,

        leftMargin=35,

        rightMargin=35,

        topMargin=45,

        bottomMargin=35

    )

    story = []

    # Cover
    build_cover(

        story,

        report

    )

    # Statistics
    build_score_cards(

        story,

        report

    )

    build_pie_chart(

        story,

        report

    )

    build_bar_chart(

        story,

        report

    )

    build_badge(

        story,

        report

    )

    # Review
    build_review_section(

        story,

        report

    )

    doc.build(

        story,

        onFirstPage=add_header_footer,

        onLaterPages=add_header_footer

    )

    return output_path

def generate_summary_pdf(summary, filename, output_path):

    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )

    from reportlab.lib.styles import getSampleStyleSheet

    from reportlab.lib.enums import TA_CENTER

    from reportlab.lib.colors import HexColor

    from datetime import datetime

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = HexColor("#2563EB")

    heading = styles["Heading2"]

    body = styles["BodyText"]

    doc = SimpleDocTemplate(output_path)

    story = []

    # ------------------------------------
    # Title
    # ------------------------------------

    story.append(
        Paragraph(
            "Cerebra AI Summary Report",
            title
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ------------------------------------
    # File Information
    # ------------------------------------

    story.append(
        Paragraph(
            f"<b>Document:</b> {filename}",
            heading
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            body
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ------------------------------------
    # Summary
    # ------------------------------------

    story.append(
        Paragraph(
            "<b>AI Generated Summary</b>",
            heading
        )
    )

    story.append(
        Spacer(1, 10)
    )

    paragraphs = summary.split("\n")

    for para in paragraphs:

        para = para.strip()

        if para:

            story.append(
                Paragraph(
                    para,
                    body
                )
            )

            story.append(
                Spacer(1, 8)
            )

    doc.build(story)

    return output_path