from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from pydantic.typing import Literal
from datetime import date
import json
import os

#any attributes with "NULL" will not need to be changed

app = FastAPI()

class Identifier (BaseModel):
    use: str = "NULL"
    type: str = "NULL"
    system: str = "NULL"
    value: str = '1'
    period: str = "NULL"


class HumanName (BaseModel):
    text:str = Field(description = "Input the first and last name of the patient")

    @validator('text')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain first and last name with a space')
        return v.title()

class ContactPoint (BaseModel):
    system: str = 'phone'
    value: str

    @validator('value')
    def full_phone_number(cls, v):
        if len(v) < 10:
            raise ValueError('not a full phone number')
        return v.title()

class Address (BaseModel):
    line: str
    city: str
    district: str
    state: str
    postalCode: str
    country: str

    @validator('line')
    def line_check(cls, v):
        if 'string' in v:
            raise ValueError('not a full address')
        return v.title()
    
    @validator('city',allow_reuse=True)
    def city_check(cls, v):
        if 'string' in v:
            raise ValueError('not a full address')
        return v.title()
    
    @validator('district',allow_reuse=True)
    def district_check(cls, v):
        if 'string' in v:
            raise ValueError('not a full address')
        return v.title()

    @validator('state',allow_reuse=True)
    def state_check(cls, v):
        if 'string' in v:
            raise ValueError('not a full address')
        return v.title()

    @validator('postalCode',allow_reuse=True)
    def postalCode_check(cls, v):
        if 'string' in v:
            raise ValueError('not a full address')
        return v.title()
    
    @validator('country',allow_reuse=True)
    def country_check(cls, v):
        if 'string' in v:
            raise ValueError('not a full address')
        return v.title()

class Contact(BaseModel):
    relationship:str
    name: HumanName
    telecom:ContactPoint
    address: Address
    gender: Literal['string','male', 'female','other', 'unknown', 'Male', "Female", "Other", "Unknown"]


    @validator('gender',allow_reuse=True)
    def contact_gender_check(cls, v):
        if 'string' in v:
            raise ValueError('cannot leave string as gender')
        return v.title()

class Communication(BaseModel):
    language: str = "NULL"
    preferred: bool = True
   

class Patient(BaseModel):
    resourceType: str = "Patient"
    active: bool = True
    identifier: Identifier
    name: HumanName
    telecom: ContactPoint
    gender: Literal['string','male', 'female','other', 'unknown', 'Male', "Female", "Other", "Unknown"]
    birthDate: str = 'YYYY-MM-DD'
    deceasedBoolean: bool = False
    address: Address
    multipleBirthBoolean: bool = False
    contact: Contact
    communication: Communication

    generalPractitioner: str = "Default General Practitioner"
    managingOrganization: str = "Default Managing Organization"


    @validator('gender')
    def patient_gender_check(cls, v):
        if 'string' in v:
            raise ValueError('cannot leave string as gender')
        return v.title()





@app.post("/createPatient")
async def post_info(patient: Patient):

    patient_db = {}

    #if file is empty
    if os.stat('patient.json').st_size == 0:
        with open("patient.json", "w") as outfile:

            #create a dict storing the response body as a key value pair
            patient_db[str(1)] = patient.dict()

            #write to file, prettifying the json
            outfile.write(json.dumps(patient_db, indent=4))

            return patient
    
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

            # #delete old dict
            # outfile.truncate(0)
            outfile.seek(0) 
            outfile.truncate()

            #write to file, prettifying the json
            outfile.write(json.dumps(db, indent=4))

            return patient

            
        
@app.put("/updateAnyPatient/{patient_id}", response_model=Patient)
async def update_patient_info(patient_id: str, patient:Patient):
    with open("patient.json", "r+") as outfile:

        #grab updated patient body from the put request
        update_patient_encoded = jsonable_encoder(patient)

        #read json from file as dict
        db = json.load(outfile)

        #check if patient_id is in db and then add the updated patient body 
        if patient_id in db:
            db[patient_id] = update_patient_encoded

            #delete everything from file
            outfile.seek(0) 
            outfile.truncate()

            #write to file, prettifying the json
            outfile.write(json.dumps(db, indent=4))
            return update_patient_encoded
        
        #return patient_id if it doesn't exist
        else:
            return {"patient_id": patient_id}

          
                
@app.get("/retrievePatientInfo/{patient_id}", response_model=Patient)
async def read_item(patient_id: str):
    #open file
    with open("patient.json", "r+") as outfile:

        #read json from file as dict
        db = json.load(outfile)

        #return key value pair (or patient) with the id the user asked for
        return db[patient_id]
