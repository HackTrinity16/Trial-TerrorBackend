from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_transcript_pdf(text, output_filename):
    # Register your custom font files
    pdfmetrics.registerFont(TTFont('CustomFont', './JMHTypewriter.ttf'))  # Regular font
    pdfmetrics.registerFont(TTFont('CustomBoldFont', './JMHTypewriter-Bold.ttf'))  # Bold font

    # Use the custom font in your styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='CustomFont', fontSize=12))
    styles.add(ParagraphStyle(name='LeftIndent', alignment=TA_LEFT, leftIndent=36, fontName='CustomFont', fontSize=12))
    styles.add(ParagraphStyle(name='CustomBoldStyle', fontName='CustomBoldFont', fontSize=12))  # Bold style for speakers

    # Create PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    story = []

    # Add header
    story.append(Paragraph("CRIMINAL DISTRICT COURT", styles['Heading1']))
    story.append(Paragraph("PARISH OF ORLEANS", styles['Heading2']))
    story.append(Paragraph("STATE OF LOUISIANA", styles['Heading2']))
    story.append(Spacer(1, 12))

    # Process the text input
    lines = text.split('\n')
    for line in lines:
        if line.strip().startswith('['):
            speaker, content = line.strip().split(']', 1)
            speaker = speaker[1:].strip().upper() + ":"
            content = content[1:]
            story.append(Paragraph(speaker, styles['CustomBoldStyle']))  # Use bold style for speakers
            story.append(Spacer(1, 12))
            story.append(Paragraph(content.strip(), styles['LeftIndent']))
        else:
            story.append(Paragraph(line.strip(), styles['Justify']))

        # Increase the spacing between rows
        story.append(Spacer(1, 12))  # Change the second argument to increase space

    # Build the PDF
    doc.build(story)

# Example usage
text_input = """
[JUDGE]: Welcome to the courtroom. The case of the People v. Smith is now in session. The defendant is charged with first...
[DEFENDER]: Your Honor, I would like to present evidence that the defendant was not present at the scene of the crime...
[DEFENDANT]: The evidence presented by the defender is inadmissible...
"""

create_transcript_pdf(text_input, "court_transcript.pdf")
