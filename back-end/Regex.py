import re

def regex(text, data2): 
    #text is the webpage content, data2 is the regular expression input

    data2= r'' + data2 
    result=re.findall(data2, text)

    if len(result)==0:
        mysent="Expression is not found"
        result.append(mysent)
        return result

    term = "<ul>" #these tags are added to represent the outcome as bulletpoints in the output box.
    
    #in case there is a wrong input entrance, it is checked whether the resulting match is nonempty, empty matches are not included in the output
    for i in result:
        i=i.strip()
        if len(i)>0:
            term+="<li>" + i +"</li>"
    
    term += "</ul>"
    
    #if all of the matches are empty, there is no match
    if term=="<ul></ul>":
        term="Expression is not found"

    return term
