from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home_page(): # Returns html
    return render_template("entry.html", the_title="Perkiomen Valley Robotics Scouting Page")

if __name__ == "__main__":
    app.run(debug=True)
