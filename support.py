import nltk
nltk.download('stopwords')
def Fashion_array():
    arr = [(r'hi|hello', ['Hello!', 'Hi there!', 'Hey!']),
        (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!']),
        (r'my favorite color is (.*)', ['That\'s a nice color choice!', 'I like that color too.']),
        (r'I like to wear (.*)', ['That\'s a great choice of clothing!', 'Nice preference!']),
        (r'I prefer (.*) brand', ['Brands are important! Which brands do you like?', 'Tell me more about your favorite brands.']),
        (r'I love (.*) style', ['Styles say a lot about a person! Could you elaborate on that?', 'Interesting! What do you like about that style?']),
        (r'I prefer (.*) brands', ['Brands are important! Which brands do you like?', 'Tell me more about your favorite brands.']),
        (r'material should be (.*)',['That is comfortable','Its a great choice for this season']),
        (r'I love (.*) style', ['Styles say a lot about a person! Could you elaborate on that?', 'Interesting! What do you like about that style?']),
        (r'my age is (\d+)', ['You\'re {} years old? Fashion preferences can change with age!', 'Age plays a role in fashion.']),
        (r'I live in (.*)', ['Living in {} sounds interesting! How does it influence your fashion choices?']),
        (r'(.*)', ['I hear you. Tell me more about fashion.', 'Fashion is fascinating! Could you tell me more?']),
    ]
    brands = [
        "Allen Solly", "Arrow", "Bata", "Biba", "FabIndia", "Forest Essentials", "Hidesign",
        "Indian Terrain", "Jockey", "Khadi", "Louis Philippe", "Manyavar", "Max Fashion",
        "Mufti", "Puma", "Ritu Kumar", "Satya Paul", "Van Heusen", "W for Woman", "Wills Lifestyle",
        "Zodiac", "Zara", "AND", "Anita Dongre", "Global Desi", "Amrapali", "Kalyan Jewellers",
        "PC Jeweller", "Swarovski", "Tanishq", "Titan", "Fastrack", "Rajesh Pratap Singh", "Shantanu & Nikhil",
        "Sabyasachi", "Rohit Bal", "Manish Malhotra", "Tarun Tahiliani", "Anita Dongre", "Ritu Beri",
        "Masaba Gupta", "Neeta Lulla", "Rocky S", "Abu Jani Sandeep Khosla", "Sunita Shekhawat",
        "Neerus", "Voylla", "Peora", "Chumbak", "ToniQ", "Zaveri Pearls", "Fossil", "Baggit",
        "Caprese", "Lavie", "Hush Puppies", "Woodland", "Clarks", "Catwalk", "Metro Shoes", "Steve Madden",
        "Van Heusen", "Khadim's", "Jabong", "Myntra", "Vero Moda", "Lakme", "Maybelline", "Colorbar",
        "Nykaa", "Revlon", "L'Oreal", "Pantaloons", "Levis", "Lee", "Wrangler", "Vans", "Converse",
        "Nike", "Adidas", "Puma", "Reebok", "Skechers", "Ray-Ban", "FastTrack", "Tommy Hilfiger",
        "Lavie", "Da Milano", "Baggit", "Fastrack", "Guess", "Gucci", "Prada", "Louis Vuitton",
        "Michael Kors", "Coach", "Aldo", "Clarks", "Crocs", "Swarovski", "Pandora", "Tiffany & Co."
    ]
    colors = [
        "White", "Black", "Gray", "Silver", "Charcoal", "Red", "Maroon", "Burgundy", "Pink", "Coral",
        "Orange", "Peach", "Yellow", "Gold", "Lemon", "Green", "Lime", "Olive", "Teal", "Turquoise",
        "Blue", "Navy", "Cobalt", "Indigo", "Violet", "Purple", "Lavender", "Magenta", "Fuchsia",
        "Brown", "Beige", "Tan", "Khaki", "Cream", "Ivory", "Mint", "Aqua", "Salmon", "Crimson",
        "Sky Blue", "Rust", "Sage", "Bronze", "Plum", "Lilac", "Apricot", "Terracotta", "Emerald",
        "Chocolate", "Sapphire", "Ruby", "Cyan", "Amber", "Aquamarine", "Cerulean", "Pearl", "Topaz",
        "Vermilion", "Turmeric", "Mauve", "Chartreuse", "Bisque", "Sienna", "Moccasin", "Periwinkle",
        "Slate", "Cornsilk", "Khaki", "Bisque", "Wheat", "Honeydew", "Lavender", "Misty Rose", "Sea Green",
        "Azure", "Old Lace", "Navajo White", "Papaya Whip", "Antique White", "Linen", "Ghost White",
        "Snow", "Floral White", "Gainsboro", "Alice Blue", "Ivory Black", "Beau Blue", "Bright Cerulean",
        "Baby Blue", "Candy Apple Red", "Crimson Glory", "French Fuchsia", "Lemon Curry", "Screamin' Green",
        "Royal Purple", "Middle Blue", "Mango Tango", "Medium Lavender Magenta", "Maximum Blue", "Ultramarine"
    ]
    fashion_items = [
        "Shirt","T-shirt","tshirt", "Polo Shirt", "Tank Top", "Sweater", "Hoodie", "Jacket", "Blazer", "Coat",
        "Jeans", "Trousers", "Chinos", "Shorts", "Sweatpants", "Leggings", "Skirt", "Dress",
        "Suit", "Tuxedo", "Wedding Dress", "Jumpsuit", "Bikini", "Swimsuit", "Lingerie", "Pajamas",
        "Socks", "Stockings", "Tights", "Underwear", "Bra", "Boxers", "Briefs", "Vest", "Undershirt",
        "Hat", "Cap", "Beanie", "Beret", "Sunhat", "Headband", "Scarf", "Gloves", "Mittens",
        "Belt", "Tie", "Bowtie", "Necktie", "Suspenders", "Shoes", "Sneakers", "Boots", "Sandals",
        "Flip Flops", "High Heels", "Loafers", "Oxfords", "Flats", "Espadrilles", "Wedges", "Mules",
        "Backpack", "Handbag", "Tote Bag", "Clutch", "Messenger Bag", "Satchel", "Briefcase", "Wallet",
        "Watch", "Bracelet", "Necklace", "Earrings", "Ring", "Sunglasses", "Glasses", "Cufflinks",
        "Tights", "Umbrella", "Belt", "Bowler Hat", "Fascinator", "Cape", "Poncho", "Pocket Square",
        "Bolero", "Bodysuit", "Corset", "Cummerbund", "Cummerbund", "Stole", "Shawl", "Pashmina",
        "Anklet", "Belly Chain", "Toe Ring", "Armlet", "Bangle", "Brooch", "Lapel Pin", "Tiara",
        "Visor", "Wristband", "Arm Warmers", "Leg Warmers", "Sarong", "Sarouel Pants", "Kilt", "Kerchief",
        "Duffel Bag", "Fanny Pack", "Gaiters", "Gauntlets", "Gusset", "Insoles", "Keffiyeh",
        "Keychain", "Lanyard", "Leggings", "Messenger Bag", "Money Belt", "Pocket Protector",
        "Shoehorn", "Shoe Tree", "Sleeve Garters", "Spats", "Suspenders", "Tights", "Tote Bag",
        "Trilby", "Turbans", "Umbrella Hat", "Visor", "Wallet", "Waterproof Bag", "Wedding Veil",
        "Kurta", "Sari", "Lehenga", "Sherwani", "Salwar Kameez", "Anarkali Suit", "Dhoti", "Pathani Suit",
        "Churidar", "Patiala Suit", "Bandhani", "Phulkari", "Dupatta", "Jhumkas", "Maang Tikka",
        "Nath", "Chooda", "Bangles", "Kada", "Bindi", "Payal", "Kolhapuri Chappals", "Mojaris",
        "Potli Bag", "Kanchipuram Sari", "Banarasi Sari", "Choli", "Ghagra Choli", "Bridal Veil"
    ]
    return fashion_items,colors,brands

def trend_check():
    array_fashion = ['#capri', '#oneshouldertop', '#trouser', '#tanktop', '#tubetop']
    return array_fashion