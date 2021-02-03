# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 00:39:24 2021

@author: Philippe
"""
from typing import List

class Course:
    def __init__(self, id, courseName, teacher, meetingTime):
        self._id = id
        self._courseName = courseName
        self._teacher = teacher
        self._meetingTime = meetingTime
        

Subject = List[Course]
    
    