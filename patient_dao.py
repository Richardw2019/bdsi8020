import json
import os
from fastapi.encoders import jsonable_encoder

class PatientDao:
    def _init_(self):
        pass

    def create_patient(self, patient):
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
    

    def update_patient_info(self, patient_id, patient):
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
    

    def get_patient_info(self, patient_id):
        #open file
        with open("patient.json", "r+") as outfile:

            #read json from file as dict
            db = json.load(outfile)

            #return key value pair (or patient) with the id the user asked for
            return db[patient_id]

            
