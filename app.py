import secrets
import sqlite3
import logging

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

app = Flask(__name__)
sess = Session(app)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.config.from_pyfile("config.py")
    app.config["DATABASE"] = "database.db"
    sess.init_app(app)

    app.run()


@app.route("/register", methods=["GET", "POST"])
def register():
    """Defines registration page route and method."""
    if request.method != "POST":
        # render registration page
        return render_template("register.html")

    # handle form submission
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # validate form data
    if not (email and password and confirm_password and name):
        error_msg = "Please fill out all fields."
    elif password != confirm_password:
        error_msg = "Passwords do not match."
    else:
        # save user data to database
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (email, name, generate_password_hash(password)),
            )
            conn.commit()
        flash("Registration successful.")
        return redirect(url_for("login"))

    # render registration page with error message
    return render_template("register.html", error=error_msg)


# define login page route and method
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check user credentials and login
        email = request.form["email"]
        password = request.form["password"]
        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        session["email"] = email
        return redirect(url_for("workouts"))
    else:
        # render login template
        return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password")
            return redirect(url_for("index"))
        session["email"] = user["email"]
        return redirect(url_for("workouts"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("index"))


@app.route("/workouts/create", methods=["GET", "POST"])
def create_workout():
    if request.method == "POST":
        workout_name = request.form["workout_name"]
        body_group = request.form["body_group"]
        email = session.get("email")

        if not workout_name:
            flash("Workout name is required.")
        elif not body_group:
            flash("Body group is required.")
        elif not email:
            flash("Email is required.")
        else:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO workout (workout_name, body_group, email) VALUES (?, ?, ?)",
                    (workout_name, body_group, email),
                )
                conn.commit()
            flash("Workout created successfully.")

        return redirect(url_for("index"))
    else:
        return render_template("create_workout.html")


@app.route("/workouts")
def workouts():
    conn = get_db_connection()
    workouts = conn.execute("SELECT * FROM workout").fetchall()
    conn.close()
    return render_template("workouts.html", workouts=workouts)


@app.route("/sets/create", methods=["GET", "POST"])
def create_set():
    if request.method == "POST":
        weight = request.form["weight"]
        reps = request.form["reps"]
        exercise_id = request.form["exercise_id"]
        workout_id = request.form["workout_id"]

        if not weight:
            flash("Weight is required.")
        elif not reps:
            flash("Reps are required.")
        elif not exercise_id:
            flash("Exercise ID is required.")
        elif not workout_id:
            flash("Workout ID is required.")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO sets (weight, reps, exercise_id, workout_id) VALUES (?, ?, ?, ?)",
                (weight, reps, exercise_id, workout_id),
            )
            conn.commit()
            conn.close()
            flash("Set created successfully.")
            return redirect(url_for("index"))

    conn = get_db_connection()
    exercises = conn.execute("SELECT exercise_id, name FROM exercise").fetchall()
    workouts = conn.execute("SELECT workout_id, workout_name FROM workout").fetchall()
    conn.close()

    return render_template("create_set.html", exercises=exercises, workouts=workouts)


@app.route("/exercises/create", methods=["GET", "POST"])
def create_exercise():
    if request.method == "POST":
        name = request.form["name"]
        body_group = request.form["body_group"]
        description = request.form["description"]
        video_link = request.form["video_link"]

        if not name:
            flash("Exercise name is required.")
        elif not body_group:
            flash("Body group is required.")
        elif not description:
            flash("Description is required.")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO exercise (name, body_group, description, video_link) VALUES (?, ?, ?, ?)",
                (name, body_group, description, video_link),
            )
            conn.commit()
            conn.close()
            flash("Exercise created successfully.")
            return redirect(url_for("index"))

    return render_template("create_exercise.html")


def get_db_connection():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/workouts/<int:workout_id>/log_sets", methods=["GET", "POST"])
def log_sets(workout_id):
    with get_db_connection() as conn:
        workout = conn.execute(
            "SELECT * FROM workout WHERE workout_id = ?", (workout_id,)
        ).fetchone()
        exercises = conn.execute("SELECT * FROM exercise").fetchall()

    if request.method != "POST":
        return render_template("log_sets.html", workout=workout, exercises=exercises)

    exercise_id = request.form["exercise"]
    weight = request.form["weight"]
    reps = request.form["reps"]

    if not exercise_id:
        flash("Exercise is required.")
    elif not weight:
        flash("Weight is required.")
    elif not reps:
        flash("Reps are required.")
    else:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO sets (weight, reps, exercise_id, workout_id) VALUES (?, ?, ?, ?)",
                (weight, reps, exercise_id, workout_id),
            )
            conn.commit()

        flash("Sets logged successfully.")

    return redirect(url_for("view_workout", workout_id=workout_id))
