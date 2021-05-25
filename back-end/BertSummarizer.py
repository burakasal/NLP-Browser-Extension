from summarizer import Summarizer
import re

def bertSummarizer(text, data2): #data2 represets the sentence number input
    try:
        data2 = int(data2)-1
    except:
        data2 = data2
        return "The input is not valid"

    if data2 < 1:
            data2 = 1
    model = Summarizer()
    result = model(text, num_sentences=data2)
    result = re.sub("[^a-zA-Z0-9 -\.\,]","",result.strip()) 
    return result