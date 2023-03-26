DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS workout;
DROP TABLE IF EXISTS sets;
CREATE TABLE exercise (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    body_group TEXT NOT NULL,
    description TEXT NOT NULL,
    video_link TEXT
);
CREATE TABLE person (
    email TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
CREATE TABLE sets (
    set_id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actual_plan INTEGER NOT NULL,
    exercise_id INTEGER,
    workout_id INTEGER,
    FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id),
    FOREIGN KEY(workout_id) REFERENCES workout(workout_id)
);
CREATE TABLE workout (
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_name TEXT NOT NULL,
    body_group TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (email) REFERENCES person(email)
);