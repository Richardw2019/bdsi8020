from daos.observation_dao import ObservationDao


class ObservationService:
    def __init__(self):
        self.observation_dao = ObservationDao()

    def create_observation(self, search_params, observation):
        return self.observation_dao.create_observation(search_params,observation)
    
    def assign_observation(self, patient_id, observation_id):
        return self.observation_dao.assign_observation(patient_id, observation_id)
    
    def get_observations(self, patient_id):
        return self.observation_dao.get_observations(patient_id)