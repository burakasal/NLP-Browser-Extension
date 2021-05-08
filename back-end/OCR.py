import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import io

def ocr():
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
        return term
    term += "</ul>"
    return term