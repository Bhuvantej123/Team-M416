from flask import Blueprint, render_template, request, redirect, url_for, session, flash,current_app
import os
import fitz  # PyMuPDF
from groq import Groq
import uuid
import json

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"
TEXT_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

GROQ_API_KEY = "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"

import re

def format_numbered_list(text):
    """
    Convert text like '1. First 2. Second' into HTML list
    """
    items = re.split(r'\s*\d+\.\s*', text)  # split at 1. 2. 3.
    items = [i.strip() for i in items if i.strip()]
    if not items:
        return text  # fallback if no numbering found
    html_list = "<ol>\n"
    for item in items:
        html_list += f"  <li>{item}</li>\n"
    html_list += "</ol>"
    return html_list




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

    return redirect(url_for("main.home"))


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
        raw_summary = completion.choices[0].message.content
        summary = format_numbered_list(raw_summary)     # 👈 add this line


    return render_template("summary.html", summary=summary)



@main.route("/quiz")
def quiz():
    text_id = session.get("pdf_text_file")
    if not text_id:
        flash("No uploaded file found.", "error")
        return redirect(url_for("main.home"))

    text_path = os.path.join(TEXT_FOLDER, text_id)
    if not os.path.exists(text_path):
        flash("Uploaded file text not found.", "error")
        return redirect(url_for("main.home"))

    with open(text_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()

    client = Groq(api_key=GROQ_API_KEY)
    prompt = (
        "Generate 10 multiple-choice quiz questions based ONLY on the text below. "
        "Respond with STRICT JSON, nothing else. Do not include ``` or explanations.\n\n"
        "Format:\n"
        "{\n"
        "  \"questions\": [\n"
        "    { \"question\": \"...\", \"options\": [\"A) ...\",\"B) ...\",\"C) ...\",\"D) ...\"], \"answer\": \"A\" }\n"
        "  ]\n"
        "}\n\n"
        f"{pdf_text[:4000]}"
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        raw_quiz = completion.choices[0].message.content.strip()

        # Sometimes AI wraps in code fences, strip them
        if raw_quiz.startswith("```"):
            raw_quiz = raw_quiz.split("```")[1]
        if raw_quiz.startswith("json"):
            raw_quiz = raw_quiz[len("json"):].strip()

        quiz_data = json.loads(raw_quiz)
    except Exception as e:
        print("Quiz generation failed:", e)
        quiz_data = {"questions": []}

    return render_template("quiz.html", quiz=quiz_data)
