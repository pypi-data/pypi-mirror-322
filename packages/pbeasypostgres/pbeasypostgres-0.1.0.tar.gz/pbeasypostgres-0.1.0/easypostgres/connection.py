import psycopg2 as ps
from .mapper import Mapper

class Connection():
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.Open()
    def Open(self):
        self.connection = ps.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        self.mapper = Mapper()
    def Close(self):
        self.cursor.close()
        self.connection.close()
    def Query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
        try:
            data = [list(obj) for obj in self.cursor.fetchall()]
            columns = [desc[0] for desc in self.cursor.description]
            result = []
            for obj in data:
                result.append(self.mapper.Map(obj, columns))
            return result
        except Exception as ex:
            return None
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(exc_value)
        else:
            self.Close()
        return False
