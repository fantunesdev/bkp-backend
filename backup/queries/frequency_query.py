from backup.databases import database


class FrequencyQuery:
    def __init__(self, session):
        self.session = session

    def get_frequencies(self):
        return self.session.query(database.Frequency)

    def get_frequency_by_id(self, frequency_id):
        return (
            self.session.query(database.Frequency)
            .filter(database.Frequency.id == frequency_id)
            .first()
        )
