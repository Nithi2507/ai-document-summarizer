import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from flask import Flask, render_template, request
from summarizer import summarize_text
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    summary = ""

    text = ""

    if request.method == "POST":

        text = request.form.get("text")

        pdf = request.files.get("pdf")

        docx_file = request.files.get("docx")

        max_length = int(request.form.get("length"))


        # PDF upload
        if pdf and pdf.filename != "":

            reader = PdfReader(pdf)

            pdf_text = ""

            for page in reader.pages:
                pdf_text += page.extract_text()

            text = pdf_text

        # DOCX upload
        elif docx_file and docx_file.filename != "":

            doc = Document(docx_file)

            docx_text = ""

            for para in doc.paragraphs:
                docx_text += para.text + "\n"

            text = docx_text

        if text:

            try:
                summary = summarize_text(text, max_length)

            except Exception as e:
                summary = f"Error: {str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)