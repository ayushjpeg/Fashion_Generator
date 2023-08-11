import nltk
nltk.download('punkt') 
nltk.download('nps_chat')
nltk.download('averaged_perceptron_tagger')

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
    return arr