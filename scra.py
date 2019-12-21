import requests
import json
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from my_data import cookies, headers #you should get thes from the website https://curl.trillworks.com/ when you get the cURL request

url_names_strains = []
all_objects=[]
for i in tqdm(range(0,200)):
    
    skip = i*60
    sk = str(skip)
    params = (
        ('', ''),
        ('sort/[0/]/[popular/]', 'asc'),
        ('take', '60'),
        ('skip', sk),
    )

    response = requests.get('https://consumer-api.leafly.com/api/strains/v1', headers=headers, params=params, cookies=cookies)
    try:
        assert response.status_code == 200
    except:
        print("wrong")
    data = json.loads(response.text)
    elements = data["data"]
    all_objects.extend(elements)
    
    for el in elements:
        url_names_strains.append(el['slug'])
        

url = 'https://www.leafly.com/strains/'
db=[]
def is_float(n):
    try:
        float(n)
        return True
    except:
        return False

url_names_strains = list(set(url_names_strains))
print(len(url_names_strains))
for el in tqdm(url_names_strains):
    response = requests.get(url+el)
    try:
        assert response.status_code == 200
    except:
        print("wrong")
    
    soup = BeautifulSoup(response.text, "html.parser")
    obj={}
    obj['name']=el
    try:
        data1 = soup.findAll("div", {"class": "self-end"})
        rating = data1[0].text.split(" ")[0]
        reviews = data1[0].text.split(" ")[1]
    except:
        reviews="0"
        rating="0"
    obj['reviews'] = reviews
    obj['rating'] = rating

    data2 = soup.findAll("div", {"class": "font-body"})
    cannbinoids= ""
    try:
        if is_float(data2[0].text[:-1]):
            cannbinoids = data2[0].text[:-1]
    except:
        pass
    obj['cannbinoids'] = cannbinoids



    data3 = soup.findAll("div", {"data-testid": "terpBarContainer"})
    try:
        terpenes = list(set([a.text for a in data3[0].findAll("div") if a.text != ""]))
    except:
        terpenes= []
    obj['terpenes'] = terpenes


    tag = 'calm-energize__mark bg-leafly-white absolute top-0 bottom-0'
    data4 = soup.findAll("div", {"class": tag})
    try:
        calming_percentage = data4[0].get('style')[data4[0].get('style').rfind(":")+1:-1]
    except:
        calming_percentage=[]
    obj['calming_percentage'] = calming_percentage

    data5 = soup.findAll("div", {"role": "tabpanel"})
    
    try:
        feelings = data5[0].text.split("%")
        helps_with = data5[1].text.split("%")
        negatives = data5[2].text.split("%")
    except:
        feelings = []
        helps_with = []
        negatives = []
    obj['feelings'] = feelings
    obj['helps_with'] = helps_with
    obj['negatives'] = negatives

    t = 'flex items-center font-mono text-xs'
    data6 = soup.findAll("div", {"class": t})
    try:
        people_reported = data6[0].text
        people_reported[:people_reported.find(" ")]
        if is_float(people_reported[:people_reported.find(" ")]):
            reports_people = people_reported[:people_reported.find(" ")]
    except:
        reports_people="0"
    obj['reports_people'] = reports_people

    db.append(obj)
with open('data_obj_leafly.json', 'w') as fp:
    json.dump(db, fp)
print("filed saved")
