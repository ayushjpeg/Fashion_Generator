from flask import redirect, render_template, session
from functools import wraps
from bs4 import BeautifulSoup
import requests
import nltk


def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def fetch_product_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_title = soup.find('span', {'class': 'B_NuCI'}).text
    product_price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text
    product_image = soup.find('img', {'class': '_2r_T1I _396QI4'})['src']
    

    return {
        'title': product_title,
        'price': product_price,
        'image': product_image,
        'link' : link,
    }

def search_flipkart(query):
    url = f'https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def set_user_preferences(entries,user_preferences,fashion_patterns,s):
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
        return entries, user_preferences
