from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from pydantic.typing import Literal
from datetime import date
import json
import os

class Identifier (BaseModel):
    use: str = "NULL"
    type: str = "NULL"
    system: str = "NULL"
    value: str = '1'
    period: str = "NULL"

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
    gender: Literal['string','male', 'female','other', 'unknown', 'Male', "Female", "Other", "Unknown"]


    # @validator('gender',allow_reuse=True)
    # def contact_gender_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('cannot leave string as gender')
    #     return v.title()

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


    # @validator('gender')
    # def patient_gender_check(cls, v):
    #     if 'string' in v:
    #         raise ValueError('cannot leave string as gender')
    #     return v.title()