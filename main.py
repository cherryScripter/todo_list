from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5  # pip install bootstrap-flask

app = Flask(__name__)
app.secret_key = "gatdmxmvLvo81653j!ksd"
bootstrap = Bootstrap5(app)


class TaskForm(FlaskForm):
    task_text = StringField("Write your task and click 'ADD':", validators=[DataRequired()])
    submit = SubmitField('ADD')


tasks = []

@app.route("/", methods=['GET', 'POST'])
def home():
    form = TaskForm(request.form)
    if form.validate_on_submit():
        task = form.task_text.data
        tasks.append(task)
        return redirect(url_for('home'))
    return render_template('index.html', form=form, tasks=tasks)


@app.route("/new_list")
def new_list():
    global tasks
    tasks = []
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)


