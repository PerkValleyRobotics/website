from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home_page(): # Returns html
    return render_template("home.html", the_title="PV Robotics Home")

@app.route("/About")
def about_page(): # Returns html
    return render_template("about.html", the_title="PV Robotics About")

@app.route("/Calendar")
def calendar_page(): # Returns html
    return render_template("calendar.html", the_title="PV Robotics Calendar")

@app.route("/Tasks")
def task_page(): # Returns html
    return render_template("task.html", the_title="PV Robotics Tasks")

@app.route("/CodeTeamBestTeam")
def code_best():
    return render_template("home.html", the_title="Code Team Best Team")

if __name__ == "__main__":
    app.run(debug=True)
