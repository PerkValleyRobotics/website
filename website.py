from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home_page(): # Returns html
    return render_template("home.html", the_title="PV Robotics Home")

if __name__ == "__main__":
    app.run(debug=True)
