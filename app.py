from flask import Flask, redirect, render_template, request, session
import nltk
from nltk.chat.util import Chat, reflections
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, fetch_product_details, search_flipkart, set_user_preferences
from support import Fashion_array
import sqlite3

# Configure application
app = Flask(__name__, static_folder='static', template_folder='templates')


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
id = ''


# Variables
entries = []
user_preferences = {}
fashion_patterns = Fashion_array()
final_preferences = {
    'color':"",
    'item':[],
    'brands':[],
    'size':"M",
    'Gender':"",
    'Price_min':0,
    'Price_max':10000,
    'Name':"", 
}


# Chatbot config
fashion_chatbot = Chat(fashion_patterns, reflections)



# Ensuring responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/',methods=["GET","POST"])
def front():
    return render_template("front.html")



@app.route('/index',methods=["GET", "POST"])
def index(): 
    
    # Calling variables
    global entries, user_preferences, final_preferences, fashion_patterns
    
    
    if request.method == "POST":
        
        
        # Taking user input 
        s = request.form.get("Entry")
        entries.append("USER : "+s)
        
        
        # Generating bot's response
        response_of_bot = fashion_chatbot.respond(str(s))
        entries.append("BOT : "+response_of_bot)
        
        
        # Updating user_preferences as per the conversation
        entries, user_preferences = set_user_preferences(entries,user_preferences,fashion_patterns,str(s))
        print(user_preferences)
        
        
        # Generating flipkart buy link as per the preference
        search_query = ' '.join(user_preferences["clothing"])
        search_results = search_flipkart(search_query)


        # Extracting information from flipkart link to display on webpage
        top_links = []
        products = search_results.find_all('div', {'class': '_1AtVbE'})
        for product in products:
            link_element = product.find('a', {'class': 'IRpwTa'})
            if link_element:
                link = 'https://www.flipkart.com' + link_element['href']
                top_links.append(link)
        product_details = []
        for link in top_links:
            try:
                details = fetch_product_details(link)
                product_details.append(details)
            except:
                continue

        return render_template("index.html", entries=entries,product_details=product_details)

    else:
        entries=[]
        return render_template("index.html", entries=entries,  top_links=[])



@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        
        # Database
        conn = sqlite3.connect("fashion_database.db")
        db = conn.cursor()
        
        
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        username_to_search = request.form.get("username")
        
        db.execute("SELECT * FROM User WHERE username = ?", (username_to_search,))
        
        rows = db.fetchall()
        
        
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0][0]
        
        conn.close()
        
        return redirect("/index")
    else:
        return render_template("login.html")

 
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/index")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        
        
        # Database
        conn = sqlite3.connect("fashion_database.db")
        db = conn.cursor()

        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("All fields must be filled")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirm password don't match")

        username = request.form.get("username")
        name = request.form.get("name")
        gender = request.form.get("gender")
        age = request.form.get("age")
        hashed_password = generate_password_hash(request.form.get("password"))

        # Check if username already exists
        db.execute("SELECT * FROM User WHERE username = ?", (username,))
        rows = db.fetchall()
        if len(rows) > 0:
            return apology("Username already exists")

        # Insert user data into User table
        db.execute("INSERT INTO User (username, password, name, gender, age) VALUES (?, ?, ?, ?, ?)",
                (username, hashed_password, name, gender, age))
        conn.commit()

        # Fetch the user_id of the newly inserted user
        db.execute("SELECT id FROM User WHERE username = ?", (username,))
        user_id = db.fetchone()[0]

        session["user_id"] = user_id

        conn.close()
        
        return redirect('/index')
    else:
        return render_template("register.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8080, debug=True)
