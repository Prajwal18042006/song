from flask import Flask, request, jsonify, render_template
from pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)
pipeline = PredictionPipeline()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        song_name = request.form.get("song_name")
        n_recommendations = int(request.form.get("n_recommendations", 5))

        try:
            results = pipeline.recommend_songs(
                song_name=song_name,
                n_recommendations=n_recommendations
            )

            return render_template(
                "index.html",
                results=results.to_dict(orient="records"),
                song_name=song_name,
                n_recommendations=n_recommendations
            )

        except Exception as e:
            return render_template(
                "index.html",
                error=str(e),
                song_name=song_name,
                n_recommendations=n_recommendations
            )

    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        song_name = data.get("song_name")
        n_recommendations = int(data.get("n_recommendations", 5))

        if not song_name:
            return jsonify({"error": "song_name is required"}), 400

        results = pipeline.recommend_songs(song_name, n_recommendations)

        return jsonify(results.to_dict(orient="records"))
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# ---------------- PODCAST ROUTES ----------------
@app.route("/podcasts")
def podcasts():
    return render_template("podcasts.html")


@app.route("/podcast/tech-beats")
def podcast_tech_beats():
    return render_template("podcast_tech_beats.html")


@app.route("/podcast/music-history")
def podcast_music_history():
    return render_template("podcast_music_history.html")


@app.route("/podcast/artist-spotlight")
def podcast_artist_spotlight():
    return render_template("podcast_artist_spotlight.html")


@app.route("/podcast/sound-science")
def podcast_sound_science():
    return render_template("podcast_sound_science.html")


# ---------------- AUTH ROUTES ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Simple login logic (can be enhanced with database)
        username = request.form.get("username")
        password = request.form.get("password")
        # For demo purposes, accept any credentials
        return render_template("login.html", success=True, message="Login successful!")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Simple registration logic (can be enhanced with database)
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # For demo purposes, accept any registration
        return render_template("register.html", success=True, message="Registration successful!")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
