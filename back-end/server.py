import datetime
import flask
from flask import request, jsonify
import re
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from matplotlib import pyplot as plt
import collections
from wordcloud import WordCloud
from summarizer import Summarizer
from nltk import tokenize
import pytesseract
import io
from PIL import Image
import os 
from langdetect import detect
import sumy 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from GetData import getData
from TermWeighting import termWeigthing
from enNER import nerEng
from trNER import nertr
from Regex import regex
from GetSeveralData import getSeveralData
from WordCloudplt import wordCloud
from Keyword import keyword

app = flask.Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run()

@app.route('/api/btnTerm', methods=['POST'])
def btnTerm():
    text=getData(True)
    term = termWeigthing(text)
    jres = {'detail': 'Descriptive Terms: ',
            'detail2': term
            }
    return jsonify(jres)


@app.route('/api/btnNer', methods=['POST'])
def btnNer():
    text = getData(False)
    lang=detect(text)

    if(lang=="en"):
        TaggedOrganizations, TaggedPersons, TaggedGeographicalEntities = nerEng(text)
        jres = {'org': "Organizations: ",
                'org2': TaggedOrganizations,
                'per': 'Persons: ',
                'per2': TaggedPersons,
                'loc': 'Locations: ',
                'loc2': TaggedGeographicalEntities
                }
        return jsonify(jres)

    elif(lang=="tr"):
        orglist,namelist,loclist,timelist= nertr(text)

        jres = {'org': "Organizations: ",
                'org2': orglist,
                'per': 'Persons: ',
                'per2': namelist,
                'loc': 'Locations:',
                'loc2': loclist,
                'time': "Time:",
                'time2': timelist
                }
        return jsonify(jres)

    else:    
        result="This language is not supported for NER"
        jres = {"org": result}
        return jsonify(jres)



@app.route('/api/btnRegex', methods=['POST'])
def btnRegex():
    text,data2 = getSeveralData("taburl", "SentRegex", False)
    data2=str(data2)
    term=regex(text, data2)
          
    jres = {'detail': term}
    return jsonify(jres)


@app.route('/api/btnCon', methods=['POST'])
def btnCon():
    text=getData(False)

    jres = {'detail': text}
    return jsonify(jres)


@app.route('/api/btnWord', methods=['POST'])
def btnWord():
    text=getData(True)
    plt=wordCloud(text)
  
    jres = {'detail': plt.show()}
    return jsonify(jres)


@app.route('/api/btnSum', methods=['POST'])
def btnSum():
    text,data2=getSeveralData("taburl", "SentNum", False)
    data2 = int(data2) 

    if data2 < 1:
        data2 = 1
    
    lang=detect(text)
    mydict = {"en": "english", "tr": "turkish", "de": "german", "es": "spanish", "fr": "french"}
    lang2 = mydict.get(lang)
    if(lang2 == None):
        result = "This language is not supported for summary function."
        jres = {'detail': result}
        return jsonify(jres)
    my_parser = PlaintextParser.from_string(text,Tokenizer(lang2))
    lex_rank_summarizer = LexRankSummarizer()
    lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=data2)

    # Printing the summary
    result=""
    for sentence in lexrank_summary:
        sentence=str(sentence)
        result += sentence

    result = result.replace(".",". ")

    jres = {'detail': result}
    return jsonify(jres)



@app.route('/api/btnKeyword', methods=['POST'])
def btnKeyword():

    data, data2, data3=getSeveralData("taburl", "SentNum","case")   
    sub_text2=keyword(data,data2,data3)

    jres = {'detail': sub_text2}
    return jsonify(jres)

@app.route('/api/btnOCR', methods=['POST'])
def btnOCR():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')
    images = soup.find_all("img")
    image_list = []
    for image in images:
        a = str(image)
        if "http" in a:
            image_list.append(image["src"])

    term = "<ul>"
    
    for i in image_list:
        try:
            response = requests.get(i)
            img = Image.open(io.BytesIO(response.content))
            a = pytesseract.image_to_string(img)
            if a.strip():
                term+="<li>"+ a+ "</li>"
        except:
            continue       
   
    if term == "<ul>":
        term = "There is no image."
        jres = {"detail2": term}
        return jsonify(jres)
    term += "</ul>"
    jres = {'detail': term}

    return jsonify(jres)