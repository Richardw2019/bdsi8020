from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from pydantic.typing import Literal
from datetime import date
import json
import os
from patient_service import PatientService
from resources import Patient



patient_service = PatientService()

app = FastAPI()

@app.post("/createPatient")
async def post_info(patient: Patient):
    return patient_service.create_patient(patient)


@app.put("/updateAnyPatient/{patient_id}", response_model=Patient)
async def update_patient_info(patient_id: str, patient:Patient):
    return patient_service.update_patient_info(patient_id, patient)


@app.get("/retrievePatientInfo/{patient_id}", response_model=Patient)
async def read_item(patient_id: str):
    return patient_service.get_patient_info(patient_id)

