from daos.medication_dao import MedicationDao


class MedciationService:
    def __init__(self):
        self.medication_dao = MedicationDao()

    def create_medication(self, search_params, medication):
        return self.medication_dao.create_medication(search_params,medication)
    
    def assign_medication(self, patient_id, medication_id):
        return self.medication_dao.assign_medication(patient_id, medication_id)
    
    
    def get_medications(self, patient_id, medication_name):
        return self.medication_dao.get_medications(patient_id, medication_name)