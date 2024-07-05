from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5  # pip install bootstrap-flask

app = Flask(__name__)
app.secret_key = "gatdmxmvLvo81653j!ksd"
bootstrap = Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class TaskList(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_text: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    checked: Mapped[bool] = mapped_column(Boolean, default=False)  # Add checked column


with app.app_context():
    db.create_all()


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
        new_task = TaskList(
            task_text=form.task_text.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    all_tasks = db.session.execute(db.select(TaskList).order_by(TaskList.id)).scalars().all()
    return render_template('index.html', form=form, all_tasks=all_tasks)


@app.route('/update-task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = db.get_or_404(TaskList, task_id)
    task.checked = not task.checked
    db.session.commit()
    return jsonify({'success': True})


# @app.route("/new_list")
# def new_list():
#     global tasks
#     tasks = []
#     return redirect(url_for('home'))
#

@app.route('/delete-task')
def delete():
    task_id = request.args.get("task_id")
    print(task_id)
    task_to_delete = db.get_or_404(TaskList, task_id)
    print(task_to_delete)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True, port=5001)


