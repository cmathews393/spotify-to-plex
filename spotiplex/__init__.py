from flask import Flask, render_template
from .web_ui import functions

app = Flask(__name__)


@app.route("/")
def home():
    web_functions = functions()
    data = web_functions.get_dashboard_data()
    return render_template("index.html.j2", data=data)


@app.route("/settings")
def settings():
    return render_template("settings.html.j2")


@app.route("/playlists")
def playlists():
    return render_template("playlists.html.j2")


# @app.route('')

if __name__ == "__main__":
    app.run(debug=True)
