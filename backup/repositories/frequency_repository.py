from backup.queries import frequency_query


class FrequencyRepository:
    def __init__(self, session):
        """Método construtor."""
        self.session = session
        self.queries = frequency_query.FrequencyQuery(self.session)

    def get_frequency_by_id(self, frequency_id):
        return self.queries.get_frequency_by_id(frequency_id)
