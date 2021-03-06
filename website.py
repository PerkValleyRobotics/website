import os
from http import client
import mysql
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, json, abort
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf import FlaskForm
from oauthlib.oauth2 import WebApplicationClient
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import user
import siteInfo
import taskpage

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


class updateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')


posts = []
numTasks = 0
codeTasks = []

# Calls for data base configuration
dbconfig = {"host": siteInfo.databasehost(),
            "user": siteInfo.databaseuser(),
            "password": siteInfo.databasepassword(),
            "database": siteInfo.database(), }


# Code for Webpages
@app.route("/FAQ")
def FAQ_page():  # Returns html
    return render_template("FAQ.html", the_title="FAQ")


@app.route("/Volunteer")
def Volunteer_page():  # Returns html
    return render_template("Volunteer.html", the_title="Volunteer")


@app.route("/")
def home_page():  # Returns html
    return render_template("home.html", the_title="PV Robotics Home")


def getData(table):
    database = mysql.connector.connect(**dbconfig)
    cursor = database.cursor(dictionary=True)
    cursor.execute("select * from " + table)
    req = cursor.fetchall()
    cursor.close()
    database.close()
    return req


def updateData(table, status, id):
    database = mysql.connector.connect(**dbconfig)
    sql = "UPDATE " + table + " SET status = " + str(status) + " WHERE id = " + str(id)

    cursor = database.cursor()
    cursor.execute(sql)

    database.commit()
    cursor.close()
    database.close()


def saveData(table, args):
    database = mysql.connector.connect(**dbconfig)
    sql = "INSERT INTO " + table + " (task, status) VALUES (%s, %s)"

    cursor = database.cursor()
    cursor.execute(sql, args)

    database.commit()
    cursor.close()
    database.close()


def saveDataGen(table, location, val):
    database = mysql.connector.connect(**dbconfig)
    sql = "INSERT INTO " + table + " (" + location + ") VALUES (" + val + ")"

    cursor = database.cursor()
    cursor.execute(sql)

    database.commit()
    cursor.close()
    database.close()


def taskupdateData(id, level):
    database = mysql.connector.connect(**dbconfig)
    sql = "UPDATE user SET access_level = " + str(level) + " WHERE id = " + str(id)

    cursor = database.cursor()
    cursor.execute(sql)

    database.commit()
    cursor.close()
    database.close()


def getuserData(id):
    database = mysql.connector.connect(**dbconfig)
    cursor = database.cursor(dictionary=True)
    cursor.execute("select " + str(id) + " from user")
    req = cursor.fetchall()
    cursor.close()
    database.close()
    return req


def deleteuser(id):
    database = mysql.connector.connect(**dbconfig)
    cursor = database.cursor()
    cursor.execute("DELETE FROM user WHERE id = " + str(id))
    database.commit()
    cursor.close()
    database.close()


@app.route("/Tasks", methods=["POST"])
@login_required
def task_form():
    global numTasks
    global codeTasks
    try:
        codeTasks = getData("codeTasks")
        codeForm = request.form['code']

        if codeForm and not codeForm == "":
            for task in codeTasks:
                if task["task"] == codeForm:
                    if task["status"] < 2:
                        return redirect('/Tasks#code')

            saveData("codeTasks", (codeForm, 1))
            return redirect('/Tasks')

    except:
        pass

    try:
        mechanicalTasks = getData("mechanicalTasks")
        mechanicalForm = request.form['mechanical']

        if mechanicalForm and not mechanicalForm == "":
            for task in mechanicalTasks:
                if task["task"] == mechanicalForm:
                    if task["status"] < 2:
                        return redirect('/Tasks#mechanical')

            saveData("mechanicalTasks", (mechanicalForm, 1))
            return redirect('/Tasks')
    except:
        pass

    try:
        electricalTasks = getData("electricalTasks")
        electricalForm = request.form['electrical']

        if electricalForm and not electricalForm == "":
            for task in electricalTasks:
                if task["task"] == electricalForm:
                    if task["status"] < 2:
                        return redirect('/Tasks#electrical')

            saveData("electricalTasks", (electricalForm, 1))
            return redirect('/Tasks')
    except:
        pass

    try:
        businessTasks = getData("businessTasks")
        businessForm = request.form['business']

        if businessForm and not businessForm == "":
            for task in businessTasks:
                if task["task"] == businessForm:
                    if task["status"] < 2:
                        return redirect('/Tasks#business')

            saveData("businessTasks", (businessForm, 1))
            return redirect('/Tasks')
    except:
        pass


@app.route("/Tasks", methods=["GET"])
@login_required
def task_page():  # Returns html
    if current_user.access_level is None:
        return taskpage.task_page("tasknoaccess.html")
    else:
        return taskpage.task_page("task.html")


"""@app.route('/Tasks/<team>/<taskID>')
def taskPage(team, taskID):
    if team == "code":
        codeTasks = getData("codeTasks")
        for task in codeTasks:
            if task["id"] == int(id):
                page = task
                break

    return render_template('TaskPage.html', page=page, updates=updates, the_title=page["task"])"""

@app.route("/CodeTeamBestTeam")
def code_best():  # Returns html
    return render_template("home.html", the_title="Code Team Best Team")


@app.route("/Privacy")
def privacy():  # Returns html
    return render_template("privacy.html", the_title="Privacy Policy")

@app.route("/Code")
def code():  # Returns html
    return render_template("code.html", the_title="Privacy Policy")

@app.route("/Electrical")
def electrical():  # Returns html
    return render_template("electrical.html", the_title="Privacy Policy")

@app.route("/Mechanical")
def mechanical():  # Returns html
    return render_template("mechanical.html", the_title="Privacy Policy")

@app.route("/Business")
def business():  # Returns html
    return render_template("business.html", the_title="Privacy Policy")

@app.route("/UnderConstruction")
def under_construction():  # Returns html
    return render_template("underConstruction.html", the_title="Work in Progress")


@app.route("/Control", methods=["GET", "POST"])
@login_required
def control():  # Returns html
    if current_user.access_level == 3:
        if request.method == "POST":
            change = request.form["changeType"]
            userID = request.form["userID"]
            currentLevel = request.form["access"]
            if change == "accessUp":
                if currentLevel == "None":
                    taskupdateData(userID, 1)
                    return redirect(url_for("control"))
                else:
                    taskupdateData(userID, (int(currentLevel) + 1))
                    return redirect(url_for("control"))
            elif change == "accessDown":
                if currentLevel == "None":
                    return redirect(url_for("control"))
                elif int(currentLevel) == 1:
                    taskupdateData(userID, "NULL")
                    return redirect(url_for("control"))
                else:
                    taskupdateData(userID, (int(currentLevel) - 1))
                    return redirect(url_for("control"))
            elif change == "deleteUser":
                deleteuser(userID)
                return redirect(url_for("control"))
            return redirect(url_for("control"))
        else:
            users = []
            userdb = getData("user")
            for people in userdb:
                users.append({"id": people["id"], "name": people["name"], "email": people["email"],
                              "access_level": people["access_level"]})
            return render_template("control.html", users=users)
    else:
        abort(404)


@app.route("/Members", methods=["GET", "POST"])
@login_required
def members():  # Returns HTML
    members = []
    membersdb = getData("memberList")
    for people in membersdb:
        members.append({"id": people["id"], "name": people["name"]})
    if current_user.access_level >= 2:
        if request.method == "POST":
            namedata = "\"" + request.form["member"] + "\""
            saveDataGen("memberList", "name", namedata)
            return redirect(url_for("members"))
        else:
            return render_template("Members.html", members=members, the_title="Members")
    else:
        return render_template("MembersView.html", members=members, the_title="Members")

@app.route("/Updates", methods=["GET", "POST"])
@login_required
def updates():  # Returns HTML
    updates = []
    updatesdb = getData("updates")
    for update in updatesdb:
        updates.append({"id": update["id"], "message": update["message"]})
    if current_user.access_level >= 2:
        if request.method == "POST":
            messagedata = "\"" + request.form["message"] + "\""
            saveDataGen("updates", "message", messagedata)
            return redirect(url_for("updates"))
        else:
            return render_template("updates.html", updates=updates, the_title="Updates")
    else:
        return render_template("updatesView.html", updates=updates, the_title="Updates")


# Code for Logining in a user
login_manager = LoginManager()
login_manager.init_app(app)

# Credentials found in siteInfo
GOOGLE_CLIENT_ID = siteInfo.googleid()
GOOGLE_CLIENT_SECRET = siteInfo.googlesecret()
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return user.User.get(user_id)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/Login")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    else:
        return render_template("gSignIn.html", the_title="Sign In")


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


@app.route("/login/callback")
def callback(user1=None):
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        level = 1
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user1 = user.User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture, access_level=level
    )

    # Doesn't exist? Add it to the database.
    if not user.User.get(unique_id):
        user.User.create(unique_id, users_name, users_email, picture, level)

    # Begin user session by logging the user in
    login_user(user1)

    # Send user back to homepage
    return redirect(url_for("index"))


# Custom error pages
@app.errorhandler(401)
def custom_401(error):
    return render_template("401.html")


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
