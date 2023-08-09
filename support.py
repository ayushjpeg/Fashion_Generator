import nltk
nltk.download('punkt') 

def Fashion_array():
    arr = [(r'hi|hello', ['Hello!', 'Hi there!', 'Hey!']),
        (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!']),
        (r'my favorite color is (.*)', ['That\'s a nice color choice!', 'I like that color too.']),
        (r'I like to wear (.*)', ['That\'s a great choice of clothing!', 'Nice preference!']),
        (r'I prefer (.*) brands', ['Brands are important! Which brands do you like?', 'Tell me more about your favorite brands.']),
        (r'I love (.*) style', ['Styles say a lot about a person! Could you elaborate on that?', 'Interesting! What do you like about that style?']),
        (r'(.*)', ['I hear you. Tell me more about fashion.', 'Fashion is fascinating! Could you tell me more?']),
        (r'I prefer (.*) brands', ['Brands are important! Which brands do you like?', 'Tell me more about your favorite brands.']),
        (r'I love (.*) style', ['Styles say a lot about a person! Could you elaborate on that?', 'Interesting! What do you like about that style?']),
        (r'my age is (\d+)', ['You\'re {} years old? Fashion preferences can change with age!', 'Age plays a role in fashion.']),
        (r'I live in (.*)', ['Living in {} sounds interesting! How does it influence your fashion choices?']),
        (r'(.*)', ['I hear you. Tell me more about fashion.', 'Fashion is fascinating! Could you tell me more?']),
        #(r'I love (green|blue|pink|purple|red|orange|yellow)', ['{} is a vibrant color!', 'Ah, {} is full of energy.']),
        #(r'My favorite color is (green|blue|pink|purple|red|orange|yellow)', ['Great choice! {} is a wonderful color.', '{} is a popular color!']),

        # # Clothing materials
        # (r'material should be (.*)', ['It is a comfortable choice!', 'Nice! it can be stylish.']),
        
        # # Footwear preferences
        # (r'I usually wear (sneakers|boots|sandals|heels|flats)', ['{} are a stylish option!', 'Nice choice of footwear.']),
        
        # # Seasonal fashion preferences
        # (r'In summer, I prefer wearing (light and breezy clothes|swimwear)', ['Summer fashion is all about staying cool! {} are great choices.']),
        
        # # Jewelry and accessories
        # (r'I like to accessorize with (necklaces|bracelets|rings|scarves)', ['Accessories can enhance your look! {} are a good choice.']),
        
        # # Preferred shopping destinations
        # (r'When shopping, I prefer (online stores|boutiques|department stores)', ['Shopping preferences vary! {} can offer a unique experience.']),
        
        # # Occasion-based clothing choices
        # (r'For formal events, I prefer (suits|gowns|tuxedos)', ['{} are great choices for formal occasions.']),
        
        # # Budget considerations
        # (r'My fashion budget is (\$[\d,]+)', ['It\'s important to budget for fashion. {} is a good budget!', 'Setting a fashion budget is wise.']),
        
        # # Travel and fashion
        # (r'I dress differently when traveling (abroad|to the beach|to colder places)', ['Traveling offers fashion opportunities! How does your style change?']),
        
        # # Body type and fashion
        # (r'I have a (slim|athletic|curvy|petite) body type', ['Fashion can be tailored to your body type! {} body types can rock different styles.']),
        # # Footwear preferences
        # (r'I often wear (sandals|loafers|oxfords|mules)', ['{} are comfortable options!', 'Nice choice of footwear.']),
        
        # # Preferred shopping time
        # (r'I like shopping (in the morning|in the afternoon|in the evening)', ['Shopping preferences vary throughout the day.']),
        
        # # Special occasions
        # (r'For special occasions, I like to wear (dresses|suits|tuxedos)', ['{} are great choices for special moments.']),
        
        # # Jewelry preferences
        # (r'I adore (diamonds|pearls|gold jewelry|silver jewelry)', ['{} add elegance to any outfit!', 'Nice choice!']),
        
        # # Hat preferences
        # (r'I enjoy wearing (hats|caps|beanies|fedoras)', ['Hats can add a unique touch to your look.']),
        
        # # Makeup and fashion
        # (r'I like to match my makeup with my outfits', ['Matching makeup can enhance your overall style!']),
        
        # # Vintage fashion
        # (r'I appreciate (vintage|retro) fashion', ['Vintage fashion has a charm of its own.']),
        
        # # Wardrobe organization
        # (r'My wardrobe is (neatly organized|a mix of styles|color-coordinated)', ['A well-organized wardrobe makes dressing up easier!']),
        
        # # Seasonal color preferences
        # (r'In (fall|winter|spring|summer), I prefer wearing (earthy tones|cool colors|pastels|bright hues)', ['Seasonal colors can complement the environment.']),
        
        # # Cultural influences
        # (r'My fashion choices are influenced by my cultural background', ['Cultural influences play a big role in fashion.']),
        
        # # Clothing textures
        # (r'I love wearing (silk|velvet|lace|knits)', ['{} can add texture and depth to your outfit.']),
        
        # # Body positivity and fashion
        # (r'I embrace my body and choose clothes that make me feel confident', ['Body positivity is essential for personal style.']),
        
        # # Shopping with friends
        # (r'I enjoy shopping with my (friends|family)', ['Shopping can be a fun social activity!']),
        
        # # Vintage versus modern fashion
        # (r'I like mixing vintage pieces with modern ones', ['Combining vintage and modern creates an eclectic style.']),
        
        # # ... Add more patterns and responses ...

        # # Fallback response
        # (r'(.*)', ['I hear you. Tell me more about fashion.', 'Fashion is fascinating! Could you tell me more?']),
        # (r'I follow a (casual|business casual|formal) dress code', ['Dress codes can influence your daily style.', 'Great! Dress codes help set the tone.']),
        
        # # Fashion magazines and blogs
        # (r'I often read (Vogue|Elle|InStyle|Fashionista) magazine', ['Fashion magazines offer inspiration and trends.']),
        
        # # Influences from art and culture
        # (r'Art and culture inspire my fashion choices', ['Artistic influences can lead to unique style choices.']),
        
        # # Prints and patterns
        # (r'I enjoy wearing (stripes|florals|animal prints|geometric patterns)', ['Patterns can add personality to your outfit.']),
        
        # # Hair and fashion
        # (r'My hairstyle complements my fashion style', ['Hair and fashion together create a complete look.']),
        
        # # Preferred jewelry type
        # (r'I prefer (minimalist|statement|bohemian) jewelry', ['Jewelry styles can complement your overall look.']),
        
        # # Fashion documentaries
        # (r'I\'ve watched fashion documentaries like The September Issue', ['Fashion documentaries offer insights into the industry.']),
        
        # # Embellishments and details
        # (r'I love clothes with (embroidery|sequins|beading|fringe)', ['Embellishments can make a garment stand out.']),
        
        # # Fashion evolution
        # (r'My fashion choices have evolved over the years', ['Fashion evolution is a natural part of personal growth.']),
        
        # # Gender-neutral fashion
        # (r'I prefer (gender-neutral|androgynous) fashion', ['Gender-neutral fashion promotes inclusivity.']),
        
        # # Wardrobe staples
        # (r'My wardrobe staples include (jeans|white shirts|black dresses|blazers)', ['Wardrobe staples are versatile and timeless.']),
        
        # # Fashion and confidence
        # (r'I feel confident when I wear (bold colors|high heels|tailored suits)', ['Confidence shines through in your fashion choices.']),
        
        # # Secondhand and thrift shopping
        # (r'I enjoy shopping for secondhand and thrifted items', ['Thrifting is a sustainable and unique way to shop.']),
        
        # # Cultural fusion in fashion
        # (r'I blend elements of different cultures in my fashion', ['Cultural fusion creates a rich and diverse style.']),
        
        # # ... Add more patterns and responses ...

        # # Fallback response
        # (r'(.*)', ['I hear you. Tell me more about fashion.', 'Fashion is fascinating! Could you tell me more?'])
    ]
    return arr