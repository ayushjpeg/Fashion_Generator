from flask import Flask, redirect, render_template, request, session
import nltk
from nltk.chat.util import Chat, reflections
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import random
import datetime
from helpers import apology, login_required, fetch_product_details, search_flipkart, set_user_preferences
from support import Fashion_array, trend_check
from Special_occassion import festives
from Trends_extraction import instagram

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
user_preferences = {
    "items":[],
    "color":"",
    "other":[],
    "brands":[],
    "dont_recommend":[],
}
product_details = []
history_details = []
trends_details = []
occasion_details = []
liking_details = []
flag = 0



# nltk replies
# fashion_patterns = Fashion_array()

final_preferences = {
    'color':"",
    'size':"M",
    'gender':"",
    'name':"",
    'location':"",
    'age':25,
}


# Chatbot config
# fashion_chatbot = Chat(fashion_patterns, reflections)


# Ensuring responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/',methods=["GET","POST"])
def front():
    global  final_preferences, product_details, entries
    session.clear()
    final_preferences = {
        'color': "",
        'size': "M",
        'gender': "",
        'name': "",
        'location': "",
        'age': 25,
    }
    product_details = list()
    entries = list()
    return render_template("front.html")



@app.route('/index',methods=["GET", "POST"])
def index(): 
    
    # Calling variables
    global entries,  final_preferences, product_details, history_details, liking_details

    print(final_preferences)
    
    if request.method == "POST":

        # Taking user input 
        s = request.form.get("Entry")
        entries.append("USER : "+s)

        # Generating bot's response
        # response_of_bot = fashion_chatbot.respond(str(s))
        # entries.append("BOT : "+response_of_bot)
        
        
        # Updating user_preferences as per the conversation
        entries, user_preferences = set_user_preferences(entries, {},str(s))

        
        if "dont_recommend" in user_preferences:
            temp = []
            for i in product_details:
                print(i)
                if i["color"] and i["color"].lower() == user_preferences["dont_recommend"].lower():
                    pass
                elif i["brand"] and i["brand"].lower() == user_preferences["dont_recommend"].lower():
                    pass
                elif i["items"] and i["items"].lower() == user_preferences["dont_recommend"].lower():
                    pass
                else:
                    temp.append(i)
            product_details = list(temp)

        # Generating flipkart buy link as per the preference
        search_results_list = search_flipkart(user_preferences,final_preferences)
        # print(search_results_list)

        # Extracting information from flipkart link to display on webpage
        top_links = []
        current_details = []
        for search_results in search_results_list:
            products = search_results[0].find_all('div', {'class': '_1AtVbE'})
            for product in products:
                for j in ['s1Q9rs','IRpwTa']:
                    link_element = product.find('a', {'class': j})
                    if link_element:
                        link = 'https://www.flipkart.com' + link_element['href']
                        top_links.append(link)

            for link in top_links:
                try:
                    details = fetch_product_details(link)
                    for i in search_results[1]:
                        details[i] = search_results[1][i]
                    current_details.append(details)
                except:
                    continue
        product_details += current_details
        liking_details += current_details
        random.shuffle(product_details)
        return render_template("index.html", entries=entries,product_details=product_details)

    else:
        entries=[]
        print(product_details)
        return render_template("index.html", entries=entries,  product_details=product_details)



@app.route("/login", methods=["GET", "POST"])
def login():

    global final_preferences, history_details, product_details, entries

    session.clear()
    final_preferences = {
        'color': "",
        'size': "M",
        'gender': "",
        'name': "",
        'location': "",
        'age': 25,
    }
    product_details = list()
    entries = list()

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

        db.execute("SELECT gender from USER where id = ?",(rows[0][0],))
        final_preferences["gender"] = db.fetchone()[0]

        db.execute("SELECT age from USER where id = ?", (rows[0][0],))
        final_preferences["age"] = db.fetchone()[0]

        db.execute("SELECT name from USER where id = ?", (rows[0][0],))
        final_preferences["name"] = db.fetchone()[0]
        # Extracting previous data 
        
        # Query History table
        db.execute('SELECT * FROM History')
        history_data = db.fetchall()
        print(history_data)
        
        # Query Likings table
        db.execute('SELECT * FROM Likings')
        likings_data = db.fetchall()


        
        # Updating using user data 
        for history_row in history_data:
            color, items, size, brands = history_row[2:6]
            final_preferences['color'] = color
            history_items = (items.split(','))
            history_brands = (brands.split(','))
            final_preferences['size'] = size
            print(history_brands,history_items)
            for i in history_items:
                for j in history_brands:
                    user_preferences ={}
                    user_preferences["items"] = i
                    user_preferences["brand"] = j
                    user_preferences["color"] = color
                    user_preferences["size"] = size
                    search_results_list = search_flipkart(user_preferences,final_preferences)
                    # print(search_results_list)

                    # Extracting information from flipkart link to display on webpage
                    top_links = []
                    current_details = []
                    for search_results in search_results_list:
                        products = search_results[0].find_all('div', {'class': '_1AtVbE'})
                        for product in products:
                            link_element = product.find('a', {'class': 'IRpwTa'})
                            if link_element:
                                link = 'https://www.flipkart.com' + link_element['href']
                                top_links.append(link)

                        for link in top_links:
                            try:
                                details = fetch_product_details(link)
                                for i in search_results[1]:
                                    details[i] = search_results[1][i]
                                current_details.append(details)
                            except:
                                continue
                    history_details += current_details
                    product_details += current_details
        # for likings_row in likings_data:
        #     color, dont_recommend, items = likings_row[2:5]
        #     final_preferences['color'] = color
        #     final_preferences['dont_recommend'].extend(dont_recommend.split(','))
        #     final_preferences['items'].extend(items.split(','))
            
        conn.close()
        
        return redirect("/index")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    
    global final_preferences, product_details, entries

    # Connect to the database
    conn = sqlite3.connect('fashion_database.db')
    cursor = conn.cursor()

    # Retrieve user_id from session
    user_id = session['user_id']

    # # Update History table
    # history_keys = ['style', 'color', 'items', 'size', 'brands']
    # history_entry = {key: final_preferences.get(key, '') for key in history_keys}
    # style = history_entry.get('style', '')
    # color = history_entry.get('color', '')
    # items = ','.join(history_entry.get('items', []))
    # size = history_entry.get('size', '')
    # brands = ','.join(history_entry.get('brands', []))
    # cursor.execute('''
    #     INSERT OR REPLACE INTO History (user_id, style, color, items, size, brands)
    #     VALUES (?, ?, ?, ?, ?, ?)
    # ''', (user_id, style, color, items, size, brands))

    # Update Likings table
    likings_keys = ['color', 'location', 'dont_recommend', 'items']
    likings_entry = {key: final_preferences.get(key, '') for key in likings_keys}
    color = likings_entry.get('color', '')
    location = likings_entry.get('location', '')
    dont_recommend = ','.join(likings_entry.get('dont_recommend', []))
    items = ','.join(likings_entry.get('items', []))
    cursor.execute('''
        INSERT OR REPLACE INTO Likings (user_id, color, location, dont_recommend, items)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, color, location, dont_recommend, items))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    session.clear()
    final_preferences = {
        'color': "",
        'size': "M",
        'gender': "",
        'name': "",
        'location': "",
        'age': 25,
    }
    product_details = list()
    entries = list()
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
        conn.commit()
        conn.close()
        
        return redirect('/index')
    else:
        return render_template("register.html")


@app.route('/history', methods=["GET", "POST"])
def history():
    if request.method == "POST":
        
        conn = sqlite3.connect('fashion_database.db')
        cursor = conn.cursor()
        
        user_id = session["user_id"]

        style = request.form.get('style')
        color = request.form.get('color')
        items = request.form.get('items').split(',')
        size = request.form.get('size')
        brands = request.form.get('brands').split(',')

        items_str = ','.join(items)
        brands_str = ','.join(brands)
        print(color,items,size,brands)
        cursor.execute('''
            INSERT OR REPLACE INTO History (user_id, style, color, items, size, brands)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, style, color, items_str, size, brands_str))
        
        # Print inserted data for testing
        cursor.execute("SELECT * FROM History WHERE user_id = ?", (user_id,))
        inserted_data = cursor.fetchone()
        print("Inserted Data:", inserted_data)
        conn.commit()
        conn.close()

        return redirect('/index')
    else:
        return render_template('history.html')


array_fashion = trend_check()
def trends():
    global trends_details, product_details
    ans = []
    for q_srch in range(0, len(array_fashion)):
        try:
            x = (instagram(q_srch))
            print(x)
            ans.append(x)
        except:
            continue

    ans.sort(key=lambda x:x[1])
    ans = ans[:5]
    for j in ans[::-1]:
        user_preferences = {}
        user_preferences["items"] = j[0]
        search_results_list = search_flipkart(user_preferences,final_preferences)

        # Extracting information from flipkart link to display on webpage
        top_links = []
        current_details = []
        for search_results in search_results_list:
            products = search_results[0].find_all('div', {'class': '_1AtVbE'})
            for product in products:
                link_element = product.find('a', {'class': 'IRpwTa'})
                if link_element:
                    link = 'https://www.flipkart.com' + link_element['href']
                    top_links.append(link)

            for link in top_links:
                try:
                    details = fetch_product_details(link)
                    for i in search_results[1]:
                        details[i] = search_results[1][i]
                    current_details.append(details)
                except:
                    continue
        trends_details += current_details
        product_details += current_details


def special_occasion():
    global occasion_details, product_details
    d = festives()
    for i in d:
        current=datetime.datetime.now()
        # print(i,current.month)
        if i["month"] == current.month:
            for j in i["items"]:
                user_preferences = {}
                user_preferences["items"] = j
                search_results_list = search_flipkart(user_preferences,final_preferences)

                # Extracting information from flipkart link to display on webpage
                top_links = []
                current_details = []
                for search_results in search_results_list:
                    products = search_results[0].find_all('div', {'class': '_1AtVbE'})
                    for product in products:
                        link_element = product.find('a', {'class': 'IRpwTa'})
                        if link_element:
                            link = 'https://www.flipkart.com' + link_element['href']
                            top_links.append(link)

                    for link in top_links:
                        try:
                            details = fetch_product_details(link)
                            for i in search_results[1]:
                                details[i] = search_results[1][i]
                            current_details.append(details)
                        except:
                            continue
                occasion_details += current_details
                product_details += current_details


if __name__ == '__main__':
    #special_occasion()
    #trends()
    app.run(host='0.0.0.0',port = 8080, debug=True)
