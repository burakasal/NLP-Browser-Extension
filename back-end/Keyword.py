import nltk
from nltk import tokenize
import re


def keyword(text,data2,data3): #text is the webpage content, data2 is the keyword input, data3 is the case sensitivity input
    data2 = str(data2)
   
    if data3 == "0": #Case sensitive, consider both lowered and capitalized versions of the word
        myword = data2.lower()
        myword2 = data2.capitalize()
    else:    # data3=1, not case sensitive, consider only the original word (ignore myword2)
        myword = data2
        myword2 = data2
    
    myword = re.sub("[^a-zA-Z0-9\sÇĞİÖŞÜçğıöşü]", "",myword)
    myword2 = re.sub("[^a-zA-Z0-9\sÇĞİÖŞÜçğıöşü]", "",myword2)

    if len(myword)==0:
        result="The keyword input is not valid"
        return result
        
    myword= " " + myword
    myword2= " " + myword2

    p = text
    p=p.replace('.', '. ')
   
    text = tokenize.sent_tokenize(p) #text is splitted into sentences (as an array)
    mylist=[]
    term = "<ul>" #these tags are added to represent the outcome as bulletpoints in the output box.
    
    for i in text:  #i=sentences
        b = i # b stores the original value of the sentences (to return at the end)
        i = i.split()
        ind=0
        for w in i:
            w=w.strip()
            w=" "+ w
            mystr = re.findall(myword + r'\w{0,1}\b', w) #this allows last letter to vary, in case there is a punctuation mark
            mystr2 = re.findall(myword2 + r'\w{0,1}\b', w)

            if mystr:
                mywordn="<span style='color:blue;'>" + w + "</span>"
                i[ind]=mywordn
                i=" ".join(i)
                term+="<li>" + i +"</li>" 

            elif mystr2:
                myword2n="<span style='color:blue;'>" + w + "</span>"
                i[ind]=myword2n
                i=" ".join(i)
                term+="<li>" + i +"</li>"
            ind+=1
           
    if term == "<ul>": #no word is detected in sentences
        term = "There is no such word."
    
    term += "</ul>"

    return term