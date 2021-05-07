import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup

def getSeveralData(taburl, sent, sent2):
    data = request.json[taburl]
    data2 = request.json[sent]

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

    if sent2:
        data3=request.json[sent2]
        return text, data2, data3
    return text, data2