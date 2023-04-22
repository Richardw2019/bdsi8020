from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from pydantic.typing import Literal
from datetime import date
import json
import os

class Identifier(BaseModel):
    use: str = "string"
    type: str = "string"
    system: str = "string"
    value: str = '1'
    period: str = "string"
    assigner: str = 'Reference(Organization)'

class CodeableConcept(BaseModel):
    coding: str = "string"
    text: str = "string"

class Period(BaseModel):
    start: str = "YYYY-M-D"
    end: str = "YYYY-M-D"

class Participant(BaseModel):
    type: CodeableConcept
    period: Period
    actor: str = "Reference(Device|Group|HealthcareService|Patient|Practitioner|PractitionerRole|RelatedPerson)"

class Coding(BaseModel):
    system: str = "string"
    version: str = "string"
    code: str = "string"
    display: str = "string"
    userSelected: bool = True

class VirtualService(BaseModel):
    channelType: Coding
    addressUrl: str = "address"
    additionalInfo: str = "string"
    maxParticipants: int = 1
    sessionKey: str = "string"

class Reason(BaseModel):
    use: CodeableConcept
    value: str = "CodeableReference(Condition|DiagnosticReport|ImmunizationRecommendation|Observation|Procedure)"

class Diagnosis(BaseModel):
    condition: str = "Condition Reference"
    use: CodeableConcept

class Admission(BaseModel):
    preAdmissionIdentifier: Identifier
    origin: str = "Reference(Location|Organization)"
    admitSource: CodeableConcept
    reAdmission: CodeableConcept
    destination: str = "Reference(Location|Organization)"
    dischargeDisposition: CodeableConcept

class Location(BaseModel):
    location: str = "Reference(Location)"
    status: str = "string"
    form: CodeableConcept
    period: Period

#patient, diagnosis, labs, medication

class Encounter(BaseModel):
    resourceType: str = "Encounter"
    identifier: Identifier
    status: Literal['planned', 'in-progress', 'on-hold', 'discharged', 'completed', 'cancelled', 'discontinued', 'entered-in-error', 'unknown'] = 'completed'
    classs: CodeableConcept
    priority: CodeableConcept
    type: CodeableConcept
    serviceType: str = "Codeable Reference(HealthcareService)"
    subject: str = 'Patient ID'
    subjectStatus: CodeableConcept
    episodeOfCare: str = "Reference(EpisodeOfCare)"
    basedOn: str = "Reference(CarePlan|DeviceRequest|MedicationRequest|ServiceRequest)"
    careTeam: str = "Reference(CareTeam)"
    partOf: str = "Reference(Encounter)"
    serviceProvider: str = "Reference(Organization)"
    participant: Participant
    appointment: str = "Reference(Appointment)"
    virtualService: VirtualService
    actualPeriod: Period
    plannedStartDate: str = "YYYY-M-D"
    plannedEndDate: str = "YYYY-M-D"
    length: str = "Duration"
    reason: Reason
    diagnosis: Diagnosis
    account: str = "Reference(Account)"
    dietPreference: CodeableConcept
    specialArrangement: CodeableConcept
    specialCourtsey: CodeableConcept
    admission: Admission
    location: Location

