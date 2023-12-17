import uuid


class Lab:

    @staticmethod
    def generate_id():
        unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id
