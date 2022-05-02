import math
import nltk
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import websearching

class valider:
    def scrape_google(self,query):
        query = urllib.parse.quote_plus(query)
        try:
            session = HTMLSession()
            response = session.get("https://www.google.com/search?q=" + query)

        except requests.exceptions.RequestException as e:
            print(e)
        
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        return links
    
    def parse_results(self, query):
        query = urllib.parse.quote_plus(query)
        session = HTMLSession()
        response = session.get("https://www.google.com/search?q=" + query)
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".VwiC3b" #.IsZvec 

        results = response.html.find(css_identifier_result)[0:5]

        output = []

        for result in results:
            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).attrs['href'],
                'text': result.find(css_identifier_text, first=True).text
            }
        
            output.append(item)

        return output

#TOKENIZATION
def tokenizer(doc_text):   
    tokens = nltk.word_tokenize(doc_text)
    return tokens

#STEMMING
def stemmer(token_list):
    ps = nltk.stem.PorterStemmer()
    stemmed = []
    for words in token_list:
        stemmed.append(ps.stem(words))
    return stemmed

#REMOVING STOPWORDS
def remove_stopwords(doc_text):
    stop_words = set(stopwords.words('english'))
    cleaned_text = []
    for words in doc_text:
        if words not in stop_words:
            cleaned_text.append(words)
    return cleaned_text


def cosinesimilarity(input_string):
    
    print(input_string)
    count = 0
    output = []
    q = []
    corpus = []
    clean_corpus = []
    result_docs = []
    stop_words = set(stopwords.words('english'))
    # input_string = str(input_string)
    # input_string = input("ENTER THE STRING TO CAL COSINE SCORE: ")

    isvalid = valider()
    isvalid.scrape_google(input_string)
    results = isvalid.parse_results(input_string)

    for result in results:
        text = result['text']
        corpus.append(text)
        count = count + 1


    #FUNCTION TO PERFORM ALL PREPROCESSING STEPS
    for doc in corpus:
        tokens = tokenizer(doc)
        doc_text = remove_stopwords(tokens)
        doc_text = stemmer(doc_text)
        doc_text = ' '.join(doc_text)
        clean_corpus.append(doc_text)

    #VECTOR SPACE REPRESENTATION
    vectorizerX = TfidfVectorizer()     #THIS WILL AUTOMATICALLY GENERATE OUR TF-IDF VECTORIZER
    vectorizerX.fit(clean_corpus)       #THIS WILL FIT OUR CORPUS INTO THE VECTORIZER
    doc_vector = vectorizerX.transform(clean_corpus)        #TRANSFORMING THE CORPUS INTO A VECTOR

    #THIS WILL MAKE THE KEYWORDS AS COLUMNS AND DOC-IDS AS ROWS
    #THIS CONTAINS THE IF-IDF WEIGHTS
    df = pd.DataFrame(doc_vector.toarray(), columns=vectorizerX.get_feature_names_out())

    query = input_string

    #PREPROCESSING WITH THE QUERY
    query = tokenizer(query)
    query = remove_stopwords(query)

    for w in stemmer(query):
        q.append(w)
    q = ' '.join(q)

    query_vector = vectorizerX.transform([q])       #TRANSFORMING QUERY INTO VECTOR

    #CALCULATE COSINE SIMILARITY AND CONVERTING IT INTO 1D LIST
    cosineSimilarities = cosine_similarity(doc_vector, query_vector).flatten()

    # for i in range(count):
    #     if cosineSimilarities[i] >= 0.001:  #USING ALPHA VALUE FOR THRESHOLD
    #         result_docs.append(i+1)

    for i, result in enumerate(results):
        item = {
            'title': result['title'],
            'link': result['link'],
            'score': cosineSimilarities[i],
            'angle': math.degrees(math.acos(cosineSimilarities[i]))
        }

        output.append(item)

    print("\n")

    if not websearching.objects.all():
        
        for i in output:

            websearching.objects.create(
                title = i['title'],
                link = i['link'],
                score = i['score'],
                angle = i['angle']
            )  

            print("TITLE: ", i['title'])
            print("LINK: ", i['link'])
            print("SCORE: ", i['score'])
            print("ANGLE: ", i['angle'])
            print('\n')

    else:
        for i in output:

            s = websearching(
                title = i['title'],
                link = i['link'],
                score = i['score'],
                angle = i['angle']
            )  

            s.save()

            print("TITLE: ", i['title'])
            print("LINK: ", i['link'])
            print("SCORE: ", i['score'])
            print("ANGLE: ", i['angle'])
            print('\n')