from flask import Blueprint, render_template

# Create a Blueprint object
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/upload") 
def upload():
    return render_template("upload.html")

