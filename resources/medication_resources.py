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
    coding: str = "DO NOT EDIT: RxNorm Code will populate from UML API"
    text: str = "DO NOT EDIT: Name of RxNorm Code will populate from UML API"

class Reference(BaseModel):
    reference: str = "string"
    type: str = "uri"
    # identifier: Identifier
    display: str = "string"

class CodeableReference_Medication(BaseModel):
    concept: UMLCodeableConcept
    reference: Reference

class Annotation(BaseModel):
    authorString: str = "Author"
    time: str = "YYYY-M-D"
    text: str = 'string'

class Period(BaseModel):
    start: str = "YYYY-M-D"
    end: str = "YYYY-M-D"

class DoseAndRate(BaseModel):
    type: CodeableConcept
    doseQuantity: str = "Quantity(SimpleQuantity)"
    rateQuantity: str = "Quantity(SimpleQuantity)"

class Ratio(BaseModel):
    numerator: str = "Quantity"
    denominator: str = "Quantity(SimpleQuantity)"

class InitialFill(BaseModel):
    quantity: str = "Quantity"
    duration: str = "Duration"

class DispenseRequest(BaseModel):
    initialFill: InitialFill

class Substition(BaseModel):
    allowedBoolean: bool =  True
    reason: CodeableConcept

class DosageInstruction(BaseModel):
    sequence: int = 1
    text: str = "string"
    additonalInstruction: CodeableConcept
    patientInstruction: str = "string"
    timing: str = "string"
    asNeeded: bool = True
    site: CodeableConcept
    route: CodeableConcept
    method: CodeableConcept
    doseAndRate: DoseAndRate
    maxDosePerPeriod: Ratio
    maxDosePerAdministration: str = "Quantity(SimpleQuantity)"
    maxDosePerLifetime: str = "Quantity(SimpleQuantity)"

class Medication(BaseModel):
    resourceType: str = "MedicationRequest"
    identifier: Identifier
    basedOn: str = "Reference(CarePlan|ImmunizationRecommendation|MedicationRequest|ServiceRequest)"
    priorPrescription: str = 'Reference(MedicationRequest)'
    groupIdentifier: Identifier
    status: Literal['active', 'on-hold', 'ended', 'stopped', 'completed', 'cancelled', 'entered-in-error', 'draft', 'unknown'] = 'active'
    statusReason: CodeableConcept
    statusChanged: str = "YYYY-M-D"
    intent: Literal['proposal', 'plan', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'] = 'proposal'
    category: CodeableConcept
    priority: Literal['routine', 'urgent', 'asap', 'stat'] = 'routine'
    doNotPerform: bool = True
    medication: CodeableReference_Medication
    subject: str = "DO NOT EDIT: Patient ID"
    informationSource: str = 'Reference(Organization|Patient|Practitioner|PractitionerRole|RelatedPerson)'
    encounter: str = "Reference(Encounter)"
    supportingInformation: str = "Reference(Any)"
    authoredOn: str = "YYYY-M-D"
    requester: str = 'Reference(Device|Organization|Patient|Practitioner|PractitionerRole|RelatedPerson)'
    reported: bool = True
    performerType: CodeableConcept
    performer: str = 'Reference(CareTeam|DeviceDefinition|HealthcareService|Organization|Patient|Practitioner|PractitionerRole|RelatedPerson)'
    device: str = "CodableReferecne(DeviceDefinition)"
    recorder: str = "Reference(Practitioner|PractitionerRole)"
    reason: str = "CodeableReference(Condition|Observation)"
    courseOfTherapyType: CodeableConcept
    insurance: str = "Reference(ClaimResponse|Coverage)"
    note: Annotation
    renderDosageInstruction: str = "markdown"
    effectiveDosePeriod: Period
    dosageInstruction: DosageInstruction
    dispenseRequest: DispenseRequest
    dispenseInterval: str = "Duration"
    validityPeriod: Period
    numberOfRepeatsAllowed: int = 1
    quantity: str = "Quantity(SimpleQuantity)"
    expectedSupplyDuration: str = "Duration"
    dispenser: str = "Reference(Organization)"
    dispenserInstruction: Annotation
    doseAdministrationAid: CodeableConcept
    substition: Substition
    eventHistory: str = "Reference(Provenance)"

