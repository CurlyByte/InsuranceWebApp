from flask import Blueprint, render_template

homepage = Blueprint('homepage',__name__)

@homepage.route("/home")
@homepage.route("/")
def home():
    return render_template("home.html")