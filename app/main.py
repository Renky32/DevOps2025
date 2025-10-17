from flask import Flask, jsonify, request
import mysql.connector

DB_HOST = "103.16.116.159"
DB_PORT = 3306
DB_USER = "devops"
DB_PASSWORD = "ubaya"
DB_NAME = "movie"

app = Flask(__name__)

def get_db_conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

@app.get("/movies")
def get_movies():
    title = request.args.get("title", "")
    sql = "SELECT * FROM movies"
    params = ()
    if title:
        sql += " WHERE title LIKE %s"
        params = (f"%{title}%",)
    sql += " LIMIT 50;"
    try:
        conn = get_db_conn()
        cur = conn.cursor(dictionary=True) 
        cur.execute(sql, params)
        data = cur.fetchall()
        if not data:
            return jsonify({"message": f"Tidak ada movie dengan judul mengandung '{title}'"}), 404
        base_url = request.url_root.rstrip("/")
        for m in data:
            poster_filename = m.get("poster") or f"{m['id']}.jpg"
            m["poster_url"] = f"{base_url}/static/posters/{poster_filename}"
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

@app.route('/movies/<int:id>/poster', methods=['GET'])
def get_movie_poster(id):
    try:
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, tmdb_id, title, poster FROM movies WHERE id = %s", (id,))
        movie = cursor.fetchone()
        if not movie:
            return jsonify({"message": "Movie not found"}), 404
        
        base_url = request.url_root.rstrip("/")
        poster_filename = movie.get("poster") or f"{movie['id']}.jpg"
        
        return jsonify({
            "id": movie['id'],
            "tmdb_id": movie['tmdb_id'],
            "title": movie['title'],
            "poster_url": f"{base_url}/static/posters/{poster_filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)