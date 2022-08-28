import json
from django.http import HttpResponse
from django.shortcuts import render
from courses.models import CreateCourses, ctrainer
from .connection import Connection


def register(request):
        if request.method == 'POST':
            try:
                data = request.POST.dict()
                employee = CreateCourses()
                employee.set_data(data)
                employee.save_to_db()

            except BaseException as error:
                print('An exception occurred: {}'.format(error))
                return HttpResponse(json.dumps({"err": "something wrong"}))
            return HttpResponse(json.dumps({"key": "okay"}))

def show(request):
    if request.method == "GET":
        try:
            connection = Connection()
            collection = connection.set_collection('Courses')
            courses = []
            for x in collection.find():
                trainer = CreateCourses()
                trainer.set_data(x)
                trainer = trainer.convert_to_json()
                courses.append(trainer)
            return HttpResponse(json.dumps({"key": courses})) 
        except BaseException as error:
                print('An exception occurred: {}'.format(error))
                return HttpResponse(json.dumps({"err": "something wrong"}))
def showt(request):
    if request.method == "POST":
            data = request.POST.dict()
            employee = ctrainer()
            employee.set_data(data)
            employee.savetodb()

def showtrainer(request):
    if request.method == "POST":
            data = request.POST.dict()
            connection = Connection()
            collection = connection.set_collection('Courses')
            courses = []
            employee = collection.find({"tid": data['tid']})
            for x in employee:
                trainer = CreateCourses()
                trainer.set_data(x)
                trainer = trainer.convert_to_json()
                courses.append(trainer)
            return HttpResponse(json.dumps({"key": courses})) 