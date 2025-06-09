from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

import os
import requests

db_url = "https://www.dropbox.com/scl/fi/1ikhm2muo220tmhlt1tk4/movies.db?rlkey=tr7lo6dhh316qnstog5uzl528&st=spv9frtn&dl=1"
db_path = "movies.db"

def download_db():
    if not os.path.exists(db_path):
        print("Downloading movies.db from Dropbox...")
        response = requests.get(db_url)
        with open(db_path, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("movies.db already exists, skipping download.")

download_db()




@app.route('/all')
def get_paginated_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) FROM movies")
    total = cursor.fetchone()[0]

    # Get paginated records
    cursor.execute(f"SELECT * FROM movies LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()

    # Get column names
    col_names = [description[0] for description in cursor.description]
    conn.close()

    # Convert to list of dicts
    data = [dict(zip(col_names, row)) for row in rows]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    })

if __name__ == '__main__':
    app.run()