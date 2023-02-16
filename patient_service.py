from patient_dao import PatientDao

class PatientService:
    def __init__(self):
        self.patient_dao = PatientDao()

    def create_patient(self, patient):
        return self.patient_dao.create_patient(patient)
    
    def update_patient_info(self, patient_id, patient):
        return self.patient_dao.update_patient_info(patient_id, patient)

    def get_patient_info(self, patient_id):
        return self.patient_dao.get_patient_info(patient_id)