from nltk import tokenize
from sumy.nlp.tokenizers import Tokenizer
import re
import pandas as pd
from LexiconCheck import lexiconCheck

def nertr(text):

        text = tokenize.sent_tokenize(text)

        myorg = ["Üniversitesi", "Koleji", "Okulu", "Kurumu", "Bankası", "Şirketi", "İştirakı", "Vakfı", "Federasyonu", "Kulübü", "Takımı", "Meclisi",  "Derneği", "Holdingi", "Teşkilatı",
                "Firması", "Bakanlığı", "Hastanesi", "Devleti", "Partisi", "Başkanlığı", "Komiserliği", "Belediyesi", "Belediyeleri", "Tiyatrosu", "İmparatorluğu", "Birliği","Bülteni", "Holding",
                "Danışmanlığı", "Müdürlüğü", "Enstitüsü", "Delegasyonu", "Büyükelçiliği", "Konseyi", "Parlamentosu", "Ofisi", "Kurulu", "Meclisi","Gazetesi","Bülteni","Basın Odası","Basın Odası",
                "Müsteşarlığı", "Parti", "A.Ş.", "şirketi", "Örgütü","Komutanlığı","Kuvvetleri","Operasyonu","Komitesi","Forumu", "Cumhuriyeti","Töreni","Komisyonu","Konseyi", "gazetesi","dergisi",
                "Birimi", "Danıştay","Yargıtay","Sayıştay", "Sekreterliği", "Mahkemesi","Teşkilatı","Bank","Ajansı","Kooperasyonu","Organizasyonu","Vakfı","Televizyonu",
                "savcılığı","Savcılığı","Başsavcılığı","kardeşi","Konferansı","kanalı", "Kanal'", "cemaati"]


        myname = ["Abi", "Ağabey", "Amca", "Dayı",
                "Bey", "Bay", "Hanım", "Bayan", "Hoca"]

        myname2 = ["Bakan", "Vali", "Müftü", "Kadı", "Kral", "Kraliçe", "Prens", "Prenses","CEO'su","yetkilisi","Muhabiri", "Editörü",
        "İmam", "Cumhurbaşkanı", "Sayın", "Sevgili", "Kıymetli", "Değerli", "Doktor", "Başbakanı", "Başkanvekili","nişanlısı", "arkadaşı olan","üyesi",
        "Hekim", "Avukat", "Öğretmen", "Profesör", "Doçent", "Başkan", "Yardımcısı","Muhabiri","Prof.", "Dr.", "başkanı", "Büyükelçisi", "Sözcüsü","danışmanı",
        "Lideri", "lideri", "yönetmen","Düşesi","sunucusu","ağabeyi","yöneticisi","Sekreteri","siyasetçi","öğretmen"] 

        myloc = ["Dağı", "Köprüsü", "Mezarı", "Saray", "Şehri", "Ülkesi", "Deresi", "Çayı", "Gölü","Çölü","anakarası","kıtası"
                "Otoyolu", "Köyü", "Kasabası", "Mahallesi", "Caddesi", "Dairesi", "Meydanı", "Rezidansı", "Meydanı", "Denizi", "Körfezi", "Kenti", "Tapınağı", "Kilisesi", "Otogarı",
                "Merkezi", "Okyanusu", "Kütüphanesi", "İstasyonu", "Kayalıkları", "Limanı", "Adası","adası", "Koyu", "Yaylası", "Tepesi", "Çayırı", "Yolu", "Kalesi", "Müzesi",
                "Boğazı", "Ocağı", "Koğuşu", "Stadyum", "Kortu", "Sahası", "Otel", "Hotel", "Pansiyon", "Mağaza", "Vadisi", "Geçidi", "İlçesi", "Beldesi", "ilçesi","bölgesi","kenti","başkenti"]
        loclist = []
        loclist=lexiconCheck(text, loclist, "sehir-ulke.txt")

        mytime=["yıl", "sene", "yüzyıl", "hafta", "gün", "saat", "dakika", "saniye", "ay"]
        aylar=["ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık"]





        orglist = []
        for line in text:  # each sentence
            for a in range(0, len(myorg)):
                myvar = myorg[a]
                if myvar in line:
                    mystr = re.findall(r'[A-ZÇĞİÖŞÜ\(][A-Za-zçğıöşü\(\)]*(?:\s+[A-ZÇĞİÖŞÜ\(][a-zçğıöşü\(\)]*)* ' + myvar, line)

                    for element in mystr:
                        orglist.append(element)
                a += 1


        basın_file = open("basınlar.txt", "r", encoding="utf8")
        basınf=[]
        for l in basın_file:
            if len(l)>1:
                basınf.append(l.strip())
        for line in text:
            for ele in range(0, len(basınf)):
                #print("eee", ele)
                #ele=ele.strip()
                #print("EEE", ele,"EEE")
                if basınf[ele] in line:
                    orglist.append(basınf[ele])


        namelist = []
        for line in text:  # each sentence
            for a in range(0, len(myname)):
                myvar = myname[a]
                if myvar in line:
                    mystr = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)*' + myvar, line)

                    for element in mystr:
                        namelist.append(element)
                a += 1
        for line in text:  # each sentence
            for a in range(0, len(myname2)):
                myvar = myname2[a]
                if myvar in line:
                    mystr = re.findall(myvar + r'\w*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)*', line)

                    for element in mystr:
                        element=element.replace(myvar, '')
                        if ord(element[0]) in range(97, 123) or element[0] == 'ı' or element[0] == 'ç' or element[0] == 'ö' or element[0] == 'ü':
                            element = element[element.find(' '):]
                        
                        namelist.append(element)
                a += 1




        for line in text:  # each sentence
            for a in range(0, len(myloc)):
                myvar = myloc[a]
                if myvar in line:
                    mystr = re.findall(
                        r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)* ' + myvar, line)

                    for element in mystr:
                        loclist.append(element)
                a += 1


        timelist = []
        for line in text:

            #aylar list  
            for a in range(0, len(aylar)):
                myvar = aylar[a]
                myvar2=myvar.capitalize()
                if myvar or myvar2 in line:
                    mystr = re.findall(r'\d{1,4}\s' + myvar +'\w*', line)
                    mystr2 = re.findall(r'\d{1,4}\s' + myvar2 +'\w*', line)

                    for element in mystr:
                        timelist.append(element)
                    for element in mystr2:
                        timelist.append(element)

                    #if months are not written together with the numbers
                    if len(mystr)==0 and len(mystr2)==0:
                        mystr = re.findall(myvar +r'\w*', line)
                        mystr = re.findall(myvar2 +r'\w*', line)
                        for element in mystr:
                            timelist.append(element)
                        for element in mystr2:
                            timelist.append(element)

                a += 1

            #mytime list
            for a in range(0, len(mytime)):
                myvar = mytime[a]
                if myvar in line:
                    mystr = re.findall(r'\d{1,4}\s' + myvar +'\w*', line)

                    for element in mystr:
                        timelist.append(element)
                a += 1

            if "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "0" in line:
                mystr = re.findall(r'\d{4}[\'][td][ea]', line)
                for element in mystr:
                    timelist.append(element)

                mystr = re.findall(r'\d\d[-\.]\d\d[-\.]\d{4}', line)
                for element in mystr:
                    timelist.append(element)

                #SONRA BAK !!!
                mystr = re.findall(r'\s\d{1,2}\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s+\d{4}', line)
                for element in mystr:
                    timelist.append(element)
                
                mystr = re.findall(r'\s\d{1,2}\s+[a-zçğıöşü]*\s+\d{4}', line)
                for element in mystr:
                    timelist.append(element)

                mystr = re.findall(r'[012]\d[:\.][012345]\d\s+', line)
                for element in mystr:
                    timelist.append(element)


        #filters out any duplicates.
        loclist = list(set(loclist))
        orglist = list(set(orglist))
        namelist = list(set(namelist))
        timelist = list(set(timelist))

        return orglist ,namelist, loclist, timelist
