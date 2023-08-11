import random, os, sys
from flask import Flask, redirect, render_template, request
import nltk
from nltk.chat.util import Chat, reflections
from support import Fashion_array
import re
import requests
from bs4 import BeautifulSoup



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
    }

# Configure application
app = Flask(__name__, static_folder='static', template_folder='templates')


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


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

@app.route('/',methods=["GET", "POST"])
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
                        # Determine the category based on the pattern used
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
                            category = 'other'  # Modify this as needed
                        user_preferences[category] = (preference)  # Store the preference in the dictionary
                        
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


@app.route('/search/<query>')
def search(query):
    # Fetch search results from Flipkart
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://www.flipkart.com/search?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product details
    product_details = []
    for product in soup.select('.YOUR_PRODUCT_CLASS_NAME'):
        title = product.text
        link = product.find('a')['href']
        product_details.append({'title': title, 'link': link})
    print(product_details, query)

    return render_template('search_results.html', query=query, results=product_details)
 




if __name__ == '__main__':
    # Run the app on all network interfaces on port 5000
    app.run(host='0.0.0.0',port = 5050, debug=True)
