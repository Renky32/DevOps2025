from flask import Flask, jsonify
import mysql.connector

# ==== HARD-CODED SETTINGS (change here for your class) ====
DB_HOST = "103.16.116.159"
DB_PORT = 3306
DB_USER = "devops"
DB_PASSWORD = "ubaya"
DB_NAME = "movie"   # change if your DB name differs
# ==========================================================

app = Flask(__name__)

def get_db_conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

@app.route('/movies/<int:id>/poster', methods=['GET'])
def get_movie_poster(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, tmdb_id, title, poster FROM movies WHERE id = %s", (id,))
    movie = cursor.fetchone()
    cursor.close()
    db.close()
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    return jsonify({
        "id": movie['id'],
        "tmdb_id": movie['tmdb_id'],
        "title": movie['title'],
        "poster_url": movie['poster']  # pastikan kolom poster berisi full URL
    });