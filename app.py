from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import json
from config import *
from utils.pdf_report import generate_summary_pdf
from flask import send_file
from utils.helpers import allowed_file
from ai.pdf_reader import extract_text
from ai.summarizer import summarize
from ai.quiz_generator import generate_quiz
from ai.flashcard_generator import generate_flashcards
from ai.chatbot import ask_notes
""" from summary_pdf import generate_summary_pdf
from quiz_report import generate_quiz_pdf """
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)
from utils.quiz_report import generate_quiz_report
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from flask import send_file

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.colors import HexColor

from flask import send_file

from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# -----------------------------
# Demo Login
# -----------------------------
USERNAME = "admin"
PASSWORD = "admin123"


# =============================
# Login
# =============================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session.clear()

            session["user"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


# =============================
# Dashboard
# =============================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


# =============================
# Upload PDF
# =============================
@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect(url_for("login"))

    if "pdf" not in request.files:
        return redirect(url_for("dashboard"))

    file = request.files["pdf"]

    if file.filename == "":
        return redirect(url_for("dashboard"))

    if not allowed_file(file.filename):
        return redirect(url_for("dashboard"))

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # --------------------------
    # Extract PDF Text
    # --------------------------

    text = extract_text(filepath)

    if not text.strip():
        return "Could not extract text from PDF."

    # Save in session
    session["filename"] = filename
    text_path = os.path.join(app.config["UPLOAD_FOLDER"], "current_text.txt")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Generate Summary
    summary = summarize(text)

    session["summary"] = summary
    session["filename"] = filename

    return render_template(
        "summary.html",
        filename=filename,
        summary=summary
    )


# =============================
# Quiz
# =============================
@app.route("/quiz")
def quiz():

    if "user" not in session:
        return redirect(url_for("login"))

    text_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "current_text.txt"
    )

    if not os.path.exists(text_path):
        return redirect(url_for("dashboard"))

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Generate quiz
    quiz = generate_quiz(text)

    # Save quiz in session (IMPORTANT)
    session["quiz"] = quiz
    session.modified = True

    # Save quiz as JSON (optional backup)
    quiz_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "current_quiz.json"
    )

    with open(quiz_path, "w", encoding="utf-8") as f:
        json.dump(quiz, f, indent=4)

    return render_template(
        "quiz.html",
        quiz=quiz
    )

# ==========================================
# CHAT WITH NOTES
# ==========================================




# ==========================================
# ASK QUESTION
# ==========================================

@app.route("/ask", methods=["POST"])
def ask():

    if "user" not in session:
        return redirect(url_for("login"))

    question = request.form.get("question", "").strip()

    if question == "":
        return {"answer": "Please enter a question."}

    text_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "current_text.txt"
    )

    if not os.path.exists(text_path):

        return {
            "answer": "No notes uploaded yet."
        }

    with open(
        text_path,
        "r",
        encoding="utf-8"
    ) as f:

        notes = f.read()

    try:

        answer = ask_notes(
            notes,
            question
        )

    except Exception as e:

        answer = f"Error: {str(e)}"

    return {
        "answer": answer
    }

# ==========================
# Chat with Notes Page
# ==========================

""" @app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html") """


@app.route("/result", methods=["POST"])
def result():

    import json

    # --------------------------------------
    # Check Login
    # --------------------------------------

    if "user" not in session:
        return redirect(url_for("login"))

    # --------------------------------------
    # Check Quiz
    # --------------------------------------

    if "quiz" not in session:
        return redirect(url_for("quiz"))

    quiz = session["quiz"]

    # --------------------------------------
    # Get Answers
    # --------------------------------------

    answers_json = request.form.get("answers")

    if not answers_json:
        return redirect(url_for("quiz"))

    try:
        user_answers = json.loads(answers_json)
    except Exception:
        return redirect(url_for("quiz"))

    review = []

    correct = 0
    wrong = 0
    skipped = 0

    # --------------------------------------
    # Evaluate Quiz
    # --------------------------------------

    for i, q in enumerate(quiz):

        user = user_answers[i] if i < len(user_answers) else -1

        if user == -1:

            skipped += 1

            status = "Skipped"

            user_answer = "Not Attempted"

        elif user == q["answer"]:

            correct += 1

            status = "Correct"

            user_answer = q["options"][user]

        else:

            wrong += 1

            status = "Wrong"

            user_answer = q["options"][user]

        review.append({

            "status": status,

            "question": q["question"],

            "user_answer": user_answer,

            "correct_answer": q["options"][q["answer"]],

            "explanation": q.get("explanation", "")

        })

    # --------------------------------------
    # Statistics
    # --------------------------------------

    total = len(quiz)

    score = correct

    accuracy = round((score / total) * 100) if total else 0

    # --------------------------------------
    # Feedback
    # --------------------------------------

    if accuracy >= 90:
        feedback = "Outstanding performance! You have mastered this topic."

    elif accuracy >= 75:
        feedback = "Very good work! A little revision will make you excellent."

    elif accuracy >= 50:
        feedback = "Good attempt. Focus on the incorrect questions."

    else:
        feedback = "You need more practice. Review the summary and retry."

    # --------------------------------------
    # Save Report
    # --------------------------------------

    session["report"] = {

        "filename": session.get("filename", "Uploaded Document"),

        "summary": session.get("summary", ""),

        "score": score,

        "total": total,

        "correct": correct,

        "wrong": wrong,

        "skipped": skipped,

        "accuracy": accuracy,

        "feedback": feedback,

        "review": review

    }

    # Make sure Flask writes the session
    session.modified = True

    # --------------------------------------
    # Render Result
    # --------------------------------------

    return render_template(

        "result.html",

        score=score,

        total=total,

        correct=correct,

        wrong=wrong,

        skipped=skipped,

        accuracy=accuracy,

        feedback=feedback,

        review=review

    )
# =============================
# Flashcards
# =============================
""" @app.route("/flashcards")
def flashcards():

    if "user" not in session:
        return redirect(url_for("login"))

    return "<h2>Flashcards Coming Soon</h2>" """


# =============================
# AI Chat
# =============================
@app.route("/chat")
def chat():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html")

from flask import send_file

@app.route("/download-report")
def download_report():

    if "user" not in session:
        return redirect(url_for("login"))

    if "report" not in session:
        return redirect(url_for("dashboard"))

    report = session["report"]

    reports_folder = os.path.join(app.root_path, "reports")
    os.makedirs(reports_folder, exist_ok=True)

    pdf_path = os.path.join(
        reports_folder,
        "Cerebra_AI_Quiz_Report.pdf"
    )

    generate_quiz_report(
        report,
        pdf_path
    )

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="Cerebra_AI_Quiz_Report.pdf",
        mimetype="application/pdf"
    )

@app.route("/download-summary")
def download_summary():

    if "summary" not in session:
        return redirect(url_for("dashboard"))

    filename = "Cerebra_AI_Summary.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = HexColor("#2563EB")

    heading = styles["Heading2"]
    heading.textColor = HexColor("#1E40AF")

    body = styles["BodyText"]
    body.leading = 22

    story = []

    # =====================================
    # Header
    # =====================================

    story.append(
        Paragraph(
            "🧠 CEREBRA AI",
            title
        )
    )

    story.append(
        Paragraph(
            "AI Generated Summary Report",
            heading
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # =====================================
    # File Name
    # =====================================

    story.append(
        Paragraph(
            f"<b>Source PDF:</b> {session.get('filename','Uploaded Document')}",
            body
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # =====================================
    # Summary Heading
    # =====================================

    story.append(
        Paragraph(
            "<b>Summary</b>",
            heading
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # =====================================
    # Summary Content
    # =====================================

    summary = session["summary"]

    paragraphs = summary.split("\n")

    for line in paragraphs:

        if line.strip():

            story.append(
                Paragraph(
                    line,
                    body
                )
            )

            story.append(
                Spacer(1, 8)
            )

    story.append(
        Spacer(1, 20)
    )

    # =====================================
    # Footer
    # =====================================

    story.append(
        Paragraph(
            "<font color='grey' size='10'>Generated by <b>Cerebra AI</b></font>",
            body
        )
    )

    # =====================================
    # Build PDF
    # =====================================

    doc.build(story)

    return send_file(
        filename,
        as_attachment=True
    )

@app.route("/history")
def history():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template("history.html")

@app.route("/my-notes")
def my_notes():

    if "user" not in session:
        return redirect(url_for("login"))

    notes = []

    if os.path.exists(app.config["UPLOAD_FOLDER"]):

        for file in os.listdir(app.config["UPLOAD_FOLDER"]):

            if file.lower().endswith(".pdf"):

                path = os.path.join(app.config["UPLOAD_FOLDER"], file)

                notes.append({
                    "name": file,
                    "date": datetime.fromtimestamp(
                        os.path.getmtime(path)
                    ).strftime("%d %b %Y • %I:%M %p")
                })

    notes.sort(key=lambda x: x["date"], reverse=True)

    return render_template(
        "my_notes.html",
        notes=notes
    )


@app.route("/flashcards")
def flashcards():

    if "user" not in session:
        return redirect(url_for("login"))

    text_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "current_text.txt"
    )

    if not os.path.exists(text_path):
        return redirect(url_for("dashboard"))

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    flashcards = generate_flashcards(text)
   

    flashcard_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "current_flashcards.json"
    )

    with open(flashcard_path, "w", encoding="utf-8") as f:
        json.dump(flashcards, f, indent=4)

    session["flashcards"] = flashcards

    return render_template(
        "flashcards.html",
        flashcards=flashcards
    )



# =============================
# Logout
# =============================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =============================
# Run
# =============================
if __name__ == "__main__":

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.run(debug=True)