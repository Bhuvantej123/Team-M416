from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
import fitz  # PyMuPDF
from groq import Groq
import uuid

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"
TEXT_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

GROQ_API_KEY = "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"


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("pdf_file")
    if not file:
        flash("No file selected.", "error")
        return redirect(url_for("main.home"))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract text
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text("text")

    # Save extracted text to a unique file
    text_id = str(uuid.uuid4()) + ".txt"
    text_path = os.path.join(TEXT_FOLDER, text_id)
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Store only filename in session
    session["pdf_text_file"] = text_id
    flash("File uploaded successfully!", "success")

    return redirect(url_for("main.summary"))


@main.route("/summary")
def summary():
    text_id = session.get("pdf_text_file")
    if not text_id:
        return render_template("summary.html", summary="No file uploaded yet.")

    text_path = os.path.join(TEXT_FOLDER, text_id)
    if not os.path.exists(text_path):
        return render_template("summary.html", summary="File not found. Please upload again.")

    with open(text_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()

    summary = "No content to summarize."
    if pdf_text.strip():
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Summarize the following content into clean, well-formatted bullet points.Do not use Markdown symbols like * or **.Return output as plain text with numbered or dashed bullets only.\n\n{pdf_text[:4000]}"
            }],
        )
        summary = completion.choices[0].message.content

    return render_template("summary.html", summary=summary)