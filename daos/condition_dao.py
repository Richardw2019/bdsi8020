import json
import os
from fastapi.encoders import jsonable_encoder
import requests

class ConditionDao:

    def _init_(self):
        pass

    #use the search params in the UML api to get the ICD10CM code and name
    def create_condition(self, search_params, condition):

        API_KEY = 'f2577616-a7e0-45e4-a76c-c550a96d914a'
        BASE_URL = 'https://uts-ws.nlm.nih.gov/rest'
        search_url = f'/search/current?string={search_params}&sabs=ICD10CM&returnIdType=code&apiKey={API_KEY}'
        api_call = BASE_URL + search_url
        
        uml_json = requests.get(api_call).json()

        #convert condition object dict
        condition_dict = condition.dict()

        #set condition code attribute to results from uml api call
        condition_dict['code']['coding'] = uml_json['result']['results'][0]['ui']
        condition_dict['code']['text'] = uml_json['result']['results'][0]['name']

        print(uml_json['result']['results'][0]['ui'])

        condition_db = {}

        #if file is empty
        if os.stat('condition.json').st_size == 0:
            with open("condition.json", "w") as outfile:

                #create a dict storing the response body as a key value pair
                condition_db[str(1)] = condition_dict

                #write to file, prettifying the json
                outfile.write(json.dumps(condition_db, indent=4))

                return condition_dict
        
        else:
            with open("condition.json", "r+") as outfile:
                
                #read json from file as dict
                db = json.load(outfile)

                #find the max key in the dict and then increment from that number.
                #this will be the key for the new patient
                key = max(db.keys())
                key = int(key)
                key += 1

                #create a new key-value pair in the existing dict
                db[str(key)] = condition_dict

                # #delete old dict
                # outfile.truncate(0)
                outfile.seek(0) 
                outfile.truncate()

                #write to file, prettifying the json
                outfile.write(json.dumps(db, indent=4))

                return condition_dict
 
        return condition_dict

    def assign_condition(self, patient_id, condition_id):

        #open patient json
        with open("patient.json", "r+") as patient_outfile:

            #read json from file as dict
            patient_db = json.load(patient_outfile)

            #check if patient exists in dict
            if patient_id not in patient_db: 
                return "patient does not exist"
            
        #open condition json
        with open("condition.json", "r+") as condition_outfile:

            #read condition json from file as a dict
            condition_db = json.load(condition_outfile)

            #check if condition exists in dict
            if condition_id not in condition_db:
                return "condition doesn't exist, create condition"
            
            else: 
                #check if condition has been assigned to a patient
                if condition_db[condition_id]['subject'] != 'DO NOT EDIT: Patient ID':
                    return "Existing condition already has a patient assigned to it, create a new condition"

                #if all checks are ignored, set the subject of the specified condition to the patient id
                else:
                    condition_db[condition_id]['subject'] = patient_id


                    #clear the condition json and write to it with the updated json
                    condition_outfile.seek(0)
                    condition_outfile.truncate()
                    condition_outfile.write(json.dumps(condition_db, indent=4))

                    return condition_db[condition_id]
                
    def get_conditions(self, patient_id):

        with open("condition.json", "r+") as condition_outfile:

            #read condition json from file as a dict
            condition_db = json.load(condition_outfile)

            #declare list that will store condtions linked to patient id
            patient_conditions = []

            #iterate condition dict
            for i in condition_db:
                #if condtion is linked to the patient id, append the condition
                #object to the patient_condtions list
                if condition_db[i]['subject'] == patient_id:
                    patient_conditions.append(condition_db[i])
                
            #if list isn't empty, return the list
            if len(patient_conditions) > 0:
                return patient_conditions
            
            #if list is empty, return message
            else:
                return "patient does not have any conditions"