import os
import json
from pptx import Presentation
from fpdf import FPDF
from pptx.util import Inches
from io import BytesIO
from unidecode import unidecode


def save_img(img, img_ext):
    if not os.path.exists("temp"):
        os.mkdir("temp")

    file_name = os.path.join("temp", str(len(os.listdir("temp"))) + "." + img_ext)
    img.save(file_name)

    return file_name

def json_to_blog_html(json_input: str, output_file: str = "blog_post.html") -> str:
    data = json.loads(json_input)
    
    # Extract content
    headline = data.get("headline", "")
    introduction = data.get("introduction", "")
    body = data.get("body", [])
    conclusion = data.get("conclusion", "")

    # Build HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{headline}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 2rem auto;
                padding: 1rem;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                color: #004080;
            }}
            p {{
                margin-bottom: 1rem;
            }}
        </style>
    </head>
    <body>
        <h1>{headline}</h1>
        <p>{introduction}</p>
    """

    for paragraph in body:
        html_content += f"<p>{paragraph}</p>\n"

    html_content += f"<p><strong>{conclusion}</strong></p>\n"

    html_content += """
    </body>
    </html>
    """

    # Save to file
    # with open(output_file, "w", encoding="utf-8") as f:
    #     f.write(html_content.strip())

    return html_content.strip()


def json_to_presentation(json_input: str, output_file: str = "content.pptx") -> BytesIO:

    json_input = json.loads(json_input)
    prs = Presentation()

    # Define layout indexes
    TITLE_SLIDE_LAYOUT = 0
    TITLE_AND_CONTENT_LAYOUT = 1

    for slide_data in json_input:
        if "subtitle" in slide_data:
            slide_layout = prs.slide_layouts[TITLE_SLIDE_LAYOUT]
            slide = prs.slides.add_slide(slide_layout)
            slide.shapes.title.text = slide_data["title"]
            slide.placeholders[1].text = slide_data["subtitle"]
        else:
            slide_layout = prs.slide_layouts[TITLE_AND_CONTENT_LAYOUT]
            slide = prs.slides.add_slide(slide_layout)
            slide.shapes.title.text = slide_data["title"]
            content = slide.placeholders[1].text_frame
            content.clear()

            for bullet in slide_data.get("bullets", []):
                p = content.add_paragraph()
                p.text = bullet
                p.level = 0

    # Save to in-memory buffer
    buffer = BytesIO()
    prs.save(buffer)
    buffer.seek(0)
    return buffer

class ProposalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Grant Proposal", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0)
        self.multi_cell(0, 10, title)
        self.ln(2)

    def chapter_body(self, text):
        self.set_font("Helvetica", "", 12)
        self.set_text_color(50)
        self.multi_cell(0, 8, text)
        self.ln(4)

def json_to_pdf(json_input: str) -> BytesIO:
    data = json.loads(json_input)
    pdf = ProposalPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for section in data:
        heading = unidecode(section.get("heading", ""))
        content = unidecode(section.get("content", ""))
        pdf.chapter_title(heading)
        pdf.chapter_body(content)

    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Get PDF as bytes
    buffer = BytesIO()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer