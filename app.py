from flask import Flask, render_template, request, redirect, url_for
import PyPDF2
import docx

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    summary = ""

    if request.method == "POST":

        text = request.form.get("input_text")

        summary_length = request.form.get("summary_length")

        pdf_file = request.files.get("pdf_file")

        docx_file = request.files.get("docx_file")

        # PDF TEXT

        if pdf_file and pdf_file.filename != "":

            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""

            for page in pdf_reader.pages:

                text += page.extract_text()

        # DOCX TEXT

        elif docx_file and docx_file.filename != "":

            doc = docx.Document(docx_file)

            text = ""

            for para in doc.paragraphs:

                text += para.text

        # SUMMARY

        words = text.split()

        if summary_length == "short":

            summary = " ".join(words[:50])

        elif summary_length == "medium":

            summary = " ".join(words[:100])

        else:

            summary = " ".join(words[:150])

        return render_template(
            "index.html",
            summary=summary
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)