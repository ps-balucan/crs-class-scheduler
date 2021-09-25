# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 00:39:24 2021

@author: Philippe
"""

import random
import operator
import json
import io
import pandas as pd

NUM_POPULATION = 10
NUM_ELITES = 3
MUTATION_RATE = 0.5
TRY_LUNCH_BREAK = 0
MINIMIZE_BREAKS = 0
LUNCH_BREAK = "12-1PM"#"11AM-1PM"

filename = "ratings.txt"
with io.open(filename, 'r', encoding='utf8') as f:
    mystring = f.read()
    
ratings = json.loads(mystring)


class Course:
    def __init__(self, id, courseName, teacher, meetingTime):
        self._id = id
        self._courseName = courseName
        self._teacher = teacher
        self._meetingTime = meetingTime
        self._meetingDay = []
        self._rating = update_rating(teacher)
    def get_meetingDays(self):
        return self._meetingDay
    
class Schedule:
    def __init__(self):
        self.classes = []
        self.conflictNum = 0
        self.fitness = -1
        self.classNumb = 0
        self.longestBreak = 0
        self.lunchBreakconflict = 0
    def initialize(self, numberOfClasses, subjectList):
        for i in range(0, numberOfClasses):
            self.classes.append(subjectList[i]._courses[random.randrange(0,len(subjectList[i]._courses))])
    def check_conflict(self):
        for i in range(0, len(self.classes)):
            for j in range(0, len(self.classes)):
                if (i < j):
                    #print("test: " + self.classes[i]._courseName + " vs " + self.classes[j]._courseName)
                    res = check_class_conflict(self.classes[i], self.classes[j])
                    if (res[0]):
                        self.conflictNum += 1
                    self.longestBreak += res[1]
                    
    def check_lunch_break(self):
        overlap = 0
        for i in range(0, len(self.classes)):    
            for day in (self.classes[i]._meetingDay):
                overlap += getOverlap(convertTodecimal(LUNCH_BREAK), convertTodecimal(self.classes[i]._meetingTime))
        #print("amount of time overlapping with lunch break: " +  str(overlap))
        self.lunchBreakconflict = overlap
        
    def check_fitness(self):
        total = 0
        for unit in self.classes:
            total += unit._rating
        average = total/len(self.classes)
        #self.fitness = average/5 + 1/(self.conflictNum+1) - self.lunchBreakconflict*0.5
        self.fitness = average - self.lunchBreakconflict*0.4*TRY_LUNCH_BREAK - self.conflictNum*0.8 - self.longestBreak*0.2*MINIMIZE_BREAKS
        
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



def print_data(subjectList):
    for subject in subjectList:
        print("\n\n\t\t\t\tSubject Name: " + str(subject._name))
        for courses in subject._courses:
            print("Course Name: " + courses._courseName)
            print("Meeting Times: " + courses._meetingTime)
            print("Meeting Days: " + str(courses._meetingDay))
            print("Professor: " + courses._teacher)



def print_schedule_data(schedule):
    print("\n\n\n\t\t\t\t\tSCHEDULE DATA ")
    for thing in schedule.classes:
        print(thing._courseName + "\t\t" + str(thing._meetingTime) + "\t\t" + str(thing._meetingDay) + " rating: " + str(thing._rating))
    print("Number of Conflicts: " + str(schedule.conflictNum))
    print("Fitness: " + str(schedule.fitness))
    print("Break_Hours: " + str(schedule.longestBreak))
    
def check_class_conflict(class1, class2):
    class_gap_total = 0 
    overlap = 0
    for day_in_class1 in class1._meetingDay:
        for day_in_class2 in class2._meetingDay:
            if day_in_class1 == day_in_class2:
                overlap = getOverlap(convertTodecimal(class1._meetingTime), convertTodecimal(class2._meetingTime))
                if(not overlap):
                    class_gap_total = countGap(convertTodecimal(class1._meetingTime), convertTodecimal(class2._meetingTime))                   
    
    if (overlap):
        return (True, class_gap_total)
    else:
        return (False, class_gap_total)

def countGap(a, b):
    if (not getOverlap(a,b)):
        if (max(a) > max(b)):
            return min(a)-max(b)
        else:
            return min(b) - max(a)
        

def getOverlap(a, b):
     return max(0, min(a[1], b[1]) - max(a[0], b[0]))
    
def convertTodecimal(time):
    buffer = time.split('-')
    start_time = buffer[0]
    end_time = buffer[1]
    #print("check here: " + str(buffer))
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
        
    

def crossover(scheduleA, scheduleB, subjectList):
    if (not len(scheduleA.classes) == len(scheduleB.classes)):
        raise Exception("scheduleA must be the same length as schedule B")
    
    crossoverSchedule = Schedule()
    crossoverSchedule.initialize(len(subjectList), subjectList)
    for i in range(0, len(scheduleA.classes)):
        if (random.random() > 0.5):
            crossoverSchedule.classes[i] = scheduleA.classes[i]
        else:
            crossoverSchedule.classes[i] = scheduleB.classes[i]
            
    crossoverSchedule.check_conflict()
    crossoverSchedule.check_lunch_break()
    crossoverSchedule.check_fitness()
    return crossoverSchedule

        
def choose_crossover(pop):
    NUM_CROSSOVER_TRIALS = 3
    chosen_schedule = -1
    lowest_conflict = 1000
    for i in range(0, NUM_CROSSOVER_TRIALS):
        trial = random.randrange(0,len(pop))
        if (pop[trial].conflictNum < lowest_conflict):
            lowest_conflict = pop[i].conflictNum
            chosen_schedule = trial
    #print("Chosen index #: " + str(trial) + " with conflicts # " + str(lowest_conflict))
    return chosen_schedule

def mutate_schedule(MUTATION_RATE, schedule, subjectList):
    mutated_schedule = Schedule()
    mutated_schedule.initialize(len(schedule.classes), subjectList)
    for i in range(0, len(schedule.classes)):
        if (random.random() < MUTATION_RATE):
            schedule.classes[i] = mutated_schedule.classes[i]
            
    return schedule
    
    
    
    
def evolve(pop, NUM_ELITES, MUTATION_RATE, subjectList):
    new_generation = []
    
    #ELITISM
    for i in range(0, NUM_ELITES):
        new_generation.append(pop[i])
    
    #print("TRYING CROSSOVER")
    #CROSSOVER
    while(i < NUM_POPULATION):
        new_generation.append(crossover(pop[choose_crossover(pop)] , pop[choose_crossover(pop)], subjectList))
        i += 1
    print("EVOLVE DONE")
    
    #MUTATION
    for i in range(NUM_ELITES, len(pop)):
        mutate_schedule(MUTATION_RATE, new_generation[i], subjectList)
        
    
    #new_generation.sort(key=operator.attrgetter('conflictNum'))
    new_generation.sort(key=operator.attrgetter('fitness'), reverse=True)
    return new_generation

        
    
    
def generate_population(num_population, subjectList):
    population = []
    for i in range(0, num_population):
        newSchedule = Schedule()
        newSchedule.initialize(len(subjectList), subjectList)
        newSchedule.check_conflict()
        newSchedule.check_lunch_break()
        newSchedule.check_fitness()
        population.append(newSchedule)
        
    #population.sort(key=operator.attrgetter('conflictNum'))
    population.sort(key=operator.attrgetter('fitness'), reverse=True)
    return population

def genetic_algorithm(subjectList):
    #number of generations is = i
    i = 0
    population = generate_population(NUM_POPULATION, subjectList)
    starting_fitness = population[0].fitness
    while (i < 1000):
    #while (population[1].conflictNum > 0):
    #while (population[0].fitness < 1.5):
        print("GENERATION# " + str(i))
        population = evolve(population, NUM_ELITES, MUTATION_RATE, subjectList)
        i += 1
        for popi in population:
            print("fitness: " + str(popi.fitness) + " lunchbreakconflict: " + str(popi.lunchBreakconflict) + " numConflict: " + str(popi.conflictNum) + " breakhours: " + str(popi.longestBreak))
        print("population fitness: " + str(population[0].fitness))
        
    ending_fitness = population[0].fitness
    
    print("fitness delta: " + str(ending_fitness-starting_fitness))
    print_schedule_data(population[0])
    print("lunchconflicts: " + str(population[0].lunchBreakconflict))
    #print_schedule_data(population[1])
    
    #for pop in population:
      #  if (pop.conflictNum == 0):
        #    print_schedule_data(pop)
           # print("lunchconflicts: " + str(population[0].lunchBreakconflict))

    final_list = []
    for thing in population[0].classes:
        date_parse = []
        for time in convertTodecimal(thing._meetingTime):
            if (not time.is_integer()):
                date_parse.append(str(int(time)) + ":" + str(int(60 * (time - int(time)))))
            else:
                date_parse.append(str(int(time)) + ":00")
        
        print("-".join(date_parse))
        print(" ".join(thing._meetingDay))
        final_list.append(thing._courseName.strip() + " " + str("-".join(thing._meetingDay)) + " " + str("-".join(date_parse)))
        #print(thing._courseName + "\t\t" + str(thing._meetingTime) + "\t\t" + str(thing._meetingDay) + " rating: " + str(thing._rating))

    return final_list
    
def update_rating(teacher):
    DEFAULT_RATING = 3
    firstName = teacher.split(",")[1].strip()
    lastName = teacher.split(",")[0].strip()
    search_value = firstName.split()
    name = ""
    #if (len(search_value) > 1):
    for i in range(0, len(search_value)):
        name = name + " " + search_value[i]
        print("Searching: [" + str(name.strip()) + "] Last Name: [" + lastName + "]")
        rating = next((item["rating"]["overall"] for item in ratings if item["firstName"].upper() == name.strip() and item["lastName"].upper() == lastName), -1)
        print(rating)
        if (rating != -1 and rating != 0):
            return rating
    return DEFAULT_RATING

def filter_subject(mycsv, search_name):
    return mycsv[mycsv["name"].str.contains(search_name, na=False, case=False)]

def load_csv():
    data = pd.read_csv('crs.csv', encoding = "ISO-8859-1", engine='python')
    data.head()
    return data

# subjectList = []

# sample_input = ["Fil 40 ", "CW 10 ", "CoE 115 TJK", "CoE 115 HWX", "CWTS 2 Engg DCS", "Math 10 ", "Archaeo 2 "]
# length = len(sample_input)
# mycsv = load_csv()

# possible_subjects = []
# for input in sample_input:
#     newSubject = Subject(input)
#     possible_subjects.append(filter_subject(mycsv, input))
#     for index, row in filter_subject(mycsv, input).iterrows():
#         if (row['professor'] == "TBA" or row['professor'] == "CONCEALED"):
#             row['professor'] = "TBA, TBA2"
#         print(row['professor'])
#         newCourse = Course(row['course number'], row['name'], row['professor'], row['schedule'].split(' ')[1])
#         newCourse._meetingDay = parse_schedule(row['schedule'].split(' ')[0])
#         newSubject._courses.append(newCourse)
#     subjectList.append(newSubject)
    
    
    
# genetic_algorithm()
        



