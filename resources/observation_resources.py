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

class UMLCodeableConcept(BaseModel):
    coding: str = "DO NOT EDIT: LOINC Code will populate from UML API"
    text: str = "DO NOT EDIT: Name of LOINC Code will populate from UML API"

class Annotation(BaseModel):
    authorString: str = "Author"
    time: str = "YYYY-M-D"
    text: str = 'string'

class ReferenceRange(BaseModel):
    low: str = 'Quantity(SimpleQuantity)'
    high: str = 'Quantity(SimpleQuantity)'
    type: CodeableConcept
    appliesTo: CodeableConcept
    age: str = 'Range'
    text: str = 'string'

class Component(BaseModel):
    code: UMLCodeableConcept
    valueDateTime: str = 'YYYY-M-D'

class Observation(BaseModel):

    resourceType: str = "Observation"
    identifier: Identifier
    basedOn: str = "Reference(CarePlan|DeviceRequest|ImmunizationRecommendation|MedicationRequest|NutritionOrder|ServiceRequest)"
    partOf: str = 'Reference(ImagingStudy|Immunization|MedicationAdministration|MedicationDispense|MedicationStatement|Procedure)'
    status: Literal['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown'] = 'registered'
    category: CodeableConcept
    code: UMLCodeableConcept
    subject: str = "DO NOT EDIT: Patient ID"
    focus: str = "Reference(Any)"
    encounter: str = "Reference(Encounter)"
    effectiveDateTime: str = "YYYY-M-D"
    performer: str = 'Reference(CareTeam|Organization|Patient|Practitioner|PractitionerRole|RelatedPerson)'
    valueDateTime: str = 'YYYY-M-D'
    dateAbsentReason: CodeableConcept
    interpretation: CodeableConcept
    note: Annotation
    bodySite: CodeableConcept
    method: CodeableConcept
    specimen: str = 'Reference(Specimen)'
    device: str = 'Reference(Device|DeviceMetric)'
    referenceRange: ReferenceRange
    hasMember: str = 'Reference(MolecularSequence|Observation|QuestionnaireResponse)'
    derivedFrom: str = 'Reference(DocumentReference|ImagingStudy|Media|MolecularSequence|Observation|QuestionnaireResponse)'
    component: Component