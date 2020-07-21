from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import mysql.connector

dbconfig = {"host": "theonlycakes.mysql.pythonanywhere-services.com",
                "user": "theonlycakes",
                "password": "3O2W$72l8d",
                "database": "theonlycakes$website", }


def getData(table):
    database = mysql.connector.connect(
        **dbconfig
    )
    cursor = database.cursor(dictionary=True)
    cursor.execute("select * from " + table)
    req = cursor.fetchall()
    cursor.close()
    database.close()
    return req

def updateData(table, status, id):
    database = mysql.connector.connect(
        **dbconfig
    )
    sql = "UPDATE " + table +" SET status = " + str(status) + " WHERE id = " + str(id)

    cursor = database.cursor()
    cursor.execute(sql)

    database.commit()
    cursor.close()
    database.close()

def saveData(table, args):
    database = mysql.connector.connect(
        **dbconfig
    )
    sql = "INSERT INTO " + table +" (task, status) VALUES (%s, %s)"

    cursor = database.cursor()
    cursor.execute(sql, args)

    database.commit()
    cursor.close()
    database.close()


class updateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')


posts = []
numTasks = 0
codeTasks = []

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
def task_page(): # Returns html
    global codeTasks
    teamClaim = request.args.get("claim", '')
    taskID = request.args.get("id", '')

    codeTasks = []
    codeDB = getData("codeTasks")

    mechanicalTasks = []
    mechanicalDB = getData("mechanicalTasks")

    electricalTasks = []
    electricalDB = getData("electricalTasks")

    businessTasks = []
    businessDB = getData("businessTasks")

    for task in codeDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            codeTasks.append({"id": task["id"], "task" : task["task"], "color": color, "claimText": claimText, "status" : task["status"]})

    for task in mechanicalDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            mechanicalTasks.append({"id": task["id"], "task" : task["task"], "color": color, "claimText": claimText, "status" : task["status"]})

    for task in electricalDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            electricalTasks.append({"id": task["id"], "task" : task["task"], "color": color, "claimText": claimText, "status" : task["status"]})

    for task in businessDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            businessTasks.append({"id": task["id"], "task" : task["task"], "color": color, "claimText": claimText, "status" : task["status"]})

    if teamClaim == "code":
        for task in codeTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("codeTasks", newStatus, task["id"])
        return redirect('/Tasks#code')
    elif teamClaim == "mechanical":
        for task in mechanicalTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("mechanicalTasks", newStatus, task["id"])
        return redirect('/Tasks#mechanical')
    elif teamClaim == "electrical":
        for task in electricalTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("electricalTasks", newStatus, task["id"])
        return redirect('/Tasks#electrical')
    elif teamClaim == "business":
        for task in businessTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("businessTasks", newStatus, task["id"])
        return redirect('/Tasks#business')
    else:
        return render_template("task.html",
                               codeTasks= sorted(codeTasks, key=lambda x: x["status"]),
                               mechanicalTasks= sorted(mechanicalTasks, key=lambda x: x["status"]),
                               electricalTasks= sorted(electricalTasks, key=lambda x: x["status"]),
                               businessTasks= sorted(businessTasks, key=lambda x: x["status"]),
                               the_title="PV Robotics Tasks")
# Hello
"""@app.route('/Tasks/<team>/<taskID>')
def taskPage(team, taskID):
    if team == "code":
        codeTasks = getData("codeTasks")
        for task in codeTasks:
            if task["id"] == int(id):
                page = task
                break

    return render_template('TaskPage.html', page=page, updates=updates, the_title=page["task"])"""

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

if __name__ == "__main__":
    app.run(debug=True)
