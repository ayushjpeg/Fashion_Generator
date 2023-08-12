from flask import Flask, redirect, render_template, request, session
import nltk
from nltk.chat.util import Chat, reflections
import requests
from flask_session import Session
from bs4 import BeautifulSoup
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from support import Fashion_array
import sqlite3

def search_flipkart(query):
    url = f'https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def fetch_product_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product details (customize based on the actual structure)
    product_title = soup.find('span', {'class': 'B_NuCI'}).text
    product_price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text
    product_image = soup.find('img', {'class': '_2r_T1I _396QI4'})['src']
    

    return {
        'title': product_title,
        'price': product_price,
        'image': product_image,
        'link' : link,
    }

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
    global entries  
    if request.method == "POST":
        s = request.form.get("Entry")
        entries.append("USER : "+s)
        response_of_bot = fashion_chatbot.respond(str(s))
        entries.append("BOT : "+response_of_bot)
        try:
            for pattern, _ in fashion_patterns:
                match = nltk.re.search(pattern, str(s))
                if match:
                    preference = match.group(1)
                    if preference:
                        if 'wear'  in pattern:
                            category = 'clothing'
                        elif 'color' in pattern:
                            category = 'colors'
                        elif 'material' in pattern:
                            category = 'materials'
                        elif 'style' in pattern:
                            category = 'styles'
                        elif 'brand' in pattern:
                            category = 'brands'
                        else:
                            category = 'other'  
                        user_preferences[category] = (preference)  
                        
                        entries.append(f"I'll remember that you enjoy {preference} in {category}.")
                    break
        except:
            entries.append("I was expecting something more detailed about your likings.")
        
        search_criteria = user_preferences
        print(search_criteria)
        search_query = ' '.join(search_criteria.values())
        search_results = search_flipkart(search_query)

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
        conn = sqlite3.connect("userdata.db")
        db = conn.cursor()
        
        
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        username_to_search = request.form.get("username")
        
        db.execute("SELECT * FROM users WHERE username = ?", (username_to_search,))
        
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
        conn = sqlite3.connect("userdata.db")
        db = conn.cursor()

        if (not request.form.get("username")) or request.form.get("username") == "" or request.form.get("username") == None:
            return apology("Username cannot be left blank")

        if (not request.form.get("password")) or request.form.get("password") == "" or request.form.get("password") == None:
            return apology("Password cannot be left blank")

        if (not request.form.get("confirmation")) or request.form.get("confirmation") == None:
            return apology("Password confirmation cannot be left blank")
        
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirm password dont match")

        username_to_search = request.form.get("username")
        db.execute("SELECT * FROM users WHERE username = ?", (username_to_search,))
        
        rows = db.fetchall()

        if len(rows) > 0:
            return apology("Username already exists")
        
        username = request.form.get("username")
        hashed_password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

        db.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = db.fetchone()[0]

        session["user_id"] = user_id
        
        conn.close()
        
        return redirect('/index')
    else:
        return render_template("register.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5050, debug=True)
