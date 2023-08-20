from flask import redirect, render_template, session
from functools import wraps
from bs4 import BeautifulSoup
import requests
import nltk
from support import Fashion_array
from random import shuffle
import re
from nltk.corpus import stopwords

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
    for i in ['_396cs4 _2amPTt _3qGmMb', '_2r_T1I _396QI4']:
        try:
            product_image = soup.find('img', {'class':i})['src']
            break
        except:
            continue
    

    return {
        'title': product_title,
        'price': product_price,
        'image': product_image,
        'link' : link,
    }


def probabilistic_ranking_with_array(item_list, probability_array):
    ranked_items = {}

    for idx, probabilities in enumerate(probability_array, start=1):
        total_probability = sum(probabilities)
        average_probability = total_probability / len(probabilities)

        for item, probability in zip(item_list, probabilities):
            ranked_items[item] = ranked_items.get(item, 0) + probability / average_probability * idx

    sorted_items = sorted(ranked_items.items(), key=lambda x: x[1], reverse=True)
    final_ranked_items = {item[0]: rank for rank, (item, _) in enumerate(sorted_items, start=1)}

    return final_ranked_items
def search_flipkart(final_preferences,global_info):
        print(final_preferences)
        collection = []
        if "items" in final_preferences:
            query = final_preferences["items"].title().replace(" ", "%2B")
        else:
            query = None
            final_preferences["items"] = None
            return collection
        if "color" in final_preferences:
            color = final_preferences["color"]
        else:
            color = None
            final_preferences["color"] = None
        if "brand" in final_preferences:
            brand = final_preferences["brand"]
        else:
            brand = None
            final_preferences["brand"] = None
        if "size" in final_preferences:
            size = final_preferences["size"]
        else:
            size = None
            final_preferences["size"] = None
        if "gender" in final_preferences:
            gender = final_preferences["gender"]
        else:
            gender = None
            final_preferences["gender"] = None
        if "price_min" in final_preferences:
            price_min = final_preferences["price_min"]
        else:
            price_min = 0
            final_preferences["price_min"] = 0
        if "price_max" in final_preferences:
            price_max = final_preferences["price_max"]
        else:
            price_max = 10000
            final_preferences["price_max"] = 10000

        base_url = 'https://www.flipkart.com/search?q='
        query_params = '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

        filters = []

        if color:
            filters.append(f'p%5B%5D=facets.color%255B%255D%3D{color.title().replace(" ", "%2B")}')

        if brand:
            filters.append(f'p%5B%5D=facets.brand%255B%255D%3D{brand.title().replace(" ", "%2B")}')

        if size:
            filters.append(f'p%5B%5D=facets.size%255B%255D%3D{size}')

        if global_info["gender"] == "male":
            if global_info["age"] < 16:
                filters.append(f'p%5B%5D=facets.ideal_for%255B%255D%3DBoys')
            else:
                filters.append(f'p%5B%5D=facets.ideal_for%255B%255D%3DMen')
        elif global_info["gender"] == "female":
            if global_info["age"] < 16:
                filters.append(f'p%5B%5D=facets.ideal_for%255B%255D%3DGirls')
            else:
                filters.append(f'p%5B%5D=facets.ideal_for%255B%255D%3DWomen')

        if price_min > 0:
            filters.append(f'p%5B%5D=facets.price_range.from%3D{int(price_min)}&p%5B%5D=facets.price_range.to%3DMax')

        if price_max < 10000:
            filters.append(f'p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D{int(price_max)}')

        filters_query = '&'.join(filters)

        full_url = f'{base_url}{query}{query_params}&{filters_query}'
        print(full_url)

        response = requests.get(full_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        collection.append([soup,final_preferences])
        shuffle(collection)
        return collection

def set_user_preferences(entries,user_preferences,s):
            for item in Fashion_array()[0]:
                match = nltk.re.search(item.lower(), str(s).lower())
                if match:
                    dont_check1 = nltk.re.search("dont", str(s).lower())
                    dont_check2 = nltk.re.search("donot", str(s).lower())
                    dont_check3 = nltk.re.search("do not", str(s).lower())
                    if dont_check1 or dont_check2 or dont_check3:
                        user_preferences["dont_recommend"] = item
                        entries.append([f"I'll make sure i dont show you {item}.",0])
                    else:
                        user_preferences["items"] = item
                        entries.append([f"I'll remember that you like {item}.",0])
                        for item in Fashion_array()[1]:
                            match = nltk.re.search(item.lower(), str(s).lower())
                            if match:
                                dont_check1 = nltk.re.search("dont", str(s).lower())
                                dont_check2 = nltk.re.search("donot", str(s).lower())
                                dont_check3 = nltk.re.search("do not", str(s).lower())
                                if dont_check1 or dont_check2 or dont_check3:
                                    user_preferences["dont_recommend"] = item
                                    entries.append([f"I'll make sure i dont show you {item}.",0])
                                else:
                                    user_preferences["color"] = item
                                    entries.append([f"Got it! {item} is your favorite color.",0])
                                    break
                        for item in Fashion_array()[2]:
                            match = nltk.re.search(item.lower(), str(s).lower())
                            if match:
                                dont_check1 = nltk.re.search("dont", str(s).lower())
                                dont_check2 = nltk.re.search("donot", str(s).lower())
                                dont_check3 = nltk.re.search("do not", str(s).lower())
                                if dont_check1 or dont_check2 or dont_check3:
                                    user_preferences["dont_recommend"] = item
                                    entries.append([f"I'll make sure i dont show you {item}. Products",0])
                                else:
                                    user_preferences["brand"] = item
                                    entries.append([f"I will include {item} products.",0])
                                    break
                        match = nltk.re.search("less", str(s).lower())
                        if match:
                            words = nltk.word_tokenize(str(s))
                            words = [word for word in words if word.lower() not in stopwords.words('english')]

                            # Check if "less" is in the words list
                            if "less" in words:
                                for word in words:
                                    # Use regular expression to match numbers
                                    match = re.search(r'\d+', word)
                                    if match:
                                        number = float(match.group())
                                        user_preferences["price_max"] = number
                            if "more" in words:
                                for word in words:
                                    # Use regular expression to match numbers
                                    match = re.search(r'\d+', word)
                                    if match:
                                        number = float(match.group())
                                        user_preferences["price_min"] = number

                        break
            return entries, user_preferences
