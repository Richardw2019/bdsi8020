from daos.encounter_dao import EncounterDao


class EncounterService:
    def __init__(self):
        self.encounter_dao = EncounterDao()

    def create_encounter(self, encounter):
        return self.encounter_dao.create_encounter(encounter)
    
    def get_encounter(self, encounter_id):
        return self.encounter_dao.get_encounter(encounter_id)
    
    def update_encounter(self,encounter_id, patient_id, condition_id):
        return self.encounter_dao.update_encounter(encounter_id, patient_id, condition_id)