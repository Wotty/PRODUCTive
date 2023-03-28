import datetime
from flask import Flask, flash, render_template, request, redirect, url_for, session
import sqlite3
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect("fitness.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()
sess = Session()

# Define routes
@app.route("/")
def index():
    # Display a list of workouts
    c.execute("SELECT * FROM workout")
    workouts = c.fetchall()
    return render_template("index.html", workouts=workouts)


# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash password
        password_hash = generate_password_hash(password)

        # Insert user data into database
        c.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()

        # Log user in
        session["email"] = email

        # Redirect to homepage
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


# User login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        email = request.form["email"]
        password = request.form["password"]

        # Check if user exists
        user = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            # Log user in
            session["email"] = email
            print(email)
            # Redirect to homepage
            return redirect(url_for("index"))
        else:
            # Show error message
            flash("Invalid email or password.")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # remove the email from the session
    session.pop("email", None)
    # redirect to the index page
    return redirect(url_for("index"))


@app.route("/create_workout", methods=["GET", "POST"])
def create_workout():
    if request.method == "POST":
        # Insert the new workout into the database
        workout_name = request.form["workout_name"]
        body_group = request.form["body_group"]
        email = session["email"]
        c.execute(
            "INSERT INTO workout (workout_name, body_group, email) VALUES (?, ?, ?)",
            (workout_name, body_group, email),
        )
        conn.commit()
        return redirect(url_for("index"))
    else:
        # Display a form to add a new workout
        return render_template("create_workout.html")


@app.route("/create_exercise", methods=["GET", "POST"])
def create_exercise():
    if request.method == "POST":
        # Insert the new exercise into the database
        name = request.form["name"]
        body_group = request.form["body_group"]
        description = request.form["description"]
        video_link = request.form["video_link"]
        c.execute(
            "INSERT INTO exercise (name, body_group, description, video_link) VALUES (?, ?, ?, ?)",
            (name, body_group, description, video_link),
        )
        conn.commit()
        return redirect(url_for("index"))
    else:
        # Display a form to add a new exercise
        return render_template("create_exercise.html")


@app.route("/workout/<int:workout_id>")
def view_workout(workout_id):
    # Display the details of a specific workout
    c.execute("SELECT * FROM workout WHERE workout_id = ?", (workout_id,))
    workout = c.fetchone()
    c.execute(
        "SELECT exercise.*, sets.weight, sets.reps FROM exercise JOIN sets ON exercise.exercise_id = sets.exercise_id WHERE sets.workout_id = ?",
        (workout_id,),
    )
    exercises = c.fetchall()
    return render_template("workout.html", workout=workout, exercises=exercises)


@app.route("/edit_workout/<int:workout_id>", methods=["GET", "POST"])
def edit_workout(workout_id):
    workout = c.execute(
        "SELECT * FROM workout WHERE workout_id = ?", (workout_id,)
    ).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        body_group = request.form["body_group"]

        c.execute(
            "UPDATE workout SET workout_name = ?, email = ?, body_group = ? WHERE workout_id = ?",
            (
                name,
                email,
                body_group,
                workout_id,
            ),
        )
        flash("Workout updated successfully", "success")
        return redirect(url_for("view_workout", workout_id=workout_id))
    return render_template("edit_workout.html", workout=workout)


@app.route("/delete_workout/<int:workout_id>", methods=["POST"])
def delete_workout(workout_id):
    c.execute("DELETE FROM workout WHERE workout_id = ?", (workout_id,))
    conn.commit()
    flash("Workout deleted successfully", "success")
    return redirect(url_for("index"))


@app.route("/create_set", methods=["POST", "GET"])
def create_set():

    if request.method == "POST":
        # Insert the new exercise into the database
        weight = request.form["weight"]
        reps = request.form["reps"]
        exercise_id = request.form["exercise_id"]
        workout_id = request.form["workout_id"]
        c.execute(
            "INSERT INTO sets (weight, reps, exercise_id, workout_id) VALUES (?, ?, ?, ?)",
            (weight, reps, exercise_id, workout_id),
        )
        conn.commit()
        return redirect(url_for("view_workout", workout_id=workout_id))
    else:
        # Display a list of workouts
        c.execute("SELECT * FROM workout")
        workouts = c.fetchall()
        c.execute("SELECT * FROM exercise")
        exercises = c.fetchall()
        # Display a form to add a new exercise
        return render_template(
            "create_set.html", workouts=workouts, exercises=exercises
        )

    # Insert a new set into the database


# Run the application
if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = "super d key"
    app.config["SESSION_TYPE"] = "filesystem"

    sess.init_app(app)

    app.debug = True
    app.run()
