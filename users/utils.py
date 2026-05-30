from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import re


def clean_html_for_pdf(html):
    """
    Remove all unsupported HTML before PDF generation
    """

    # Remove style & script blocks
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)

    # Remove external resources
    html = re.sub(r"<link.*?>", "", html)

    # REMOVE ALL <a> LINKS COMPLETELY
    html = re.sub(r"<a.*?>", "", html)
    html = re.sub(r"</a>", "", html)

    # Remove all attributes (class, id, style)
    html = re.sub(r'\s(class|id|style|href)=".*?"', "", html)

    # Remove remaining HTML tags except safe ones
    html = re.sub(r"</?(div|span|section|header|footer|nav)>", "", html)

    return html


def generate_resume_pdf(resume_text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    story = []

    # 🔥 CLEAN HTML FIRST
    resume_text = clean_html_for_pdf(resume_text)

    for line in resume_text.split("\n"):
        line = line.strip()

        if line:
            safe_line = (
                line.replace("&", "&amp;")
                    .replace("<br>", "<br/>")
            )

            story.append(Paragraph(safe_line, styles["Normal"]))
            story.append(Spacer(1, 10))

    doc.build(story)
    buffer.seek(0)
    return buffer
