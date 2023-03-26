from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
app.config["DATABASE"] = "database.db"

# import necessary modules
from flask import Flask, render_template, request, redirect, url_for

# initialize Flask app
app = Flask(__name__)

# define registration page route and method
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # handle form submission
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # validate form data
        if not (username and email and password and confirm_password):
            error_msg = "Please fill out all fields."
        elif password != confirm_password:
            error_msg = "Passwords do not match."
        else:
            # TODO: Add code to save user data to database
            return redirect(url_for("login"))

        # render registration page with error message
        return render_template("register.html", error=error_msg)
    else:
        # render registration page
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check user credentials and login
        # Redirect to main page on success
        return redirect(url_for("index"))
    else:
        # Render login template
        return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM person WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password")
            return redirect(url_for("index"))
        session["user_id"] = user["email"]
        return redirect(url_for("workouts"))
    return render_template("login.html")


@app.route("/workouts/create", methods=["GET", "POST"])
def create_workout():
    if request.method == "POST":
        workout_name = request.form["workout_name"]
        body_group = request.form["body_group"]
        email = request.form["email"]

        if not workout_name:
            flash("Workout name is required.")
        elif not body_group:
            flash("Body group is required.")
        elif not email:
            flash("Email is required.")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO workout (workout_name, body_group, email) VALUES (?, ?, ?)",
                (workout_name, body_group, email),
            )
            conn.commit()
            conn.close()
            flash("Workout created successfully.")
            return redirect(url_for("index"))

    return render_template("create_workout.html")


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
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/workouts/<int:workout_id>/log_sets", methods=["GET", "POST"])
def log_sets(workout_id):
    conn = get_db_connection()
    workout = conn.execute(
        "SELECT * FROM workout WHERE workout_id = ?", (workout_id,)
    ).fetchone()
    exercises = conn.execute("SELECT * FROM exercise").fetchall()
    conn.close()

    if request.method == "POST":
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
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO sets (weight, reps, exercise_id, workout_id) VALUES (?, ?, ?, ?)",
                (weight, reps, exercise_id, workout_id),
            )
            conn.commit()
            conn.close()
            flash("Sets logged successfully.")
            return redirect(url_for("view_workout", workout_id=workout_id))

    return render_template("log_sets.html", workout=workout, exercises=exercises)


if __name__ == "__main__":
    app.run(debug=True)
