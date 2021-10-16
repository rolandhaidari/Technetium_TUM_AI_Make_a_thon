
import requests
import re
from bs4 import BeautifulSoup
import json


#URL = 'https://immobilien.sparkasse.de/immobilien/bayern/muenchen.html'
URL = 'https://immobilien.sparkasse.de/immobilien/nrw/bonn.html'

global r
r = requests.get(URL)

def prices(r):
    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all('a', {'class': 'estate-item'})
    alllinks=[]
    for l in links:
        alllinks.append(l.get('href'))
    return alllinks



# Click on the next button if it is available.
'''
Example HTML:
    <a class="icon-container pull-right seo-forward" href="https://immobilien.sparkasse.de/immobilien/bayern/muenchen/2.html"><span class="icon-text">weiter</span><span class="icon icon-arrow-right-grey"></span></a>
'''
def click_next(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a', {'class': 'icon-container pull-right seo-forward'})
    alllinks=[]
    for l in links:
        #print("l:", l)
        #print('Next page')
        # Load the next page
        r = requests.get(l.get('href'))
        returnedlinks=prices(r)
        for rl in returnedlinks:
            alllinks.append(rl)
        #names(r)
        for i in click_next(r):
            alllinks.append(i)
    return alllinks

def getAllLinks(r):
    alllinks=prices(r)
    for i in click_next(r):
        alllinks.append(i)
    #print(alllinks)
    return alllinks

def getFields(link):
    r= requests.get(link)
    #print("getting link "+link)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find_all('div', {'class': 'sip-estate'})
    allData=[]

    for d in data:
        estateInfo=d.get('data-props')
        #print(estateInfo)

        estate=json.loads(estateInfo)
        allData.append({"estateId":estate["estateId"]})
        #print(estate["estateId"])
        estateData=estate["estateData"]

        #print("estateData")
        #print(estateData)
        
        es=json.loads(estateData)
        es=es["estate"]
        
        #print(es)
        
        title=es["title"]
        allData.append({"title":title})
        subtitle=es["subtitle"]
        allData.append({"subtitle":subtitle})
        blz=es["blz"]
        allData.append({"blz":blz})
        
        geo=es["geo"]
        geo=geo["coordinates"]
        lat=geo["lat"]
        lat=float(lat.replace(",","."))
        allData.append({"lat":lat})
        lng=geo["lng"]
        lng=float(lng.replace(",","."))
        allData.append({"lng":lng})

        mainf=es["mainfacts"]
        #price=mainf["Kaufpreis"]
        try:
            type="Kauf"
            price=float((mainf["Kaufpreis"]).replace("€", "").replace(".","").replace(",","."))
        except:
            #type="Miete"
            #try:
            #SKIP MIETE
            allData=[]
            return allData
            #    price=float((mainf["Nettokaltmiete"]).replace("€", "").replace(".","").replace(",","."))
            #except:
                #print("failed because of missing type")
                #print(mainf)
                #price=0
        #print(price)
        allData.append({"type":type})
        allData.append({"price":price})
        try:
            size=mainf["Wohnfl\u00e4che"]
            if size:
                size=float(mainf["Wohnfl\u00e4che"].replace("m²", "").replace(" ","").replace(",","."))
        except KeyError:
            size=None
        #print(size)
        allData.append({"size":size})
        
        try:
            rooms=float(mainf["Zimmer"].replace(",","."))
        except:
            rooms=0
        allData.append({"rooms":rooms})
        #print(rooms)

        items=es["frontend"]
        items=items["items"]

        for i in items:
            #print(i)
            label=i["label"]
            if label=="Objektbeschreibung":
                contents=i["contents"]
                descriptionContents=contents[0]["data"]["content"]
                allData.append({"descriptionContentents":descriptionContents})
                #print(descriptionContents)
            if label=="Ausstattung":
                equipmentData=i["contents"]
                equipmentData=equipmentData[0]["data"]
                for d in equipmentData:
                    try:
                        value=d["value"]
                    except:
                        print(d)
                        value=d
                    split=value.split(": ")
                    header="Ausstattung_"+split[0].replace(" ","_")
                    if len(split)>1:
                        val=split[1]
                    else:
                        val=True
                    if header in ["Ausstattung_Heizungsart","Ausstattung_Bad","Ausstattung_Küche","Ausstattung_Boden","Ausstattung_Wesentlicher_Energieträger","Ausstattung_Stellplatzart","Ausstattung_Fahrstuhl"]:
                        newvalues=val.split(", ")
                        for v in newvalues:
                            try:
                                header+="_"+v
                            except:
                                print(value)
                                print(val)
                                print(v)
                                print(header)
                                allData.append({header: val})
                                continue
                            val=True
                            allData.append({header.replace(" ","_"): val})
                    else:
                        allData.append({header: val})
                
            if label=="Lage":
                contents=i["contents"]
                state=contents[0]["data"]["content"].replace(";",":")
                allData.append({"state":state})
            #IGNORING SONSTIGEN BECAUSE I'M LAZY
            #if label=="Sonstiges":
            #    print("Sonstiges")
            if label=="Preise / Kosten":
                priceData=i["contents"]
                priceData=priceData[0]["data"]
                
                for d in priceData:
                    value=d["value"]
                    try:
                        value=value.replace("€", "").replace("m²", "m2").replace(".","").replace(" % (inkl. MwSt.)","").replace(" % (inkl MwSt)","").replace(" pa","")
                        value=float(value)
                    except:
                        pass
                    header="Cost_"+d["label"]
                    header=header.replace(" ","_").replace("m²", "m2").replace(",", "_")
                    allData.append({header: value})
            if label=="Objektdaten":
                priceData=i["contents"]
                priceData=priceData[0]["data"]
                
                for d in priceData:
                    value=d["value"]
                    try:
                        value=value.replace("€", "").replace("m²", "m2").replace(".","").replace(" % (inkl. MwSt.)","").replace(" % (inkl MwSt)","").replace(" pa","")
                        tmp=value.replace("m2","")
                        value=float(tmp)
                    except:
                        pass
                    header="Object_"+d["label"]
                    if header=="Object_Verfügbar_ab":
                        value=d["value"]
                    header=header.replace(" ","_").replace("m²", "m2").replace(",", "_")
                    allData.append({header: value}) 
            if label=="Zustand & Energieausweis":
                priceData=i["contents"]
                priceData=priceData[0]["data"]
                
                for d in priceData:
                    value=d["value"]
                    try:
                        value=value.replace("€", "").replace(".","").replace(" % (inkl. MwSt.)","").replace(" % (inkl MwSt)","").replace(" pa","").replace(" kWh/(m²*a)","")
                        value=float(value)
                    except:
                        pass
                    header="Zustand_"+d["label"]
                    header=header.replace(" ","_").replace("m²", "m2").replace(",", "_")
                    allData.append({header: value})

    return allData
        


def makeCSV(allData):
    #print("making csv")
    usedColumns=[]
    for datavalue in allData:
     #   print(datavalue)
        for val in datavalue:
            for key in val.keys():
                if not (key in usedColumns):
                    usedColumns.append(key)
      
   # print(usedColumns)
    for column in usedColumns:
        print(column, end=";")
    print()
    for datavalue in allData:
        for column in usedColumns:
            found=False
            for val in datavalue:
                value=val.get(column)
                if value:
                    if isinstance(value, (int, float)):
                        print(value, end=";")
                    else:
                        print("\""+' '.join(value.splitlines())+"\"", end=";")
                    found=True
            if not found:
                print("", end=";")
        print()

        





if __name__ == '__main__':
    #prices(r)
    #names(r)

    alllinks=getAllLinks(r)
    #alllinks=["https://immobilien.sparkasse.de/FIO-10916182170?origin=content","https://immobilien.sparkasse.de/FIO-10916130380?origin=content"]
    allData=[]
    for link in alllinks:
        returned=getFields(link)
        allData.append(returned)
    makeCSV(allData)
    
