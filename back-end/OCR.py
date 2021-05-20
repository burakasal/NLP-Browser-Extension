import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import io
import re

def ocr():
    data = request.get_data()
    data2 = data.decode("ascii")
    html_content = requests.get(data2).text
    soup = BeautifulSoup(html_content, 'lxml')
    images = soup.find_all("img") #Find all image tags
    image_list = []
    for image in images:
        a = str(image)

        if ".png" in a or ".svg" in a or ".jpg" in a: #Check if it is a valid image
            image_list.append(image["src"]) #Append the src to the list which contains the image link
            
    term = "<ul>"
    
    for i in image_list:
        try:
            if "http" not in i: #Http is added to the link if it does not exist, for get request
                i="http:" +i
            response = requests.get(i)
            img = Image.open(io.BytesIO(response.content))
            a = pytesseract.image_to_string(img)
            if a.strip():
                a=re.sub(r'[^A-Za-z0-9]', "", a)
                term+="<li>"+ a+ "</li>"
        except:
            continue       
   
    if term == "<ul>":
        term = "There is no image."
        return term
    term += "</ul>"
    return term