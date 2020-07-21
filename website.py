from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from user import User

class updateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')



posts = []
numTasks = 0
codeTasks = []

#Code for Logining in a user
login_manager = LoginManager()
login_manager.init_app(app)

GOOGLE_CLIENT_ID = "GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "GOOGLE_CLIENT_SECRET"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

#Code for Webpages
@app.route("/FAQ")
def FAQ_page(): # Returns html
    return render_template("FAQ.html", the_title="FAQ")

@app.route("/Volunteer")
def Volunteer_page(): # Returns html
    return render_template("Volunteer.html", the_title="Volunteer")

@app.route("/")
def home_page(): # Returns html
    return render_template("home.html", the_title="PV Robotics Home")

@app.route("/Tasks", methods=["POST"])
def task_form():
    global numTasks
    global codeTasks

    codeForm = request.form['code']
    if codeForm and not codeForm == "":
        codeTasks.append({"color" : "Tomato", "task" : codeForm, "taskNum" : str(numTasks +1), "claimText" : "Claim Task", "sort" : 1})
        numTasks += 1
        return redirect('/Tasks')

@app.route("/Tasks", methods=["GET"])
def task_page(): # Returns html
    global codeTasks
    teamClaim = request.args.get("claim", '')
    taskNum = request.args.get("num", '')

    if teamClaim == "code":
        for i in range(len(codeTasks)):
            try:
                if codeTasks[i]["taskNum"] == taskNum:
                    if codeTasks[i]["color"] == "Tomato":
                        codeTasks[i]["color"] = "Orange"
                        codeTasks[i]["claimText"] = "Finish"
                        codeTasks[i]["sort"] = 0
                    elif codeTasks[i]["color"] == "Orange":
                        codeTasks[i]["color"] = "MediumSeaGreen"
                        codeTasks[i]["claimText"] = "Remove"
                        codeTasks[i]["sort"] = 2
                    else:
                        codeTasks.pop(i)
            except:
                pass

    return render_template("task.html", codeTasks= sorted(codeTasks, key=lambda x: x["sort"]), the_title="PV Robotics Tasks")

@app.route("/Updates", methods=["GET","POST"])
def updates_page(): # Returns html
    tag = request.args.get("tag", '')
    p = []
    if tag == "All" or tag == "":
        p = posts
    else:
        for i in range(len(posts)):
            if posts[i]["tag"] == tag:
                p.append(posts[i])

    return render_template('updates.html', posts=p, the_title="PV Robotics Updates")

@app.route('/Post', methods=["GET","POST"])
def post():
    global posts
    form = updateForm()
    if form.validate_on_submit():
        flash('Posted')
        tag = request.form.get('tag')

        def switch(argument):
            switcher = {
                "Code": "DodgerBlue",
                "Mechanical": "Tomato",
                "Electrical": "Orange",
                "Business": "MediumSeaGreen",
                "Other": "grey",
            }
            return switcher.get(argument, "white")
        color = switch(tag)
        ch = len(tag) + .5
        posts.insert(0,{"author" : form.name.data, "body" : form.text.data, "tag" : request.form.get('tag'), "color" : color, "ch" : ch})
        return redirect('/Updates')
    return render_template('post.html', title='Sign In', form=form)

@app.route("/CodeTeamBestTeam")
def code_best(): # Returns html
    return render_template("home.html", the_title="Code Team Best Team")

@app.route("/Privacy")
def privacy(): # Returns html
    return render_template("privacy.html", the_title="Privacy Policy")

@app.route("/UnderConstruction")
def under_construction(): # Returns html
    return render_template("underConstruction.html", the_title="Work in Progress")

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
