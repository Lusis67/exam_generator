from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def text_to_pdf(text, output_pdf_path, title="Practice Exam", subtitle=None, details=None):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

    # --- Cover Page ---
    title_style = styles["Title"]
    story.append(Spacer(1, 100))
    story.append(Paragraph(title, title_style))
    if subtitle:
        subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=16, alignment=1, spaceAfter=20)
        story.append(Spacer(1, 24))
        story.append(Paragraph(subtitle, subtitle_style))
    if details:
        details_style = ParagraphStyle("Details", parent=styles["Normal"], fontSize=12, alignment=1, spaceAfter=12)
        story.append(Spacer(1, 24))
        for line in details:
            story.append(Paragraph(line, details_style))
    story.append(PageBreak())

    # --- Questions ---
    questions = [q.strip() for q in text.strip().split("\n\n") if q.strip()]
    question_style = ParagraphStyle(
        "Question",
        parent=styles["Normal"],
        leftIndent=20,
        spaceAfter=12,
        fontSize=12,
    )
    for idx, question in enumerate(questions, 1):
        numbered_question = f"Question {idx}:<br/>{question.replace(chr(10), '<br/>')}"
        story.append(Paragraph(numbered_question, question_style))
        story.append(PageBreak())

    doc.build(story)