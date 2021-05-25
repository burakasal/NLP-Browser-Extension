import flask
from flask import request, jsonify
import collections
from langdetect import detect
import os
from GetData import getData
from TermWeighting import termWeigthing
from enNER import nerEng
from trNER import nertr
from Regex import regex
from GetSeveralData import getSeveralData
from WordCloudplt import wordCloud
from Keyword import keyword
from OCR import ocr
from LexrankSummarizer import lexRankSummarizer
from BertSummarizer import bertSummarizer
from LanguageDetect import languagedetect

app = flask.Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run()

@app.route('/api/btnlangDetect', methods=['POST'])
def btnlangDetect():
    text=getData(False)
    result, lang = languagedetect(text) 
    jres = {'language': result,
            'language2': lang}
    return jsonify(jres)

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
    my_path = os.path.abspath(__file__) 
   
    plt.savefig(my_path)
    jres = {'detail': plt.show()}
    return jsonify(jres)


@app.route('/api/btnSum', methods=['POST'])
def btnSum():
    text,data2=getSeveralData("taburl", "SentNum", False)
    result = lexRankSummarizer(text, data2)

    jres = {'detail': result}
    return jsonify(jres)

@app.route('/api/btnBertSum', methods=['POST'])
def btnBertSum():
    text,data2=getSeveralData("taburl", "SentNum", False)
    result = bertSummarizer(text, data2)

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
    term = ocr()
    jres = {'detail': term}

    return jsonify(jres)

 