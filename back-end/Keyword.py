import nltk
from nltk import tokenize
import re


def keyword(text,data2,data3):
    #text is the webpage content, data2 is the keyword input, data3 is the case sensitivity input
    data2 = str(data2)
   
    if data3 == "0": #Case sensitive, consider both lowered and capitalized versions of the word
        myword = data2.lower()
        myword2 = data2.capitalize()
    else:    # data3=1, not case sensitive, consider only the original word (ignore myword2)
        myword = data2
        myword2 = data2
    
    p = text
    p=p.replace('.', '. ')
   
    text = tokenize.sent_tokenize(p) #text is splitted into sentences (as an array)
    mylist=[]
    term = "<ul>" #these tags are added to represent the outcome as bulletpoints in the output box.
    
    for i in text:  #i=sentences
        b = i # b stores the original value of the sentences ( to return at the end)
        i = re.sub("[^a-zA-Z0-9\sÇĞİÖŞÜçğıöşü]", " ",i) #processing the text 
        i = i.split()
        for w in i:
            if w==myword:
                term+="<li>" + b +"</li>"     
            elif w==myword2:
                term+="<li>" + b +"</li>"
           
    if term == "<ul>": #no word is detected in sentences
        term = "There is no such word."
    
    term += "</ul>"

    reg = re.compile(myword)
    reg2 = re.compile(myword2)

    sub_text = re.sub(pattern=reg, string=term, repl="<span style='color:blue;'>" + myword + "</span>") #coloring the keyword to blue
    sub_text2 = re.sub(pattern=reg2, string=sub_text, repl="<span style='color:blue;'>" + myword2 + "</span>") 

    return sub_text2