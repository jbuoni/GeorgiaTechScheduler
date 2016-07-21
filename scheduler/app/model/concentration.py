from ..model import concentrationDao

class Concentration():

    @staticmethod
    def get_concentration(id):
        return concentrationDao.get_concentration(id)

    @staticmethod
    def get_concentration_name(id):
        concentration = concentrationDao.get_concentration(id)
        if concentration is not None:
            return concentrationDao.get_concentration_name(id)

        return None
