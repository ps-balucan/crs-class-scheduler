# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 22:14:07 2021

@author: Philippe
"""

import genetic_algorithm



subjectList = []

sample_input = ["Fil 40 ", "CW 10 ", "CoE 115 TJK", "CoE 115 HWX", "CWTS 2 Engg DCS", "Math 10 ", "Archaeo 2 "]
length = len(sample_input)
mycsv = genetic_algorithm.load_csv()

possible_subjects = []
for input in sample_input:
    newSubject = Subject(input)
    possible_subjects.append(filter_subject(mycsv, input))
    for index, row in filter_subject(mycsv, input).iterrows():
        if (row['professor'] == "TBA" or row['professor'] == "CONCEALED"):
            row['professor'] = "TBA, TBA2"
        print(row['professor'])
        newCourse = Course(row['course number'], row['name'], row['professor'], row['schedule'].split(' ')[1])
        newCourse._meetingDay = parse_schedule(row['schedule'].split(' ')[0])
        newSubject._courses.append(newCourse)
    subjectList.append(newSubject)
    
    
    
genetic_algorithm.genetic_algorithm()