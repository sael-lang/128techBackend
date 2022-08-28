import json
from pickle import PERSID
from django.db import models

from courses.connection import Connection

# Create your models here.
class CreateCourses():
    def __init__(self):
        self.cname = ""
        self.cid = ""
        self.cdescription = ""
        self.cduration = ""
        self.coutcome = ""
        self.coutline = ""
        self.cimg=""
        self.tid = ""
        self.cdate = ""
    
    def set_data(self, employee):
        self.cname = employee['cname']
        self.cid = employee['cid']
        self.cdescription = employee['cdescription']
        self.cduration = employee['cduration']
        self.coutcome = employee['coutcome']
        self.coutline = employee['coutline']
        self.cimg=employee["cimg"]
        self.tid = employee['tid']
        self.cdate = employee['cdate']

    def save_to_db(self,employee):
        connection = Connection()
        collection = connection.set_collection('Courses')
        collection.insert_one(self.__dict__)

    def convert_to_json(self):
        return json.dumps(self.__dict__)

class ctrainer(CreateCourses):
    def __init__(self):
        CreateCourses.__init__(self)
        super().__init__()
        self.eid=""
    def set(self,employee):
        self.cid=employee["cid"]
        self.eid=employee["eid"]
    def savetodb(self):
        connection = Connection()
        collection = connection.set_collection('trainer_course')
        collection.insert_one(self.__dict__)