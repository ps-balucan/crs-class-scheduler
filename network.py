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
import random
import operator

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
        self._meetingDay = []
    def get_meetingDays(self):
        return self._meetingDay

        
class Subject:
    def __init__(self, name):
        self._name = name
        self._courses = []
    def get_courses(self):
        return self._courses
    
          

def parse_schedule(schedule):
    if ((len(schedule) > 1) and schedule[1].isupper()):
        if (not schedule[1].isupper()):
            return [schedule[0:2] , schedule[2:len(schedule)]]
        else:
            return [schedule[0] , schedule[1:len(schedule)]]
    else:
        return [schedule]


subjectList = []

sample_input = ["Fil 40", "MS 1" , "CW 10", "CoE 115", "Eng 11", "Math 10"]
length = len(sample_input)
mycsv = load_csv()

possible_subjects = []
for input in sample_input:
    newSubject = Subject(input)
    #possible_subjects.append(filter_subject(mycsv, input))
    for index, row in filter_subject(mycsv, input).iterrows():
        newCourse = Course(row['course number'], row['name'], row['professor'], row['schedule'].split(' ')[1])
        newCourse._meetingDay = parse_schedule(row['schedule'].split(' ')[0])
        newSubject._courses.append(newCourse)
    subjectList.append(newSubject)
    

def print_data(subjectList):
    for subject in subjectList:
        print("\n\n\t\t\t\tSubject Name: " + str(subject._name))
        for courses in subject._courses:
            print("Course Name: " + courses._courseName)
            print("Meeting Times: " + courses._meetingTime)
            print("Meeting Days: " + str(courses._meetingDay))
            print("Professor: " + courses._teacher)

class Schedule:
    def __init__(self):
        self.classes = []
        self.conflictNum = 0
        self.fitness = -1
        self.classNumb = 0
    def initialize(self, numberOfClasses):
        for i in range(0, numberOfClasses):
            self.classes.append(subjectList[i]._courses[random.randrange(0,len(subjectList[i]._courses))])
    def check_conflict(self):
        for i in range(0, len(self.classes)):
            for j in range(0, len(self.classes)):
                if (i < j):
                    print("test: " + self.classes[i]._courseName + " vs " + self.classes[j]._courseName)
                    if (check_class_conflict(self.classes[i], self.classes[j])):
                        self.conflictNum += 1

def print_schedule_data(schedule):
    print("\n\n\n\t\t\t\t\tSCHEDULE DATA ")
    for thing in schedule.classes:
        print(thing._courseName + "\t\t" + str(thing._meetingTime) + "\t\t" + str(thing._meetingDay))
    print("Number of Conflicts: " + str(schedule.conflictNum))
    print("Fitness: " + str(schedule.fitness))
    
def check_class_conflict(class1, class2):
    for day_in_class1 in class1._meetingDay:
        for day_in_class2 in class2._meetingDay:
            if day_in_class1 == day_in_class2:
                print("Comparing: " + class1._meetingTime[-2:] + " and " + class2._meetingTime[-2:])
                if (getOverlap(convertTodecimal(class1._meetingTime), convertTodecimal(class2._meetingTime))):
                    return True
    return False

def getOverlap(a, b):
     return max(0, min(a[1], b[1]) - max(a[0], b[0]))

def convertTodecimal(time):
    buffer = time.split('-')
    start_time = buffer[0]
    end_time = buffer[1]
    print("check here: " + str(buffer))
    if (start_time.find("AM") > 0 and end_time.find("PM")):
        start_time = start_time.replace("AM", "").replace("PM", "")
        end_time = end_time.replace("AM", "").replace("PM", "")
        if (start_time.find(":") > 0):
            start_time = start_time[:-3] + str(float(start_time[-2:])/60)[1:]
        if (end_time.find(":") > 0):
            end_time = end_time[:-3] + str(float(end_time[-2:])/60)[1:]
        return [float(start_time) , float(end_time)+12]
    elif (end_time.find("PM") > 0):
        start_time = start_time.replace("AM", "").replace("PM", "")
        end_time = end_time.replace("AM", "").replace("PM", "")
        if (start_time.find(":") > 0):
            start_time = start_time[:-3] + str(float(start_time[-2:])/60)[1:]
        if (end_time.find(":") > 0):
            end_time = end_time[:-3] + str(float(end_time[-2:])/60)[1:]
        return [float(start_time)+12 , float(end_time)+12 ]        
    else:
        start_time = start_time.replace("AM", "").replace("PM", "")
        end_time = end_time.replace("AM", "").replace("PM", "")
        if (start_time.find(":") > 0):
            start_time = start_time[:-3] + str(float(start_time[-2:])/60)[1:]
        if (end_time.find(":") > 0):
            end_time = end_time[:-3] + str(float(end_time[-2:])/60)[1:]
        return [float(start_time) , float(end_time) ]  
        
    

def crossover(scheduleA, scheduleB):
    for course in scheduleA.classes:
        print('woo')
    #for i in range(0, num_generations):
    
        
def evolve(pop):
    new_generation = []
    
    #ELITISM
    for i in range(0, NUM_ELITES):
        new_generation.append(pop[i])
        
    #CROSSOVER
    
    
    
def generate_population(num_population):
    population = []
    for i in range(0, num_population):
        newSchedule = Schedule()
        newSchedule.initialize(len(sample_input))
        newSchedule.check_conflict()
        population.append(newSchedule)
        
    population.sort(key=operator.attrgetter('conflictNum'))
    return population

NUM_POPULATION = 10
NUM_ELITES = 3

print("GENERATION#0")
unogeneracion = generate_population(NUM_POPULATION)
for schedule in unogeneracion:
    print_schedule_data(schedule)
    
    
    





                