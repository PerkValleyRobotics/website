from http import client

from flask import Flask, render_template, request, redirect, url_for, flash, json

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
import user


class updateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')


posts = []
numTasks = 0
codeTasks = []


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


@app.route("/Tasks", methods=["POST"])
def task_form():
    global numTasks
    global codeTasks

    codeForm = request.form['code']
    if codeForm and not codeForm == "":
        codeTasks.append(
            {"color": "Tomato", "task": codeForm, "taskNum": str(numTasks + 1), "claimText": "Claim Task", "sort": 1})
        numTasks += 1
        return redirect('/Tasks')


@app.route("/Tasks", methods=["GET"])
def task_page():  # Returns html
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

    return render_template("task.html", codeTasks=sorted(codeTasks, key=lambda x: x["sort"]),
                           the_title="PV Robotics Tasks")


@app.route("/Updates", methods=["GET", "POST"])
def updates_page():  # Returns html
    tag = request.args.get("tag", '')
    p = []
    if tag == "All" or tag == "":
        p = posts
    else:
        for i in range(len(posts)):
            if posts[i]["tag"] == tag:
                p.append(posts[i])

    return render_template('updates.html', posts=p, the_title="PV Robotics Updates")


@app.route('/Post', methods=["GET", "POST"])
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
        posts.insert(0,
                     {"author": form.name.data, "body": form.text.data, "tag": request.form.get('tag'), "color": color,
                      "ch": ch})
        return redirect('/Updates')
    return render_template('post.html', title='Sign In', form=form)


@app.route("/CodeTeamBestTeam")
def code_best():  # Returns html
    return render_template("home.html", the_title="Code Team Best Team")


@app.route("/Privacy")
def privacy():  # Returns html
    return render_template("privacy.html", the_title="Privacy Policy")


@app.route("/UnderConstruction")
def under_construction():  # Returns html
    return render_template("underConstruction.html", the_title="Work in Progress")


# Code for Logining in a user
login_manager = LoginManager()
login_manager.init_app(app)

# This needs to be changed when added to site with actual credentials
GOOGLE_CLIENT_ID = "GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "GOOGLE_CLIENT_SECRET"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return user.User.get(user_id)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/test")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


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
def callback(user=None):
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
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = user.User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not user.User.get(unique_id):
        user.User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
