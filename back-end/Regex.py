import re

def regex(text, data2):

    data2= r'' + data2 
    result=re.findall(data2, text)

    if len(result)==0:
        mysent="Expression is not found"
        result.append(mysent)
        jres = {'detail2': result}
        return jsonify(jres)

    term = "<ul>"
    
    for i in result:
        i=i.strip()
        if len(i)>0:
            term+="<li>" + i +"</li>"
    
    term += "</ul>"
    
    if term=="<ul></ul>":
        term="Expression is not found"

    return term
