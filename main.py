from datetime import timedelta
from typing import Union
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bootstrap = Bootstrap5(app)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    """
    Handles CSRF (Cross-Site Request Forgery) errors.
    This function is triggered when a CSRF token is invalid or has expired.

    Args:
        e: The CSRFError exception object containing error details.

    Returns:
        A rendered template ('csrf_error.html') with a user-friendly message
        and a 400 HTTP status code (Bad Request).
    """
    return render_template("csrf_error.html", message="Session expired, please refresh the page."), 400


@app.before_request
def make_session_permanent() -> None:
    """
    Ensures the user session remains active and sets a custom session lifetime.
    This functions runs every request.
    """
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)


class TaskForm(FlaskForm):
    """
    A form for creating tasks in a to-do list application.
        This form includes:
        - task_text: A text field where users enter the task description.
        - submit: A submit button to add the task to the list.
    """
    task_text = StringField("Write your task and click 'ADD':", validators=[DataRequired()])
    submit = SubmitField('ADD')


@app.route("/", methods=['GET', 'POST'])
def home() -> Union[str, Response]:
    """
    Handles the main to-do list page, displaying tasks and processing new task submissions.

    Returns:
        Response: Redirects to the home page upon successful form submission.
        str: Renders the 'index.html' template with the current list of tasks.
    """
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
def update_task(task_id: int) -> Response:
    """
    Toggles the 'checked' status of a task in the session-based task list.

    Args:
        task_id (int): The index of the task to be updated.

    Returns:
        JSON response indicating success.
    """
    if session['tasks'][task_id]['checked']:
        session['tasks'][task_id]['checked'] = False
    else:
        session['tasks'][task_id]['checked'] = True
    session.modified = True
    return jsonify({'success': True})


@app.route('/delete-task')
def delete() -> Response:
    """
    Deletes a task from the session-based task list.

    This function retrieves the task ID from the request arguments, removes
    the corresponding task from the session's 'tasks' list, and redirects
    the user back to the home page.

    Parameters:
    None (task_id is retrieved from request.args)

    Returns:
    Redirect to the home route after deleting the task.
    """
    task_id = int(request.args.get("task_id"))
    session['tasks'].pop(task_id)
    session.modified = True
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
