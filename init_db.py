import sqlite3

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect("fitness.db", check_same_thread=False)
c = conn.cursor()

c.execute(" DROP TABLE IF EXISTS sets;")
c.execute("DROP TABLE IF EXISTS workout;")
c.execute("DROP TABLE IF EXISTS exercise;")
c.execute("DROP TABLE IF EXISTS users;")
# Create the exercise table
c.execute(
    """CREATE TABLE exercise (
                exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                body_group TEXT NOT NULL,
                description TEXT NOT NULL,
                video_link TEXT
             )"""
)

# Create the users table
c.execute(
    """CREATE TABLE users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL
             )"""
)

# Create the workout table
c.execute(
    """CREATE TABLE workout (
                workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_name TEXT NOT NULL,
                body_group TEXT NOT NULL,
                email TEXT,
                FOREIGN KEY (email) REFERENCES users(email)
             )"""
)

# Create the sets table
c.execute(
    """CREATE TABLE sets (
                set_id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                exercise_id INTEGER,
                workout_id INTEGER,
                FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id),
                FOREIGN KEY (workout_id) REFERENCES workout(workout_id)
             )"""
)
# Insert some sample exercises
exercises = [
    (
        "Squats",
        "Legs",
        "Squat down, keeping your back straight",
        "https://www.youtube.com/embed/ultWZbUMPL8",
    ),
    (
        "Bench Press",
        "Chest",
        "Lift the bar up and down while lying on a bench",
        "https://www.youtube.com/embed/OwJ-gx0UoSE",
    ),
    (
        "Deadlifts",
        "Back",
        "Lift the bar off the ground and stand up straight",
        "https://www.youtube.com/embed/op9kVnSso6Q",
    ),
    (
        "Pushups",
        "Chest",
        "Lower your body down to the ground and then push back up",
        "https://www.youtube.com/embed/IODxDxX7oi4",
    ),
    (
        "Pullups",
        "Back",
        "Lift your body up towards the bar and then lower back down",
        "https://www.youtube.com/embed/6kALZikXxLc",
    ),
]
c.executemany(
    "INSERT INTO exercise (name, body_group, description, video_link) VALUES (?, ?, ?, ?)",
    exercises,
)

# Insert some sample workouts
workouts = [
    ("Leg Day", "Legs", "william.otty@gmail.com"),
    ("Chest Day", "Chest", "william.otty@gmail.com"),
    ("Back Day", "Back", "william.otty@gmail.com"),
]
c.executemany(
    "INSERT INTO workout (workout_name, body_group, email) VALUES (?, ?, ?)", workouts
)

# populate sets table
sets_data = [
    (1, 1, 1, 1),
    (2, 1, 1, 2),
    (3, 1, 1, 2),
    (4, 2, 2, 1),
    (5, 2, 2, 1),
    (6, 2, 2, 1),
]

c.executemany(
    "INSERT INTO sets (weight, reps, exercise_id, workout_id) VALUES (?, ?, ?, ?)",
    sets_data,
)
# Commit the changes and close the connection
conn.commit()
conn.close()
