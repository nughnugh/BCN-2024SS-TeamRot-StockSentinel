class Source:
    def __init__(self, name: str, url: str, db_id=None):
        self.db_id = db_id
        self.name = name
        self.url = url
