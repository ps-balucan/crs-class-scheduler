# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 22:10:33 2021

@author: Philippe
"""

import requests
from bs4 import BeautifulSoup
import string
import csv as csv

base = 'https://crs.upd.edu.ph/schedule/'
year = '120202/'
letter = 'A'



def save_html(url, path):
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
        
    
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()
    
def access_html(letter):
    print('checking letter : ' + letter)
    url = base + year + letter
    r = requests.get(url)
    html = r.content
    
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tbody tr')
    data = []
    
    if(len(rows) == 1):
        return data
    
    for row in rows:
        d = dict()
        d['course number'] = row.findAll('td')[0].text.strip()
        print(d['course number'])
        if (not (d['course number'].isnumeric())):
            continue
        d['name'] = row.findAll('td')[1].text.strip()
        d['units'] = row.findAll('td')[2].text.strip()
        d['schedule'] = row.findAll('td')[3].text.strip().split('\n')[0]
        
        if (len(row.findAll('td')[3].text.strip().split('\n')) == 1 ):
            d['professor'] = d['schedule']
            d['schedule'] = "TBA"
            continue
        
        d['professor'] = row.findAll('td')[3].text.strip().split('\n')[1].strip('\t')
        
        data.append(d)
    print(data[0])
    return data


mycsv = []
for letter in list(string.ascii_uppercase):
    result = access_html(letter)
    if result:
        mycsv = mycsv + result



keys = mycsv[0].keys()

with open('crs.csv', 'a', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file,keys)
    dict_writer.writeheader()
    dict_writer.writerows(mycsv)

