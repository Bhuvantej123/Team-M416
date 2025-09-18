from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
import fitz  # PyMuPDF for PDF text extraction
from groq import Groq

main = Blueprint("main", __name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔑 Set your Groq API key
GROQ_API_KEY = "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"

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("pdf_file")
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # extract text
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text("text")

        session["pdf_text"] = text
        flash("File uploaded successfully!", "success")
    else:
        flash("No file selected.", "error")

    return redirect(url_for("main.home"))

@main.route("/summary")
def summary():
    pdf_text = session.get("pdf_text", "")
    summary = "No file uploaded yet."

    if pdf_text:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Summarize this text:\n\n{pdf_text[:4000]}"}],  # limit text
        )
        summary = completion.choices[0].message.content

    return render_template("summary.html", summary=summary)
