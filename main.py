from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from pydantic.typing import Literal
from uuid import UUID, uuid4
from datetime import date
import json
import os
import random


app = FastAPI()

class HumanName (BaseModel):
    text:str = Field(description = "Input the first and last name of the patient")

    # @validator('text')
    # def name_must_contain_space(cls, v):
    #     if ' ' not in v:
    #         raise ValueError('must contain first and last name with a space')
    #     return v.title()

class ContactPoint (BaseModel):
    system: str = 'phone'
    value: str

    # @validator('value')
    # def full_phone_number(cls, v):
    #     if len(v) < 10:
    #         raise ValueError('not a full phone number')
    #     return v.title()

class Address (BaseModel):
    line: str
    city: str
    district: str
    state: str
    postalCode: str
    country: str

    # @validator('line')
    # def line_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('not a full address')
    #     return v.title()
    
    # @validator('city',allow_reuse=True)
    # def city_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('not a full address')
    #     return v.title()
    
    # @validator('district',allow_reuse=True)
    # def district_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('not a full address')
    #     return v.title()

    # @validator('state',allow_reuse=True)
    # def state_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('not a full address')
    #     return v.title()

    # @validator('postalCode',allow_reuse=True)
    # def postalCode_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('not a full address')
    #     return v.title()
    
    # @validator('country',allow_reuse=True)
    # def country_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('not a full address')
    #     return v.title()

class Contact(BaseModel):
    relationship:str
    name: HumanName
    telecom:ContactPoint
    address: Address
    gender: Literal['string','male', 'female','other', 'unknown']


    # @validator('gender',allow_reuse=True)
    # def gender_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('cannot leave string as gender')
    #     return v.title()


   
    


class Patient(BaseModel):
    resourceType: str = "Patient"
    active: bool = True
    id: int
    name: HumanName
    telecom: ContactPoint
    gender: Literal['string','male', 'female','other', 'unknown']
    birthdate: Union[date,str] = 'YYYY-MM-DD'
    deceasedBoolean: bool = False
    address: Address
    contact: Contact


    # @validator('gender',allow_reuse=True)
    # def gender_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('cannot leave string as gender')
    #     return v.title()





@app.post("/createPatient")
def post_info(patient: Patient):

    patient_db = {}

    #if file is empty
    if os.stat('patient.json').st_size == 0:
        with open("patient.json", "w") as outfile:

            #create a dict storing the response body as a key value pair
            patient_db[str(1)] = patient.dict()

            #write to file, prettifying the json
            outfile.write(json.dumps(patient_db, indent=4))
    
    else:
        with open("patient.json", "r+") as outfile:
            
            #read json from file as dict
            db = json.load(outfile)

            #find the max key in the dict and then increment from that number.
            #this will be the key for the new patient
            key = max(db.keys())
            key = int(key)
            key += 1

            #create a new key-value pair in the existing dict
            db[str(key)] = patient.dict()
            print(db)

            # #delete old dict
            # outfile.truncate(0)
            outfile.seek(0) 
            outfile.truncate()

            #write to file, prettifying the json
            outfile.write(json.dumps(db, indent=4))
            

        
@app.put("/updateAnyPatient/{patient_id}", response_model=Patient)
async def update_patient_info(patient_id: str, patient:Patient):
    with open("patient.json", "r+") as outfile:
            #read json from file as dict
            update_patient_encoded = jsonable_encoder(patient)

            db = json.load(outfile)

            db[patient_id] = update_patient_encoded

            outfile.seek(0) 
            outfile.truncate()

            #write to file, prettifying the json
            outfile.write(json.dumps(db, indent=4))
            return update_patient_encoded

 
@app.get("/retrievePatient/{patient_id}", response_model=Patient)
async def read_item(patient_id: str):
    with open("patient.json", "r+") as outfile:

        db = json.load(outfile)
        return db[patient_id]


# @app.get("/readFromFile")
# def read_info():
#     f = open('test.json')
#     data = json.load(f) 
#     return data
