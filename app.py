from flask import Flask
from flask import render_template
from flask import request

from selenium import webdriver
from bs4  import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import random
import string
import time
import sys
import requests
import re
import urllib.request
import random

import nltk 
from nltk.corpus import wordnet 
from nltk.corpus import stopwords
nltk.download("stopwords")
nltk.download('wordnet')
eng_stopwords = set(stopwords.words('english'))


def getSentence(cur):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': 'Machine_learning',
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
    ).json()
    page = next(iter(response['query']['pages'].values()))
    parse_text = page['extract']
    sent = parse_text.split(".")
    
   
    parse_text = sent[cur]
    sent_withoutStopwords = [word for word in parse_text.split(" ") if word not in eng_stopwords]
    randWord = random.choice(sent_withoutStopwords)

    antonyms = [] 
    
    for syn in wordnet.synsets(randWord): 
        for l in syn.lemmas(): 
            if l.antonyms(): 
                antonyms.append(l.antonyms()[0].name()) 

    allOptions = []

    if(len(antonyms) > 0):
        allOptions.append((antonyms[0],0))

    parse_text = parse_text.replace(randWord, "______")
    allOptions.append((randWord,1))

    random.shuffle(allOptions)

    return [parse_text, allOptions]



app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def landing_page():
    return render_template('input.html')

@app.route('/nexter', methods=['POST'])
def nexter():

    if not request.form:
        return render_template('notFound.html')
    
    curr = int(request.form['curr'])
    searchTerm = request.form['searchTerm']
    totalSent = request.form['totalSent']

    if int(curr)== int(totalSent)-1:
        return render_template('congrats.html')

    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': searchTerm,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
    ).json()
    page = next(iter(response['query']['pages'].values()))
    parse_text = page['extract']
    sent = parse_text.split(".")
    
    parse_text = sent[curr]
    sent_withoutStopwords = [word for word in parse_text.split(" ") if word not in eng_stopwords]
    randWord = random.choice(sent_withoutStopwords)

    antonyms = [] 
    
    for syn in wordnet.synsets(randWord): 
        for l in syn.lemmas(): 
            if l.antonyms(): 
                antonyms.append(l.antonyms()[0].name()) 

    allOptions = []

    if(len(antonyms) > 0):
        allOptions.append((antonyms[0],0))

    parse_text = parse_text.replace(randWord, "______")
    allOptions.append((randWord,1))

    random.shuffle(allOptions)

    return render_template('landing_page.html', allOptions=allOptions, sent=parse_text, curr = curr+1, searchTerm = searchTerm, totalSent=totalSent )


@app.route('/search', methods=['POST'])
def suggestions():

    if not request.form:
        return render_template('notFound.html')

    searchTerm = request.form['searchTerm']
   
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': searchTerm,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
    ).json()
    page = next(iter(response['query']['pages'].values()))
    parse_text = page['extract']
    sent = parse_text.split(".")
    totalSent = len(sent)
    
   
    parse_text = sent[0]
    sent_withoutStopwords = [word for word in parse_text.split(" ") if word not in eng_stopwords]
    randWord = random.choice(sent_withoutStopwords)

    antonyms = [] 
    
    for syn in wordnet.synsets(randWord): 
        for l in syn.lemmas(): 
            if l.antonyms(): 
                antonyms.append(l.antonyms()[0].name()) 

    allOptions = []

    if(len(antonyms) > 0):
        allOptions.append((antonyms[0],0))

    parse_text = parse_text.replace(randWord, "______")
    allOptions.append((randWord,1))

    random.shuffle(allOptions)

    return render_template('landing_page.html', allOptions=allOptions, sent=parse_text, curr = 0, searchTerm = searchTerm, totalSent=totalSent )
   

    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)


