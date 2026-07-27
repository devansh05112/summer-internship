
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart

styles=getSampleStyleSheet()

def generate_quiz_report(report, output_path):
    doc=SimpleDocTemplate(output_path)
    story=[]
    title=styles["Heading1"]; title.alignment=TA_CENTER
    story.append(Paragraph("Cerebra AI Quiz Report",title))
    story.append(Paragraph(f"Document: {report.get('filename','Uploaded PDF')}",styles["BodyText"]))
    story.append(Spacer(1,12))
    data=[
        ["Score",f"{report['score']}/{report['total']}"],
        ["Accuracy",f"{report['accuracy']}%"],
        ["Correct",str(report["correct"])],
        ["Wrong",str(report["wrong"])],
        ["Skipped",str(report["skipped"])],
        ["Feedback",report["feedback"]],
    ]
    t=Table(data,colWidths=[120,300])
    t.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#cccccc")),
        ("BACKGROUND",(0,0),(-1,0),HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),HexColor("#ffffff")),
        ("BACKGROUND",(0,1),(-1,-1),HexColor("#F8FAFC")),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    story.append(t)
    story.append(Spacer(1,18))
    d=Drawing(300,180)
    p=Pie()
    p.x=60;p.y=0;p.width=140;p.height=140
    p.data=[report["correct"],report["wrong"],report["skipped"]]
    p.labels=["Correct","Wrong","Skipped"]
    d.add(p)
    story.append(d)
    story.append(PageBreak())
    story.append(Paragraph("Question Review",styles["Heading2"]))
    for i,item in enumerate(report["review"],1):
        story.append(Paragraph(f"<b>Q{i}.</b> {item['question']}",styles["BodyText"]))
        story.append(Paragraph(f"<b>Status:</b> {item['status']}",styles["BodyText"]))
        story.append(Paragraph(f"<b>Your Answer:</b> {item['user_answer']}",styles["BodyText"]))
        story.append(Paragraph(f"<b>Correct Answer:</b> {item['correct_answer']}",styles["BodyText"]))
        story.append(Paragraph(f"<b>Explanation:</b> {item['explanation']}",styles["BodyText"]))
        story.append(Spacer(1,12))
    doc.build(story)
    return output_path
