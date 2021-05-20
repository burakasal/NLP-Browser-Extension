import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup

def getData(array):
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml') #Parsing
    for a in soup.findAll('a', href=True):
        a.decompose() #Remove all 'a' tags which contain links
    footer_tag = soup.footer
    if footer_tag == True:
        footer_tag.decompose() #Remove footer tags
    mytext = soup.find_all("p")
    if(array):
        text = []
        for points in mytext:
            point = str(points.text)
            text.append(point)
    else:        
        text = ""
        for points in mytext:
            point = str(points.text)
            text += point    
        text = text.replace(".",". ")    
    return text     