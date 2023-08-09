import random, os, sys
from flask import Flask, redirect, render_template, request
import nltk
from nltk.chat.util import Chat, reflections

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Variables
fashion_patterns = [
    (r'hi|hello', ['Hello!', 'Hi there!', 'Hey!']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!']),
    (r'my favorite color is (.*)', ['That\'s a nice color choice!', 'I like that color too.']),
    (r'I like to wear (.*)', ['That\'s a great choice of clothing!', 'Nice preference!']),
    (r'I prefer (.*) brands', ['Brands are important! Which brands do you like?', 'Tell me more about your favorite brands.']),
    (r'I love (.*) style', ['Styles say a lot about a person! Could you elaborate on that?', 'Interesting! What do you like about that style?']),
    (r'(.*)', ['I hear you. Tell me more about fashion.', 'Fashion is fascinating! Could you tell me more?'])
]

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
