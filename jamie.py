import numpy as np
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read and preprocess the document
with open('chatbots.txt', 'r', errors='ignore') as f:
    raw_doc = f.read().lower()

# Download necessary NLTK packages
nltk.download('punkt')
nltk.download('wordnet')

# Tokenization
sent_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)

# Lemmatization
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting inputs and responses
GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)

# Detailed response function with improved context
def response(user_response):
    robo1_response = ''

    # Append the user response to the list of sentences for context
    sent_tokens.append(user_response)

    # Create the TF-IDF Vectorizer
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)

    # Calculate cosine similarity
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])
    idx = vals.argsort()[0][-1]

    # Check the similarity
    if vals[0][idx] == 0:
        robo1_response = "I am sorry! I don't understand you."
    else:
        # Use surrounding sentences for more context
        context_window = 0  # Number of surrounding sentences to include
        start_idx = max(0, idx - context_window)
        end_idx = min(len(sent_tokens), idx + context_window + 1)

        # Generate a detailed response by including a broader context
        detailed_response = ' '.join(sent_tokens[start_idx:end_idx])
        robo1_response = detailed_response

    # Remove the user response from the list
    sent_tokens.pop(-1)
    return robo1_response

# Main chatbot loop
flag = True
print("BOT: Hi, I'm Jamie. Let's talk about Ideation! Also, if you want to exit at any time, just type Bye!")

while flag:
    user_response = input().lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you' or user_response == 'nice' or user_response == 'good':
            flag = False
            print("BOT: You are welcome..,If you have more questions don't hesitate to ask!!")
        else:
            if greet(user_response) is not None:
                print("BOT: " + greet(user_response))
            else:
                print("BOT: ", end="")
                print(response(user_response))
    else:
        flag = False
        print("BOT: Bye! Take care <3")
