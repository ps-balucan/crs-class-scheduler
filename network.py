# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 22:10:33 2021

@author: Philippe
"""

import requests
from bs4 import BeautifulSoup
import string
import csv as csv
import pandas as pd

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
        d['schedule'] = row.findAll('td')[3].text.strip().split('\n')[0].rsplit(" ", 2)[0]
        print(d['schedule'])
        
        if (len(row.findAll('td')[3].text.strip().split('\n')) == 1 ):
            d['professor'] = d['schedule']
            d['schedule'] = "TBA"
            continue
        
        d['professor'] = row.findAll('td')[3].text.strip().split('\n')[1].strip('\t')
        
        data.append(d)
    print(data[0])
    return data

def create_csv():
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

def load_csv():
    data = pd.read_csv('crs.csv', encoding = "ISO-8859-1", engine='python')
    data.head()
    return data

def filter_subject(mycsv, search_name):
    return mycsv[mycsv["name"].str.contains(search_name, na=False, case=False)]

class Course:
    def __init__(self, id, courseName, teacher, meetingTime):
        self._id = id
        self._courseName = courseName
        self._teacher = teacher
        self._meetingTime = meetingTime
        
class Subject:
    def __init__(self, name):
        self._name = name
        self._courses = []
    def get_courses(self):
        return self._courses
    
          
        
        
subjectList = []

sample_input = ["Fil 40", "MS 1" , "CW 10", "CoE 115"]
length = len(sample_input)
mycsv = load_csv()

possible_subjects = []
for input in sample_input:
    newSubject = Subject(input)
    #possible_subjects.append(filter_subject(mycsv, input))
    for index, row in filter_subject(mycsv, input).iterrows():
        newSubject._courses.append(Course(row['course number'], row['name'], row['professor'], row['schedule']))
        #print("Name: " + str(row['name']))
    subjectList.append(newSubject)
    #mylist = [(Course(id, row.name, row.professor, row.schedule)) for index, row in filter_subject(mycsv, input).items()]
    

for subject in subjectList:
    print("\n\n\t\t\t\tSubject Name: " + str(subject._name))
    for courses in subject._courses:
        print("Course Name: " + courses._courseName)
        print("Meeting Times: " + courses._meetingTime)
        print("Professor: " + courses._teacher)




