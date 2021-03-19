import datetime
import flask
from flask import request, jsonify
from bs4 import BeautifulSoup
import requests
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

app = flask.Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run()


@app.route('/api/fetch', methods=['POST'])
def fetch():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")
    text = []
    for points in mytext:
        point = str(points.text)
        text.append(point)

    # Pre-processing
    stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
                 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    Data = []
    for item in text:
        item = item.lower()
        item = re.sub(r'[^\w\s]', '', item)
        Data.append(item)

    vectorizer = TfidfVectorizer(stop_words=stopWords)
    X = vectorizer.fit_transform(Data).toarray()

    myDictionary = []
    featureCount = 0
    for item in vectorizer.get_feature_names():
        myDictionary.append(item)
        featureCount += 1

    (row, column) = X.shape
    tfidf = [0] * featureCount
    counter = 0
    while counter < featureCount:
        for j in range(0, row):
            tfidf[counter] += X[j][counter]
        counter += 1

    TFIDF = {}
    for i in range(0, featureCount):
        TFIDF[myDictionary[i]] = tfidf[i]

    SortedDict = {k: v for k, v in sorted(
        TFIDF.items(), key=lambda item: item[1])}
    TFIDFListesi = []
    for item, value in SortedDict.items():
        value = "{:.2f}".format(value)
        TFIDFListesi.append(item + ":")
        TFIDFListesi.append(value + ",")

    mostImportantwords = TFIDFListesi[-20:]
    term = "<ul>"

    for i in range(0, len(mostImportantwords)):
        a = len(mostImportantwords)-i-2
        if i % 2 == 0:
            if i < len(mostImportantwords)-1:
                term += "<li>" + \
                    str(mostImportantwords[a]) + " " + \
                    str(mostImportantwords[a+1]) + "</li>"

    term += "</ul>"

    jres = {'detail': 'Descriptive Terms: ',
            'detail2': term
            }
    return jsonify(jres)


@app.route('/api/fetch2', methods=['POST'])
def fetch2():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')

    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""

    for points in mytext:
        point = str(points.text)
        text += point

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    OrganizationList = []
    GPEList = []
    PersonList = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text not in PersonList:
                PersonList.append(ent.text)
        if ent.label_ == "ORG":
            if ent.text not in OrganizationList:
                OrganizationList.append(ent.text)
        if ent.label_ == "GPE":
            if ent.text not in GPEList:
                GPEList.append(ent.text)

    TaggedOrganizations = ', '.join(OrganizationList)
    TaggedPersons = ', '.join(PersonList)
    TaggedGeographicalEntities = ', '.join(GPEList)

    jres = {'org': "Organizations: ",
            'org2': TaggedOrganizations,
            'per': 'Persons: ',
            'per2': TaggedPersons,
            'loc': 'Locations: ',
            'loc2': TaggedGeographicalEntities
            }
    return jsonify(jres)


@app.route('/api/fetch3', methods=['POST'])
def fetch3():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")

    text = ""
    for points in mytext:
        point = str(points.text)
        text += point
    new_text = ""
    for sen in text:
        new_text = new_text + sen

    text = new_text
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    words = nltk.wordpunct_tokenize(text)

    i = 0
    mydict = set()

    term = []
    voc_size = []
    for word in words:
        i = i + 1
        mydict.add(word)  # words exist only once

        term.append(i)
        voc_size.append(len(mydict))

    plt.scatter(term, voc_size)
    plt.xlabel('term occurrence')
    plt.ylabel('vocabulary size')

    jres = {'detail': plt.show()}

    return jsonify(jres)


@app.route('/api/fetch4', methods=['POST'])
def fetch4():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""
    for points in mytext:
        point = str(points.text)
        text += point + " "

    jres = {'detail': text}

    return jsonify(jres)


@app.route('/api/fetch5', methods=['POST'])
def fetch5():
    sword = ['acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her',
             'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani']
    sword2 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
              'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")
    text = []
    for points in mytext:
        point = str(points.text)
        text.append(point)

    a = 0
    for i in text:
        i = i.lower()
        new = re.sub(r'[^\w\s]', '', i)
        text[a] = new
        a = a + 1

    aa = 0
    for i in text:  # for every sentence
        sentence = i

        sentence = nltk.wordpunct_tokenize(sentence)

        mylist = []
        for a in sentence:
            # if a in sword:
            # mylist.append(a)
            if a in sword2:
                mylist.append(a)

        for u in mylist:
            sentence.remove(u)

        new_s = ""
        for y in sentence:
            new_s = new_s + " " + y

        text[aa] = new_s
        aa = aa + 1

    vectorizer = TfidfVectorizer()
    vecs = vectorizer.fit_transform(text)
    feature_names = vectorizer.get_feature_names()
    aaa = vecs.transpose().sum(axis=1)
    lst1 = aaa.tolist()

    myl = []
    for i in lst1:
        res = str(i)[1:-1]
        ress = float(res)
        myl.append(ress)

    # creating the dictionary to give as a parameter to wordcloud function
    mydict = {}
    n = 0
    for name in feature_names:
        mydict[name] = myl[n]
        n = n + 1

    mywc = WordCloud(background_color="black", width=1000, height=1000)
    mywc.generate_from_frequencies(mydict)

    plt.figure(figsize=(6, 6), facecolor=None)
    plt.imshow(mywc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)

    jres = {'detail': plt.show()}

    return jsonify(jres)


@app.route('/api/fetch6', methods=['POST'])
def fetch6():
    data = request.json['taburl']
    data2 = request.json['SentNum']
    data2 = int(data2) - 1
    if data2 < 1:
        data2 = 1
    html_content = requests.get(data).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""
    for points in mytext:
        point = str(points.text)
        text += point
    new_text = ""
    for sen in text:
        new_text = new_text + sen

    text = new_text

    model = Summarizer()
    result = model(text, num_sentences=data2)

    jres = {'detail': result}
    return jsonify(jres)


@app.route('/api/fetch7', methods=['POST'])
def fetch7():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')

    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""

    for points in mytext:
        point = str(points.text)
        text += point

    p = text
    text = tokenize.sent_tokenize(p)

    myorg = ["Üniversitesi", "Koleji", "Okulu", "Kurumu", "Bankası", "Şirketi", "İştirakı", "Vakfı",
             "Federasyonu", "Kulübü", "Takımı", "Meclisi",  "Derneği", "Holdingi", "Firması", "Bakanlığı", "Hastanesi"]
    orglist = []
    for line in text:  # each sentence
        for a in range(0, len(myorg)):
            myvar = myorg[a]
            if myvar in line:
                mystr = re.findall(
                    r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)* ' + myvar, line)

                for element in mystr:
                    orglist.append(element)
            a += 1

    myname = ["Abi", "Ağabey", "Amca", "Dayı",
              "Bey", "Bay", "Hanım", "Bayan", "Hoca"]
    namelist = []
    for line in text:  # each sentence
        for a in range(0, len(myname)):
            myvar = myname[a]
            if myvar in line:
                mystr = re.findall(
                    r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)* ' + myvar, line)

                for element in mystr:
                    namelist.append(element)
            a += 1

    myloc = ["Dağı", "Köprüsü", "Mezarı", "Sarayı", "Şehri", "Ülkesi", "Deresi", "Çayı", "Gölü",
             "Otoyolu", "Köyü", "Kasabası", "Mahallesi", "Caddesi", "Dairesi", "Meydanı", "Rezidansı"]
    loclist = []
    for line in text:  # each sentence
        for a in range(0, len(myloc)):
            myvar = myloc[a]
            if myvar in line:
                mystr = re.findall(
                    r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)* ' + myvar, line)

                for element in mystr:
                    loclist.append(element)
            a += 1


    timelist = []
    for line in text:
        if ' yıl' in line:
            mystr = re.findall(r'\d{4}(?=\s+yıl\w+)', line)
            for element in mystr:
                timelist.append(element)

        if ' sene' in line:
            mystr = re.findall(r'\d{4}(?=\s+sene\w+)', line)
            for element in mystr:
                timelist.append(element)

        if "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "0" in line:
            mystr = re.findall(r'\d{4}[\'][td][ea]', line)
            for element in mystr:
                timelist.append(element)

            mystr = re.findall(r'\d\d[-\.]\d\d[-\.]\d{4}', line)
            for element in mystr:
                timelist.append(element)

            mystr = re.findall(r'\d\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s+\d{4}', line)
            for element in mystr:
                timelist.append(element)

            mystr = re.findall(r'\d\s+[a-zçğıöşü]*\s+\d{4}', line)
            for element in mystr:
                timelist.append(element)

            mystr = re.findall(r'[012]\d[:\.][012345]\d\s+', line)
            for element in mystr:
                timelist.append(element)

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
