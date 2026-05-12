from flask import send_file
from flask import Flask, render_template, request
from summarizer import summarize_text

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import PyPDF2
import docx

app = Flask(__name__)

def extract_pdf_text(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        text += page.extract_text()

    return text

def extract_docx_text(docx_file):

    doc = docx.Document(docx_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text

    return text

@app.route('/', methods=['GET', 'POST'])
def home():

    summary = ""

    if request.method == 'POST':

        text = request.form.get('text')

        pdf = request.files.get('pdf')

        docx_file = request.files.get('docx')

        if pdf and pdf.filename != "":

            text = extract_pdf_text(pdf)

        elif docx_file and docx_file.filename != "":

            text = extract_docx_text(docx_file)

        if text and text.strip() != "":

            summary = summarize_text(text)

    return render_template(
        'index.html',
        summary=summary
    )

@app.route('/download')

def download_pdf():

    summary = request.args.get('summary')

    pdf_path = "summary.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(summary, styles['BodyText'])
    )

    doc.build(content)

    return send_file(
        pdf_path,
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)