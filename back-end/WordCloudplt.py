from wordcloud import WordCloud
import re
import nltk
from nltk import tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot as plt

 
def wordCloud(text):

    sword = ['acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her',
             'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani']
    sword2 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
              'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


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

    return plt