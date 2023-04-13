from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from pydantic.typing import Literal
from datetime import date
import json
import os
from services.patient_service import PatientService
from services.condition_service import ConditonService
from services.observation_service import ObservationService
from services.medication_service import MedciationService
from resources.patient_resources import Patient
from resources.conditon_resources import Condition
from resources.observation_resources import Observation
from resources.medication_resources import Medication


patient_service = PatientService()
condition_service = ConditonService()
observation_service = ObservationService()
medication_service = MedciationService()

app = FastAPI()

#create a patient object
@app.post("/createPatient")
async def post_info(patient: Patient):
    return patient_service.create_patient(patient)

#update the information of any patient
@app.put("/updateAnyPatient/{patient_id}", response_model=Patient)
async def update_patient_info(patient_id: str, patient:Patient):
    return patient_service.update_patient_info(patient_id, patient)

#retrieve the information of a specific patient
@app.get("/retrievePatientInfo/{patient_id}", response_model=Patient)
async def read_item(patient_id: str):
    return patient_service.get_patient_info(patient_id)





#create a condition object, this will using search params for a separate API
#call to UML API to retrieve the ICD10CM code and name of code
#user will see the request body that can be edited, but the code attribute 
#is empty. ASSUME THAT IT IS FILLED UP AS IT WILL BE SET TO THE UML API
#RESULTS ONCE SAVED IN THE CONDITIONS JSON FILE
@app.post("/createCondition/{search_params}", response_model=Condition)
async def create_condition(search_params: str, condition: Condition):  
    return condition_service.create_condition(search_params, condition)

#takes a patient id and conditon id and assigns a patient to that condition specified 
#by its condition id
@app.put("/assignConditionToPatient/{patient_id}/{condition_id}")
async def assign_condition(patient_id: str, condition_id: str):  
    return condition_service.assign_condition(patient_id, condition_id)

#takes in a patient id and returns a list of all condtion objects that are linked to 
#that patient 
@app.get("/getPatientCondtions/{patient_id}")
async def get_conditions(patient_id: str):
    return condition_service.get_conditions(patient_id)




#create observation using loinc code
@app.post("/createObservation/{search_params}", response_model=Observation)
async def create_observation(search_params: str, observation: Observation):
    return observation_service.create_observation(search_params, observation)

#assign the created observation to a patient
@app.put("/assignObservationToPatient/{patient_id}/{observation_id}")
async def assign_observation(patient_id: str, observation_id: str):  
    return observation_service.assign_observation(patient_id, observation_id)

#retrieve all observations tied to a patient id
@app.get("/getPatientObservations/{patient_id}")
async def get_observations(patient_id: str):
    return observation_service.get_observations(patient_id)



#create a medication request using RxNORM 
#Used medication ciprofloxacin as test case
#acetaminophen
@app.post("/createMedicationRequest/{search_params}", response_model=Medication)
async def create_medication(search_params: str, medication: Medication):
    return medication_service.create_medication(search_params, medication)

#assign created medication request to a patient
@app.put("/assignMedicationToPatient/{patient_id}/{medication_id}")
async def assign_medication(patient_id: str, medication_id: str):  
    return medication_service.assign_medication(patient_id, medication_id)

#retreive all medication tied to a patient using medication name
@app.get("/getPatientMedications/{patient_id}/{medication_name}")
async def get_medications(patient_id: str, medication_name: str):
    return medication_service.get_medications(patient_id, medication_name)
