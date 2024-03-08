#!/bin/bash

# Ensure the script is executed from the correct directory
# This script should be run from the root of your project structure

# Creating necessary directories if they don't already exist
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img
mkdir -p templates

# Creating placeholder files for Flask
# Base HTML template
cat > templates/base.html.j2 << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spotiplex</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
EOF

# Home page HTML template
cat > templates/index.html.j2 << EOF
{% extends "base.html.j2" %}

{% block content %}
<h1>Welcome to Spotiplex</h1>
{% endblock %}
EOF

# Placeholder CSS
cat > static/css/style.css << EOF
body {
    font-family: Arial, sans-serif;
}
EOF

# Placeholder main.py (if not already present in spotiplex)
if [ ! -f spotiplex/main.py ]; then
cat > spotiplex/main.py << EOF
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html.j2')

if __name__ == "__main__":
    app.run(debug=True)
EOF
fi

echo "Flask app structure is set up. You can now run the app using 'flask run' or 'python -m flask run'."
