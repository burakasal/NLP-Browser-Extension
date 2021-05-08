from summarizer import Summarizer
import re
def bertSummarizer(text, data2):
    data2 = int(data2)-1
    if data2 < 1:
        data2 = 1
    model = Summarizer()
    result = model(text, num_sentences=data2)
    result = re.sub("[^a-zA-Z0-9 -\.\,]","",result.strip()) #SONRA BAK!!!
    return result