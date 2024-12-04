from datetime import timedelta
from typing import Union
from sqlalchemy.orm import DeclarativeBase
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bootstrap = Bootstrap5(app)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


class TaskForm(FlaskForm):
    task_text = StringField("Write your task and click 'ADD':", validators=[DataRequired()])
    submit = SubmitField('ADD')


@app.route("/", methods=['GET', 'POST'])
def home() -> Union[str, Response]:
    form = TaskForm(request.form)
    if 'tasks' not in session:
        session['tasks'] = []
    if form.validate_on_submit():
        task = {
            'text': form.task_text.data,
            'checked': False
        }
        session['tasks'].append(task)
        return redirect(url_for('home'))
    return render_template('index.html', form=form, all_tasks=session['tasks'])


@app.route('/update-task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if session['tasks'][task_id]['checked']:
        session['tasks'][task_id]['checked'] = False
    else:
        session['tasks'][task_id]['checked'] = True
    session.modified = True
    return jsonify({'success': True})


@app.route('/delete-task')
def delete():
    task_id = int(request.args.get("task_id"))
    session['tasks'].pop(task_id)
    session.modified = True
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)


