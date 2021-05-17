import re
from sklearn.feature_extraction.text import TfidfVectorizer

def termWeigthing(text):
    # Pre-processing
    stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
                 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    stopWords = ['acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her',
             'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani']             
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
    return term
