from langdetect import detect_langs
from langdetect import DetectorFactory
DetectorFactory.seed = 0
def languagedetect(text):
    try:
        lang_list=detect_langs(text)
    except:
        result="The language could not be detected"
        res="en"
        return result, res

    langs=[]
    probs=[]
    for i in lang_list:
        i=str(i)
        langs.append(i[0:2])
        probs.append(i[3:7])
    res = langs[0]
    mydict = {"en": "English", "tr": "Turkish", "de": "German", "es": "Spanish", "fr": "French"}

    for i in range(0, len(langs)):
      lang2 = mydict.get(langs[i])
      if(lang2 != None):
          langs[i]=lang2

    result=""
    
    for i in range(0, len(langs)):
        result += "Page language is '" + str(langs[i]) + "' with " + probs[i] + " reliability score"  + "<br>"

    return result, res