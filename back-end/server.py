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
import pytesseract
import io
from PIL import Image
import os 


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
    if footer_tag == True:
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
    if footer_tag == True:
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
    data = request.json['taburl']
    data2 = request.json['SentRegex']
    data2 = str(data2)
    html_content = requests.get(data).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    if footer_tag == True:
        footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""
    for points in mytext:
        point = str(points.text)
        text += point
    
    text = text.replace(".",". ")

    data2= r'' + data2 
    result=re.findall(data2, text)

    if len(result)==0:
        mysent="Expression is not found"
        result.append(mysent)
        jres = {'detail2': result}
        return jsonify(jres)

    term = "<ul>"
    
    for i in result:
        term+="<li>" + i +"</li>"
    
    term += "</ul>"
    jres = {'detail': term}
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
    if footer_tag == True:
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
    if footer_tag == True:
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
    data2 = int(data2) -1
    if data2 < 1:
        data2 = 1
    html_content = requests.get(data).text
    soup = BeautifulSoup(html_content, 'lxml')
    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    if footer_tag == True:
        footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""
    for points in mytext:
        point = str(points.text)
        text += point
    
    text = text.replace(".",". ")
    
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
    if footer_tag == True:
        footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""

    for points in mytext:
        point = str(points.text)
        text += point

    p = text
    text = tokenize.sent_tokenize(p)

    myorg = ["Üniversitesi", "Koleji", "Okulu", "Kurumu", "Bankası", "Şirketi", "İştirakı", "Vakfı", "Federasyonu", "Kulübü", "Takımı", "Meclisi",  "Derneği", "Holdingi", "Teşkilatı",
            "Firması", "Bakanlığı", "Hastanesi", "Devleti", "Partisi", "Başkanlığı", "Komiserliği", "Belediyesi", "Belediyeleri", "Tiyatrosu", "İmparatorluğu", "Birliği","Bülteni", "Holding",
            "Danışmanlığı", "Müdürlüğü", "Enstitüsü", "Delegasyonu", "Büyükelçiliği", "Konseyi", "Parlamentosu", "Ofisi", "Kurulu", "Meclisi","Gazetesi","Bülteni","Basın Odası","Basın Odası",
            "Müsteşarlığı", "Parti", "A.Ş.", "şirketi", "Örgütü","Komutanlığı","Kuvvetleri","Operasyonu","Komitesi","Forumu", "Cumhuriyeti","Töreni","Komisyonu","Konseyi", "gazetesi","dergisi",
            "Birimi", "Danıştay","Yargıtay","Sayıştay", "Sekreterliği", "Mahkemesi","Teşkilatı","Bank","Ajansı","Kooperasyonu","Organizasyonu","Vakfı","Televizyonu",
            "savcılığı","Savcılığı","Başsavcılığı","kardeşi","Konferansı","kanalı", "Kanal'", "cemaati"]
    orglist = []
    for line in text:  # each sentence
        for a in range(0, len(myorg)):
            myvar = myorg[a]
            if myvar in line:
                mystr = re.findall(r'[A-ZÇĞİÖŞÜ\(][A-Za-zçğıöşü\(\)]*(?:\s+[A-ZÇĞİÖŞÜ\(][a-zçğıöşü\(\)]*)* ' + myvar, line)

                for element in mystr:
                    orglist.append(element)
            a += 1


    basın_file = open("basınlar.txt", "r", encoding="utf8")
    basınf=[]
    for l in basın_file:
        if len(l)>1:
            basınf.append(l.strip())
    for line in text:
        print("LINE:", line)
        for ele in range(0, len(basınf)):
            #print("eee", ele)
            #ele=ele.strip()
            #print("EEE", ele,"EEE")
            if basınf[ele] in line:
                print("YESS")
                orglist.append(basınf[ele])



    myname = ["Abi", "Ağabey", "Amca", "Dayı",
              "Bey", "Bay", "Hanım", "Bayan", "Hoca"]

    myname2 = ["Bakan", "Vali", "Müftü", "Kadı", "Kral", "Kraliçe", "Prens", "Prenses","CEO'su","yetkilisi","Muhabiri", "Editörü",
    "İmam", "Cumhurbaşkanı", "Sayın", "Sevgili", "Kıymetli", "Değerli", "Doktor", "Başbakanı", "Başkanvekili","nişanlısı", "arkadaşı olan","üyesi",
    "Hekim", "Avukat", "Öğretmen", "Profesör", "Doçent", "Başkan", "Yardımcısı","Muhabiri","Prof.", "Dr.", "başkanı", "Büyükelçisi", "Sözcüsü","danışmanı",
    "Lideri", "lideri", "yönetmen","Düşesi","sunucusu","ağabeyi","yöneticisi","Sekreteri","siyasetçi","öğretmen"]          

    namelist = []
    for line in text:  # each sentence
        for a in range(0, len(myname)):
            myvar = myname[a]
            if myvar in line:
                mystr = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)*' + myvar, line)

                for element in mystr:
                    namelist.append(element)
            a += 1
    for line in text:  # each sentence
        for a in range(0, len(myname2)):
            myvar = myname2[a]
            if myvar in line:
                mystr = re.findall(myvar + r'\w*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)*', line)

                for element in mystr:
                    element=element.replace(myvar, '')
                    if ord(element[0]) in range(97, 123) or element[0] == 'ı' or element[0] == 'ç' or element[0] == 'ö' or element[0] == 'ü':
                        element = element[element.find(' '):]
                    
                    namelist.append(element)
            a += 1

    myloc = ["Dağı", "Köprüsü", "Mezarı", "Saray", "Şehri", "Ülkesi", "Deresi", "Çayı", "Gölü","Çölü","anakarası","kıtası"
             "Otoyolu", "Köyü", "Kasabası", "Mahallesi", "Caddesi", "Dairesi", "Meydanı", "Rezidansı", "Meydanı", "Denizi", "Körfezi", "Kenti", "Tapınağı", "Kilisesi", "Otogarı",
             "Merkezi", "Okyanusu", "Kütüphanesi", "İstasyonu", "Kayalıkları", "Limanı", "Adası","adası", "Koyu", "Yaylası", "Tepesi", "Çayırı", "Yolu", "Kalesi", "Müzesi",
             "Boğazı", "Ocağı", "Koğuşu", "Stadyum", "Kortu", "Sahası", "Otel", "Hotel", "Pansiyon", "Mağaza", "Vadisi", "Geçidi", "İlçesi", "Beldesi", "ilçesi","bölgesi","kenti","başkenti"]
    loclist = []

    loc_file = open("Şehirler.txt", "r", encoding="utf8")
    locf=[]
    for l in loc_file:
        if len(l)>1:
            locf.append(l.strip())
    for line in text:
        print("LINE:", line)
        for ele in range(0, len(locf)):
            if locf[ele] in line:
                print("YESS")
                loclist.append(locf[ele])
    #ÜLKELER
    df1 = pd.read_excel('Ulkeler.xlsx')
    ülkeler = df1['ulkeler'].tolist()
    for line in text:
        for ü in range(0, len(ülkeler)):
            if ülkeler[ü] in  line:
                loclist.append(ülkeler[ü])


    for line in text:  # each sentence
        for a in range(0, len(myloc)):
            myvar = myloc[a]
            if myvar in line:
                mystr = re.findall(
                    r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)* ' + myvar, line)

                for element in mystr:
                    loclist.append(element)
            a += 1

    mytime=["yıl", "sene", "yüzyıl", "hafta", "gün", "saat", "dakika", "saniye", "ay"]
    aylar=["ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık"]
    timelist = []
    for line in text:

        #aylar list  
        for a in range(0, len(aylar)):
            myvar = aylar[a]
            myvar2=myvar.capitalize()
            if myvar or myvar2 in line:
                mystr = re.findall(r'\d{1,4}\s' + myvar +'\w*', line)
                mystr2 = re.findall(r'\d{1,4}\s' + myvar2 +'\w*', line)

                for element in mystr:
                    timelist.append(element)
                for element in mystr2:
                    timelist.append(element)

                #if months are not written together with the numbers
                if len(mystr)==0 and len(mystr2)==0:
                    mystr = re.findall(myvar +r'\w*', line)
                    mystr = re.findall(myvar2 +r'\w*', line)
                    for element in mystr:
                        timelist.append(element)
                    for element in mystr2:
                        timelist.append(element)

            a += 1

        #mytime list
        for a in range(0, len(mytime)):
            myvar = mytime[a]
            if myvar in line:
                mystr = re.findall(r'\d{1,4}\s' + myvar +'\w*', line)

                for element in mystr:
                    timelist.append(element)
            a += 1



        if "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "0" in line:
            mystr = re.findall(r'\d{4}[\'][td][ea]', line)
            for element in mystr:
                timelist.append(element)

            mystr = re.findall(r'\d\d[-\.]\d\d[-\.]\d{4}', line)
            for element in mystr:
                timelist.append(element)

            #SONRA BAK !!!
            mystr = re.findall(r'\s\d{1,2}\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s+\d{4}', line)
            for element in mystr:
                timelist.append(element)
            
            mystr = re.findall(r'\s\d{1,2}\s+[a-zçğıöşü]*\s+\d{4}', line)
            for element in mystr:
                timelist.append(element)

            mystr = re.findall(r'[012]\d[:\.][012345]\d\s+', line)
            for element in mystr:
                timelist.append(element)


    #filters out any duplicates.
    loclist = list(set(loclist))
    orglist = list(set(orglist))
    namelist = list(set(namelist))
    timelist = list(set(timelist))

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

@app.route('/api/fetch8', methods=['POST'])
def fetch8():
    data = request.json['taburl']
    data2 = request.json['SentNum']
    data3 = request.json["case"]
    data2 = str(data2)
    if data3 == "0": #Case sensitive
        myword = data2.lower()
        myword2 = data2.capitalize()
    else:    
        myword = data2
        myword2 = data2
    
    html_content = requests.get(data).text
    soup = BeautifulSoup(html_content, 'lxml')

    for a in soup.findAll('a', href=True):
        a.decompose()
    footer_tag = soup.footer
    if footer_tag == True:
        footer_tag.decompose()
    mytext = soup.find_all("p")
    text = ""

    for points in mytext:
        point = str(points.text)
        text += point

    p = text
    p=p.replace('.', '. ')
   
    text = tokenize.sent_tokenize(p)
    
    mylist=[]

    term = "<ul>"
    
    for i in text:
        b = i
        i = re.sub("[^a-zA-Z0-9\s]+", " ",i)
        i = i.split()
        for w in i:
            if w==myword:
                term+="<li>" + b +"</li>"     
            elif w==myword2:
                term+="<li>" + b +"</li>"
           

    if term == "<ul>":
        term = "There is no such word."
    
    term += "</ul>"
    reg = re.compile(myword)
    reg2 = re.compile(myword2)
    values = re.findall(pattern=reg, string=term)
    sub_text = re.sub(pattern=reg, string=term, repl="<span style='color:blue;'>" + myword + "</span>")
    sub_text2 = re.sub(pattern=reg2, string=sub_text, repl="<span style='color:blue;'>" + myword2 + "</span>")
    jres = {'detail': sub_text2}
    return jsonify(jres)

@app.route('/api/fetch9', methods=['POST'])
def fetch9():
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