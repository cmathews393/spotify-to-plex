from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from .web_ui import functions
from .confighandler import read_config, write_config
import os


app = Flask(__name__, static_url_path='/static')

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


def update_manual_match(track_element_id, match_id):
    # Logic to update your data storage with the manual match
    # This function should update the match so that future processing uses this information
    print(f"Updating manual match for {track_element_id} with {match_id}")
    return True

@app.route('/manual-match', methods=['POST'])
def manual_match():
    matches_json = web_functions.man_match()
    return jsonify(matches_json)

@app.route('/confirm-match', methods=['POST'])
def confirm_match():
    data = request.json  # Get the JSON data sent with the POST request
    track_element_id = data.get('trackElementId')
    selected_match_id = data.get('selectedMatchId')

    if not track_element_id or not selected_match_id:
        # Missing data, return an error
        return jsonify({"error": "Missing trackElementId or selectedMatchId"}), 400

    # Call the function to update the match with the provided IDs
    if update_manual_match(track_element_id, selected_match_id):
        return jsonify({"success": True}), 200
    else:
        # If updating the match fails for some reason
        return jsonify({"error": "Failed to update manual match"}), 500

@app.route('/update-manual-match', methods=['POST'])
def update_manual_match():
    data = request.json
    track_element_id = data.get('trackElementId')
    selected_match_id = data.get('selectedMatchId')

    # Here you would convert selected_match_id into track_name and artist_name
    # For this example, let's assume selected_match_id contains both separated by a delimiter
    track_name, artist_name = selected_match_id.split('|', 1)

    # Now, assuming man_match can also handle updating a match (or you have a similar function for this)
    success = Spotiplex.PlexService().update_match(track_name, artist_name)

    if success:
        return jsonify({"success": True, "message": "Manual match updated successfully."}), 200
    else:
        return jsonify({"success": False, "message": "Failed to update manual match."}), 500



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
