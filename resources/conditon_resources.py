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

class UMLCodeableConcept(BaseModel):
    coding: str = "DO NOT EDIT: ICD10CM Code will populate from UML API"
    text: str = "DO NOT EDIT: Name of ICD10CM Code will populate from UML API"

class CodeableConcept(BaseModel):
    coding: str = "string"
    text: str = "string"

class Stage(BaseModel):
    summary: CodeableConcept
    assessment: str = 'Reference(ClinicalImpression|DiagnosticReport|Observation)'
    type: str = CodeableConcept

class Evidence(BaseModel):
    code: str = CodeableConcept
    detail: str = "Reference(Any)"

class Note(BaseModel):
    authorString: str = "Author"
    time: str = "YYYY-M-D"
    text: str = 'string'


class Condition(BaseModel):

    resourceType: str = "Condition"
    identifier: Identifier
    clinicalStatus: CodeableConcept
    verificationStatus: CodeableConcept
    category: CodeableConcept
    severity: CodeableConcept
    code: UMLCodeableConcept
    bodySite: CodeableConcept
    subject: str = "DO NOT EDIT: Patient ID"
    encounter: str = "Reference (Encounter)"
    onsetDateTime: str = 'YYYY-M-D'
    abatementDateTime: str = 'YYYY-M-D'
    recordedDate: str = 'YYYY-M-D'
    recorder: str = 'Reference (Patient|Practitioner|PractitionerRole|RelatedPerson)'
    asserter: str = 'Reference (Patient|Practitioner|PractitionerRole|RelatedPerson)'
    stage: Stage
    evidence: Evidence
    note: Note