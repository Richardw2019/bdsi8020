from daos.condition_dao import ConditionDao


class ConditonService:
    def __init__(self):
        self.conditon_dao = ConditionDao()

    def create_condition(self, search_params, condition):
        return self.conditon_dao.create_condition(search_params,condition)
    
    def assign_condition(self, patient_id, condition_id):
        return self.conditon_dao.assign_condition(patient_id, condition_id)
    
    def get_conditions(self, patient_id):
        return self.conditon_dao.get_conditions(patient_id)