import random, os, sys
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensuring responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # Run the app on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

#sabka katega hmfgjh