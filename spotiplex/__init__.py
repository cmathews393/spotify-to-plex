from flask import Flask, render_template, request, redirect, url_for, flash
from .web_ui import functions
from .confighandler import read_config, write_config
import os

app = Flask(__name__)

web_functions = functions()

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev")


@app.route("/")
def home():
    data = web_functions.get_dashboard_data()
    return render_template("index.html.j2", data=data)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        try:
            spotify_config = {
                "client_id": request.form.get("spotifyClientId"),
                "api_key": request.form.get("spotifyAPIKey"),
            }
            plex_config = {
                "url": request.form.get("plexURL"),
                "api_key": request.form.get("plexApiKey"),
            }
            lidarr_config = {
                "url": request.form.get("lidarrUrl"),
                "api_key": request.form.get("lidarrAPIKey"),
            }
            spotiplex_config = {
                "lidarr_sync": (
                    "True" if request.form.get("lidarrSync") == "True" else "False"
                ),
                "plex_users": request.form.get("plexUsers"),
                "worker_count": int(request.form.get("workerCount")),
                "seconds_interval": int(request.form.get("secondsInterval")),
                "manual_playlists": request.form.get("manualPlaylists"),
                "first_run": False,
            }

            write_config("spotify", spotify_config)
            write_config("plex", plex_config)
            write_config("lidarr", lidarr_config)
            write_config("spotiplex", spotiplex_config)

            flash("Settings successfully saved!", "success")
        except Exception as e:
            flash(f"Failed to save settings: {e}", "danger")

        return redirect(url_for("settings"))

    spotify_config = read_config("spotify")
    plex_config = read_config("plex")
    lidarr_config = read_config("lidarr")
    spotiplex_config = read_config("spotiplex")

    return render_template(
        "settings.html.j2",
        spotify_config=spotify_config,
        plex_config=plex_config,
        lidarr_config=lidarr_config,
        spotiplex_config=spotiplex_config,
    )


@app.route("/playlists")
def playlists_view():
    playlists = web_functions.get_playlists_data()
    return render_template("playlists.html.j2", playlists=playlists)

@app.route("/support")
def support_us():
    return render_template("support.html.j2")

# @app.route('')

if __name__ == "__main__":
    app.run(debug=True)
