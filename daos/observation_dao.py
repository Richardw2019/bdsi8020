import json
import os
from fastapi.encoders import jsonable_encoder
import requests

class ObservationDao:

    def _init_(self):
        pass

    #use the search params in the UML api to get the LOINC code and name
    def create_observation(self, search_params, observation):
        API_KEY = 'f2577616-a7e0-45e4-a76c-c550a96d914a'
        BASE_URL = 'https://uts-ws.nlm.nih.gov/rest'
        search_url = f'/search/current?string={search_params}&searchType=exact&returnIdType=sourceConcept&sabs=LNC&apiKey={API_KEY}'
        api_call = BASE_URL + search_url
        
        uml_json = requests.get(api_call).json()

        #convert observation object dict
        observation_dict = observation.dict()

        #remove any results that don't have a LOINC code
        for x in uml_json['result']['results']:
            if 'MTHU' in x['ui']:
                uml_json['result']['results'].remove(x)
        
        print(uml_json)

        #set observation code attribute to results from uml api call
        observation_dict['code']['coding'] = uml_json['result']['results'][0]['ui']
        observation_dict['code']['text'] = uml_json['result']['results'][0]['name']

        observation_dict['component']['code']['coding'] = uml_json['result']['results'][0]['ui']
        observation_dict['component']['code']['text'] = uml_json['result']['results'][0]['name']

        observation_db = {}

        #if file is empty
        if os.stat('observation.json').st_size == 0:
            with open("observation.json", "w") as outfile:

                #create a dict storing the response body as a key value pair
                observation_db[str(1)] = observation_dict

                #write to file, prettifying the json
                outfile.write(json.dumps(observation_db, indent=4))

                return observation_dict
        
        else:
            with open("observation.json", "r+") as outfile:
                
                #read json from file as dict
                db = json.load(outfile)

                #find the max key in the dict and then increment from that number.
                #this will be the key for the new patient
                key = max(db.keys())
                key = int(key)
                key += 1

                #create a new key-value pair in the existing dict
                db[str(key)] = observation_dict

                # #delete old dict
                # outfile.truncate(0)
                outfile.seek(0) 
                outfile.truncate()

                #write to file, prettifying the json
                outfile.write(json.dumps(db, indent=4))

                return observation_dict


    def assign_observation(self, patient_id, observation_id):

        #open patient json
        with open("patient.json", "r+") as patient_outfile:

            #read json from file as dict
            patient_db = json.load(patient_outfile)

            #check if patient exists in dict
            if patient_id not in patient_db: 
                return "patient does not exist"
            
        #open observation json
        with open("observation.json", "r+") as observation_outfile:

            #read observation json from file as a dict
            observation_db = json.load(observation_outfile)

            #check if observation exists in dict
            if observation_id not in observation_db:
                return "observation doesn't exist, create observation"
            
            else: 
                #check if observation has been assigned to a patient
                if observation_db[observation_id]['subject'] != 'DO NOT EDIT: Patient ID':
                    return "Existing observation already has a patient assigned to it, create a new observation"

                #if all checks are ignored, set the subject of the specified observation to the patient id
                else:
                    observation_db[observation_id]['subject'] = patient_id


                    #clear the observation json and write to it with the updated json
                    observation_outfile.seek(0)
                    observation_outfile.truncate()
                    observation_outfile.write(json.dumps(observation_db, indent=4))

                    return observation_db[observation_id]


    def get_observations(self, patient_id):
         with open("observation.json", "r+") as observation_outfile:

            #read observation json from file as a dict
            observation_db = json.load(observation_outfile)

            #declare list that will store observations linked to patient id
            patient_observations = []

            #iterate condition dict
            for i in observation_db:
                #if condtion is linked to the patient id, append the observation
                #object to the patient_observations list
                if observation_db[i]['subject'] == patient_id:
                    patient_observations.append(observation_db[i])
                
            #if list isn't empty, return the list
            if len(patient_observations) > 0:
                return patient_observations
            
            #if list is empty, return message
            else:
                return "patient does not have any observations"