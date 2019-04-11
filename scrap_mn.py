#!/bin/python  
# Python 3.5
# Installer le driver (voir : https://selenium-python.readthedocs.io/)
import requests
from bs4 import BeautifulSoup as bs
import datetime
import csv
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import re
from selenium import webdriver
print('Python version ' + sys.version)
print('Numpy version ' + np.__version__)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)


# Utilisation de Selenium pour lire les données dynamique
# Début Selenium
driver = webdriver.Chrome()
driver.get('https://masternodes.online/')

select = driver.find_element_by_name("masternodes_table_length")
select.click()
select.send_keys('a')
select.click()

r = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
# Fin Selenium

# --------------------------------------------------------------------
# Le code Commenté prend le html sans analyser les variables javascript
# url = "https://masternodes.online/#masternode-stats" # ouverture avec selenium
# r= requests.get(url)
# --------------------------------------------------------------------

html = r
soup = bs(html, "html.parser")
table1 = soup.find("table", {"id": "masternodes_table"})
row = table1.find_all('tr')
cells = table1.find_all('td')
data =[]
today = datetime.datetime.now().strftime("%y-%m-%d")
filename = ("MNO-"+today+".csv")



#html dans un dictonaire  
titles = []
"""
# Titres
for c,i in enumerate(row):
    if(c==0):
        print(i.text+ "  "+str(c))
"""
for c,i in enumerate(cells):
    data.append(i.text)

coin = data[2::11]
price = data[3::11]
change = data[4::11]
volume = data[5::11]
mkap = data[6::11]
roi = data[7::11]
ncount = data[8::11]
coinreq = data[9::11]
tprice = data[10::11]

table = {}
col_names = ['coin','price','change','volume', 'mkap', 'roi', 'ncount', 'coinreq', 'tprice']


# séparateur décimal .
for i,c in enumerate(coin):
    table[c] = price[i].replace('$','').replace(',',''),\
    change[i].replace('%','').replace(',',''),\
    volume[i].replace('$','').replace(',','').replace('.',','),\
    mkap[i].replace('$','').replace(',','').replace('.',',').replace('?','0'),\
    roi[i].replace('%','').replace(',',''),\
    ncount[i].replace(',',''),\
    coinreq[i].replace(',',''),\
    tprice[i].replace('$','').replace(',','').replace('.',',') 
    
# Création du tableau
tdata = pd.DataFrame.from_dict(table, orient='index', dtype='float')

# Nommer les colonnes
tdata.columns = ['Prix($)','Change', 'Volume', 'Mkap','ROI','Nodes','Requis','MN_worth']

# Ajout de colonnes
tdata['Day-income'] = ((tdata['ROI']/100)/365)*tdata['MN_worth']
tdata['ROI_days'] = (365/(tdata['ROI']/100))
# Passe du type float en int
tdata['Volume'] = tdata['Volume'].astype('int32')
tdata['Mkap'] = tdata['Mkap'].astype('int32')
tdata['Nodes'] = tdata['Nodes'].astype('int32')
tdata['Requis'] = tdata['Requis'].astype('int32')
tdata['MN_worth'] = tdata['MN_worth'].astype('int32')


#ecriture csv
location = "~/Documents/Web_scrap/"
save = location+filename
tdata.to_csv(save)






pd.set_option('display.max_columns', 14) 
emplacement = ('~/Documents/Web_scrap/')

today = datetime.datetime.now().strftime("%y-%m-%d")
fichier = ("MNO-"+today+".csv")
fichier = emplacement+fichier
mncsv = pd.read_csv(fichier)

# Vérification du type pour chaque colonnes
bc=tdata.columns
col = ((pd.DataFrame([bc,tdata.dtypes]))
       .T).rename(columns={0: "Nom du champ", 1: "Type de donnée"})




bc=tdata.columns
col = ((pd.DataFrame([bc,tdata.dtypes])).T).rename(columns={0: "Nom du champ", 1: "Type de donnée"})





# Le filtre et : Mkap >= 50 000 $, ROI >= 70%, moins de 1500 MN et ayant un volume/day > au prix du prix d'un MN

data_select = tdata[(tdata['Mkap'] >= 50000) & (tdata['ROI'] >= 70)  & (tdata['Nodes'] <= 1500)
                   & (tdata['Volume'] >= tdata['MN_worth'])]
# tris par ROI
data_select = data_select.sort_values(by=['ROI'],ascending=False)

#ecriture csv
date_fichier = datetime.datetime.now().strftime("%y-%m-%d")
fichier = ("MNO_F1-"+date_fichier+".csv")
repertoir = "~/Documents/Web_scrap/"
sauve = repertoir+fichier
data_select.to_csv(sauve)