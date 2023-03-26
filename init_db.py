import sqlite3

connection = sqlite3.connect("database.db")


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO exercise (name, body_group, description, video_link) VALUES (?, ?, ?, ?)",
    ("Tricep Pushdowns", "Triceps", "", "https://youtu.be/sss"),
)
cur.execute(
    "INSERT INTO exercise (name, body_group, description, video_link) VALUES (?, ?, ?, ?)",
    ("Bicep Curl", "Bicpes", "just curl", "https://youtu.be/sss"),
)

connection.commit()
connection.close()
