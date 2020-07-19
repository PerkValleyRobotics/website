from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired



class updateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
posts = []


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
        em = len(tag) / 2
        posts.insert(0,{"author" : form.name.data, "body" : form.text.data, "tag" : request.form.get('tag'), "color" : color, "em" : em})
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
