from ..connection import Connection
import re
import json

# Create your models here.
class PTCLEmployee():
    def __init__(self):
        self.fname = ""
        self.lname = ""
        self.lmEmpId = ""
        self.EmpId = ""
        self.Functions = ""
        self.Designation = ""
        self.Region = ""
        self.Email = ""
        self.Password = ""
        self.Contact = ""
        self.status = ""
        self.img = ""
        self.Cnic = ""
    
    def set_data(self, employee):
        self.fname = employee['fname']
        self.lname = employee['lname']
        self.lmEmpId = employee['lmEmpId']
        self.EmpId = employee['EmpId']
        self.Functions = employee['Functions']
        self.Designation = employee['Designation']
        self.Region = employee['Region']
        self.Email = employee['Email']
        self.Password = employee['Password']
        self.Contact = employee['Contact']
        self.status = employee['status']
        self.img = employee['img']
        self.Cnic = employee['Cnic']
    
    def save_to_db(self, employee):
        if(not self.is_external(self.EmpId)):
            self.insert_to_internal(employee)
        connection = Connection()
        collection = connection.set_collection(collection_name='Employees')
        collection.insert_one(self.__dict__)
    
    def is_external(self, employee_id):
        nic_regex = '^[0-9+]{5}-[0-9+]{7}-[0-9]{1}$'
        if re.match(nic_regex, employee_id):
            return True
        return False

    def insert_to_internal(self, employee):
        connection = Connection()
        collection = connection.set_collection('InternalEmployees')
        collection.insert_one(
            {
                "EmpId": employee['EmpId'],
                "Post": employee['Post']
            }
        )
    def convert_to_json(self):
        return json.dumps(self.__dict__)