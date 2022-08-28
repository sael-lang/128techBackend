from optparse import Values
from django.shortcuts import render, redirect
# from .serializer import EmployeeSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from .models.employee import PTCLEmployee
from .models.admin import PTCLAdmin
from .models.trainer import PTCLTrainer
# from .forms import EmployeeForm, EmployeeLoginForm
import re
import json
from bson.json_util import dumps
import pymongo
from django.conf import settings

### TODO Cleanup & Secure this part

###

# class Employee(viewsets.ModelViewSet):
class Employee():
    # queryset = EmployeeModel.objects.all()
    # serializer_class = EmployeeSerializer

    def login(request):
        if request.method == 'POST':
            data = request.POST.dict()
            if is_external(data['EmpId']):
                pass
            else:
                collection = set_collection('InternalEmployees')
                existing = collection.find_one({"EmpId": data['EmpId']})
                if existing == None:
                    return HttpResponse(json.dumps({"key": "n"}))
                else:
                    if existing['Post'] == 'Employee':
                        collection = set_collection('Employees')
                        employee = collection.find_one({"EmpId": existing['EmpId']})
                        if data['Password'] == employee['Password']:
                           if employee['status'] == "false":
                            return HttpResponse(json.dumps({"key":"w"}))
                           else:
                            admin = PTCLEmployee()
                            admin.set_data(employee)
                            admin = admin.convert_to_json()                            
                            return HttpResponse(json.dumps({"key": "e", "data": admin}))
                        return HttpResponse(json.dumps({"key": "p"}))
                    elif existing['Post'] == 'Admin':
                        collection = set_collection('Admins')
                        employee = collection.find_one({"EmpId": existing['EmpId']})
                        if data['Password'] == employee['Password']:
                            admin = PTCLAdmin()
                            admin.set_data(employee)
                            admin = admin.convert_to_json()                            
                            return HttpResponse(json.dumps({"key": "a", "data": admin}))
                        return HttpResponse(json.dumps({"key": "p"}))
                    elif existing['Post'] == 'Trainer':
                        collection = set_collection('Trainers')
                        employee = collection.find_one({"EmpId": existing['EmpId']})
                        if data['Password'] == employee['Password']:
                            trainer=PTCLTrainer()
                            trainer.set_data(employee)
                            trainer=trainer.convert_to_json()
                            return HttpResponse(json.dumps({"key": "t", "data": trainer}))
                        return HttpResponse(json.dumps({"key": "p"}))
                    else:
                        return HttpResponse(json.dumps({"key": "invalid request"}))
            pass

            
    def getadmins(request):
        if request.method == "GET":
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["LMS"]
            mycol = mydb["Admins"]
            x = mycol.find({},{ "_id": 0, "fname": 1, "lname": 1,"EmpId":1 })
            admins = []
            for ad in x:
                admins.append(f"{ad['EmpId']} {ad['fname']}")
            # data = {"key": admins}
            return HttpResponse(json.dumps(admins))

    def get_rights(request):
        if request.method=="POST":
            existing=request.POST.dict()
            collection = set_collection('Admins')
            employee = collection.find_one({"EmpId": existing['EmpId']},{"_id": 0, "Rights": 1})       
            if not employee == None:
                rights= "" + employee['Rights']
                data = {"key": rights}
                return HttpResponse(json.dumps(data))

    def update_rights(request):
        if request.method=="POST":
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["LMS"]
            mycol = mydb["Admins"]
            rights=request.POST.dict()
            updated= "" + rights['EmpId']
            collection = set_collection('Admins')
            empId=updated.split()[0]
            data = {"Rights": updated.split()[1]}
            employee = collection.find_one({"EmpId": empId},{"_id": 0, "Rights": 1}) 
            values = { "$set": data }   
            mycol.update_one(employee, values)
            return HttpResponse(json.dumps({"key": "okay"}))


    def register(request):
        if request.method == 'POST':
            try:
                data = request.POST.dict()
                if data['Post'] == None:
                    return HttpResponse(json.dumps({"err": "invalid request"}))
                elif data['Post'] == 'Employee':
                    collection = set_collection('InternalEmployees')
                    existing = collection.find_one({"EmpId": data['EmpId']})
                    if existing==None:
                        employee = PTCLEmployee()
                        employee.set_data(data)
                        employee.save_to_db(data)
                    else:
                        return HttpResponse(json.dumps({"key": "ae"}))
                elif data['Post'] == 'Admin':
                    collection = set_collection('InternalEmployees')
                    existing = collection.find_one({"EmpId": data['EmpId']})
                    if existing==None:
                        employee = PTCLAdmin()
                        employee.set_data(data)
                        employee.save_to_db(data)
                    else:
                        return HttpResponse(json.dumps({"key": "ae"}))
                elif data['Post'] == 'Trainer':
                    collection = set_collection('InternalEmployees')
                    existing = collection.find_one({"EmpId": data['EmpId']})
                    if existing==None:
                        employee = PTCLTrainer()
                        employee.set_data(data)
                        employee.save_to_db(data)
                    else:
                        return HttpResponse(json.dumps({"key": "ae"}))
                else:
                    return HttpResponse(json.dumps({"err": "invalid request"}))
            except BaseException as error:
                print('An exception occurred: {}'.format(error))
                return HttpResponse(json.dumps({"err": "something wrong"}))
            return HttpResponse(json.dumps({"key": "okay"}))
        elif request.method == "GET":
            return HttpResponse('404')

def set_collection(table_name):
    connect_string = "mongodb://localhost:27017"
    mongo_client = pymongo.MongoClient(connect_string)
    dbname = mongo_client['LMS']
    collection_name = dbname[table_name]
    return collection_name


def is_external(employee_id):
    nic_regex = '^[0-9+]{5}-[0-9+]{7}-[0-9]{1}$'
    if re.match(nic_regex, employee_id):
        return True
    return False

def changepass(request):
    if request.method == 'POST':
        data = request.POST.dict()
        collection = set_collection('InternalEmployees')
        employee = collection.find_one({"EmpId": data['EmpId']},{"_id": 0, "password": 1})
        if data.split[1] == employee['Password']:
            if employee['Post'] == 'Employee':
                        collection = set_collection('Employees')
                        data=data.split[2]
                        values = { "$set": data } 
                        collection.update_one(employee, values)
