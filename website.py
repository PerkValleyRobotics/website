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

@app.route("/Updates")
def updates_page(): # Returns html
    return render_template('updates.html', posts=posts, the_title="PV Robotics Updates")

@app.route('/Post', methods=["GET","POST"])
def login():
    form = updateForm()
    if form.validate_on_submit():
        flash('Posted')
        posts.append({"author" : form.name.data, "body" : form.text.data})
        return redirect('/Updates')
    return render_template('post.html', title='Sign In', form=form)

@app.route("/CodeTeamBestTeam")
def code_best(): # Returns html
    return render_template("home.html", the_title="Code Team Best Team")

@app.route("/Privacy")
def privacy(): # Returns html
    return render_template("privacy.html", the_title="Privacy Policy")

@app.route("/Login")
def sign_in():
    return render_template("login.html", the_title="Test")

if __name__ == "__main__":
    app.run(debug=True)
