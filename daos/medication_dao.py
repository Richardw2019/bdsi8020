import json
import os
from fastapi.encoders import jsonable_encoder
import requests

class MedicationDao:

    def _init_(self):
        pass

    def create_medication(self, search_params, medication):
        
        API_KEY = 'f2577616-a7e0-45e4-a76c-c550a96d914a'
        BASE_URL = 'https://uts-ws.nlm.nih.gov/rest'
        search_url = f'/search/current?string={search_params}&searchType=exact&returnIdType=code&sabs=RXNORM&apiKey={API_KEY}'
        api_call = BASE_URL + search_url
        
        uml_json = requests.get(api_call).json()

        #convert observation object dict
        medication_dict = medication.dict()

        #remove any results that don't have a LOINC code
        for x in uml_json['result']['results']:
            if 'MTHU' in x['ui']:
                uml_json['result']['results'].remove(x)

        medication_dict['medication']['concept']['coding'] = uml_json['result']['results'][0]['ui']
        medication_dict['medication']['concept']['text'] = uml_json['result']['results'][0]['name']

        medication_db = {}

        #if file is empty
        if os.stat('medication.json').st_size == 0:
            with open("medication.json", "w") as outfile:

                #create a dict storing the response body as a key value pair
                medication_db[str(1)] = medication_dict

                #write to file, prettifying the json
                outfile.write(json.dumps(medication_db, indent=4))

                return medication_dict
        
        else:
            with open("medication.json", "r+") as outfile:
                
                #read json from file as dict
                db = json.load(outfile)

                #find the max key in the dict and then increment from that number.
                #this will be the key for the new patient
                key = max(db.keys())
                key = int(key)
                key += 1

                #create a new key-value pair in the existing dict
                db[str(key)] = medication_dict

                # #delete old dict
                # outfile.truncate(0)
                outfile.seek(0) 
                outfile.truncate()

                #write to file, prettifying the json
                outfile.write(json.dumps(db, indent=4))

                return medication_dict
            

    def assign_medication(self, patient_id, medication_id):

        #open patient json
        with open("patient.json", "r+") as patient_outfile:

            #read json from file as dict
            patient_db = json.load(patient_outfile)

            #check if patient exists in dict
            if patient_id not in patient_db: 
                return "patient does not exist"
            
        #open medication json
        with open("medication.json", "r+") as medication_outfile:

            #read medication json from file as a dict
            medication_db = json.load(medication_outfile)

            #check if medication exists in dict
            if medication_id not in medication_db:
                return "medication doesn't exist, create medication"
            
            else: 
                #check if medication has been assigned to a patient
                if medication_db[medication_id]['subject'] != 'DO NOT EDIT: Patient ID':
                    return "Existing medication already has a patient assigned to it, create a new medication"

                #if all checks are ignored, set the subject of the specified medication to the patient id
                else:
                    medication_db[medication_id]['subject'] = patient_id


                    #clear the medication json and write to it with the updated json
                    medication_outfile.seek(0)
                    medication_outfile.truncate()
                    medication_outfile.write(json.dumps(medication_db, indent=4))

                    return medication_db[medication_id]


    def get_medications(self, patient_id, medication_name):
         with open("medication.json", "r+") as medication_outfile:

            #read medication json from file as a dict
            medication_db = json.load(medication_outfile)

            #declare list that will store medications linked to patient id
            patient_medications = []

            #iterate condition dict
            for i in medication_db:
                #if condtion is linked to the patient id, append the medication
                #object to the patient_medications list
                if medication_db[i]['subject'] == patient_id and medication_db[i]['medication']['concept']['text'] == medication_name:
                    patient_medications.append(medication_db[i])
                
            #if list isn't empty, return the list
            if len(patient_medications) > 0:
                return patient_medications
            
            #if list is empty, return message
            else:
                return "patient does not have any medications"