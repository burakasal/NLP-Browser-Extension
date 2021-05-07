import nltk
from nltk import tokenize
import re


def keyword(text,data2,data3):
    data2 = str(data2)
    
    if data3 == "0": #Case sensitive
        myword = data2.lower()
        myword2 = data2.capitalize()
    else:    
        myword = data2
        myword2 = data2
    

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
    sub_text = re.sub(pattern=reg, string=term, repl="<span style='color:blue;'>" + myword + "</span>")
    sub_text2 = re.sub(pattern=reg2, string=sub_text, repl="<span style='color:blue;'>" + myword2 + "</span>")

    return sub_text2