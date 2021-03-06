from langdetect import detect
import sumy 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def lexRankSummarizer(text, data2): #data2 represents the sentence number input
    try:
        data2 = int(data2) 
    except:
        data2 = data2
        return "The input is not valid"

    if data2 < 1:
        data2 = 1
    
    lang=detect(text)
    mydict = {"en": "english", "tr": "turkish", "de": "german", "es": "spanish", "fr": "french"} #this function only works for these languages, more languages can be added to the dictionary
    lang2 = mydict.get(lang)
    if(lang2 == None): #if the detected language is not in the dictionary
        return "This language is not supported for summary function."
        
    my_parser = PlaintextParser.from_string(text,Tokenizer(lang2))
    lex_rank_summarizer = LexRankSummarizer()
    lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=data2)

    # Printing the summary
    result=""
    for sentence in lexrank_summary:
        sentence=str(sentence)
        result += sentence

    result = result.replace(".",". ")
    return result