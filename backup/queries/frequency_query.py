from backup.databases.database import Frequency


class FrequencyQuery:
    def get_frequencies(self, session):
        frequencies = session.query(Frequency)
        return frequencies

    def get_frequency_by_id(self, session, frequency_id):
        return session.query(Frequency).filter(Frequency.id == frequency_id).first()
