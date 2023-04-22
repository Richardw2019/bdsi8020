import json
import os
from fastapi.encoders import jsonable_encoder
import requests

from services.patient_service import PatientService
from services.condition_service import ConditonService


patient_service = PatientService()
condition_service = ConditonService()

class EncounterDao:

    def _init_(self):
        pass

    def create_encounter(self, encounter):
        encounter_db = {}
        
        #if file is empty
        if os.stat('encounter.json').st_size == 0:
            with open("encounter.json", "w") as outfile:

                #create a dict storing the response body as a key value pair
                encounter_db[str(1)] = encounter.dict()

                #write to file, prettifying the json
                outfile.write(json.dumps(encounter_db, indent=4))

                return encounter
            
        else:
            with open("encounter.json", "r+") as outfile:
                
                #read json from file as dict
                db = json.load(outfile)

                #find the max key in the dict and then increment from that number.
                #this will be the key for the new patient
                key = max(db.keys())
                key = int(key)
                key += 1

                #create a new key-value pair in the existing dict
                db[str(key)] = encounter.dict()

                # #delete old dict
                # outfile.truncate(0)
                outfile.seek(0) 
                outfile.truncate()

                #write to file, prettifying the json
                outfile.write(json.dumps(db, indent=4))

                return encounter
        
    def get_encounter(self, encounter_id):
        #open file
        with open("encounter.json", "r+") as outfile:

            #read json from file as dict
            db = json.load(outfile)

            #return key value pair (or encounter) with the id the user asked for

            if encounter_id not in db: 
                return "encounter does not exist"
            else: 
                return db[encounter_id]
            
    
    def update_encounter(self, encounter_id, patient_id, condition_id):
        
        #check if encounter exists
        encounter = self.get_encounter(encounter_id)

        if encounter == "encounter does not exist":
            return "encounter does not exist"
        
        if encounter['subject'] != "Patient ID":
            return "specifc encounter already has patient linked to it"
        
        #Check to see if patient exists
        else:
            patient = patient_service.get_patient_info(patient_id)

            if patient == "patient does not exist":
                return "patient does not exist"

            
            #check to see if condition_id and patient_id exists
            with open("condition.json", "r+") as condition_outfile:

                #read condition json from file as a dict
                condition_db = json.load(condition_outfile)

                if condition_id not in condition_db:
                    return "condition does not exist"
                
                elif condition_db[condition_id]['subject'] != patient_id:
                    return "condition does not have patient attached to it"
                
                else:

                    with open("encounter.json", "r+") as outfile:

                        #read json from file as dict
                        encounter_db = json.load(outfile)

                        #link encounter to patient
                        encounter_db[encounter_id]['subject'] = patient_id

                        #link encounter to condition
                        encounter_db[encounter_id]['diagnosis']['condition'] = condition_db[condition_id]['code']['text']
                
                        #update json
                        outfile.seek(0)
                        outfile.truncate()
                        outfile.write(json.dumps(encounter_db, indent=4))

                        #return the updated encounter
                        return encounter_db[encounter_id]

            
            
            
            
            #check to see if patient has conditions
            # conditions = condition_service.get_conditions(patient_id)

            # if conditions == "patient does not have any conditions":
            #     return "patient does not have any conditions"
            
            # else:
            #     return conditions




            # #else open and see if patient id exists
            # else: 
            #     with open("patient.json", "r+") as outfile:

            #     #read json from file as dict
            #     db = json.load(outfile)

            #     #return key value pair (or patient) with the id the user asked for
            #     return db[patient_id]