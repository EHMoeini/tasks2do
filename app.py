from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, abort
from forms import RegisterForm, LoginForm, TaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, logout_user, login_user, current_user, UserMixin
from functools import wraps
from datetime import datetime, timedelta
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('FLASK_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///task_manager.db")

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

def not_logged_in_only(func):
    @wraps(func)
    def inner_function(*arg, **kwargs):
        if current_user.is_authenticated:
            flash("user already logged in!", "warning")
            return redirect(url_for("home_page"))
        return func(*arg, **kwargs) 
    return inner_function

def logged_in_only(func):
    @wraps(func)
    def inner_function(*arg, **kwargs):
        if not current_user.is_authenticated:
            flash("user not logged in!", "warning")
            return redirect(url_for("home_page"))
        return func(*arg, **kwargs) 
    return inner_function


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(500), nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    done_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)


@app.route("/")
def home_page():
    return render_template("home_page.html", login_status=current_user.is_authenticated)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("user has been logged out!", "warning")
    return redirect(url_for("home_page"))

@app.route("/register", methods=["POST", "GET"])
@not_logged_in_only
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data.strip()
            raw_password = form.password.data.strip()
            if (User.query.filter(User.username == username).first()):
                flash("user already exists!", "danger")
                return render_template("register.html", form=form), 409
            new_user = User(username=username, password=generate_password_hash(raw_password, method="pbkdf2:sha256", salt_length=8))
            try:
                db.session.add(new_user)
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({"error": "Database error"}), 500
            else:
                login_user(new_user, remember=True)
                flash("user was created successfully!", "success")
                return redirect(url_for("home_page"))

    return render_template("register.html", form=form), 200

@app.route("/login", methods=["POST", "GET"])
@not_logged_in_only
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data.strip()
            password = form.password.data.strip()
            user = User.query.filter(User.username == username).first()

            if not user:
                flash("user not found!", "danger")
                return render_template("login.html", form=form), 401
            elif not check_password_hash(user.password, password):
                form.password.errors.append("Incorrect password. Please try again.")
                return render_template("login.html", form=form), 401
            else:
                login_user(user, remember=True)
                flash("Logged in successfully!", "success")
                return redirect(url_for("home_page"))

    return render_template("login.html", form=form), 200

@app.route("/tasks")
@logged_in_only
def show_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = 10   

    filter_args = {k: v for k, v in request.args.items() if k != 'page'}

    query = Task.query.filter_by(user_id=current_user.id)

    category_filter = request.args.get('category', '').strip()
    if category_filter:
        query = query.filter(Task.category.ilike(f'%{category_filter}%'))

    if request.args.get('undone_only') == 'yes':
        query = query.filter(Task.done == False)

    if request.args.get('date_from'):
        date_from = datetime.strptime(request.args.get('date_from'), '%Y-%m-%d')
        query = query.filter(Task.date >= date_from)
    if request.args.get('date_to'):
        date_to = datetime.strptime(request.args.get('date_to'), '%Y-%m-%d')
        date_to = date_to.replace(hour=23, minute=59, second=59)
        query = query.filter(Task.date <= date_to)

    if request.args.get('deadline_from'):
        dl_from = datetime.strptime(request.args.get('deadline_from'), '%Y-%m-%d')
        query = query.filter(Task.deadline >= dl_from)
    if request.args.get('deadline_to'):
        dl_to = datetime.strptime(request.args.get('deadline_to'), '%Y-%m-%d')
        dl_to = dl_to.replace(hour=23, minute=59, second=59)
        query = query.filter(Task.deadline <= dl_to)
    
    sort_by = request.args.get('sort', 'date_desc')
    if sort_by == 'date_asc':
        query = query.order_by(Task.date.asc())
    elif sort_by == 'date_desc':
        query = query.order_by(Task.date.desc())
    elif sort_by == 'deadline_asc':
        query = query.filter(Task.deadline.isnot(None)).order_by(Task.deadline.asc())
    elif sort_by == 'deadline_desc':
        query = query.filter(Task.deadline.isnot(None)).order_by(Task.deadline.desc())
    elif sort_by == 'title_asc':
        query = query.order_by(Task.title.asc())
    else:
        query = query.order_by(Task.date.desc())

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    tasks = paginated.items
    total_pages = paginated.pages
    current_page = paginated.page

    return render_template("show_tasks.html",
                           tasks=tasks,
                           pagination={
                               'current': current_page,
                               'total': total_pages,
                               'has_prev': paginated.has_prev,
                               'has_next': paginated.has_next
                           },
                           filter_args=filter_args,
                           current_date=datetime.now()), 200
                           
@app.route("/tasks/add", methods=["POST","GET"])
@logged_in_only
def add_task():
    form = TaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            deadline = form.deadline.data if form.has_deadline.data else None
            new_task = Task(title=form.title.data.strip(),
                            description=form.description.data,
                            category=form.category.data.strip(),
                            deadline=deadline,
                            date=datetime.now(),
                            user_id=current_user.id)
            try:
                db.session.add(new_task)
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({"error": "Database error"}), 500
            else:
                return redirect(url_for("show_tasks"))
    return render_template("add_task.html", form=form, is_edit=False), 200

@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@logged_in_only
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return abort(403)

    if task.done:
        flash("Completed tasks cannot be edited.", 'warning')
        return redirect(url_for("show_tasks"))

    form = TaskForm(obj=task)
    
    # For GET requests, sync the checkbox with the existence of a deadline
    if request.method == 'GET':
        form.has_deadline.data = (task.deadline is not None)
    
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = form.description.data
        task.category = form.category.data.strip()
        if form.has_deadline.data:
            task.deadline = form.deadline.data
        else:
            task.deadline = None
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({"error": "Database error"}), 500
        else:
            flash('Task updated successfully!', 'success')
            return redirect(url_for('show_tasks'))
    
    return render_template('add_task.html', form=form, task=task, is_edit=True), 200

@app.route("/tasks/delete/<int:task_id>", methods=["DELETE"])
@logged_in_only
def delete_task(task_id):
    task = Task.query.filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500


@app.route("/tasks/done/<int:task_id>", methods=["PATCH"])
@logged_in_only
def done_task(task_id):
    task = Task.query.filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    try:
        task.done = True
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500


if __name__ == "__main__":
    app.run(debug=False)