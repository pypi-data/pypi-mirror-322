class Mapper():
    def __init__(self):
        pass
    def Map(self, obj, columns):
        if (len(columns) == len(obj)):
            args = {}
            for column in columns:
                args[column] = obj[columns.index(column)]
            return type("Map",(),args)
        else:
            raise ValueError("The number of columns does not match the number of values")
