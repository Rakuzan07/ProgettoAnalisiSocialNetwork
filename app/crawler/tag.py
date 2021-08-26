class Tag:

    def __init__(self, name: str, column: int):
        self.name = name
        self.column = column

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_column(self):
        return self.column

    def set_column(self, column):
        self.column = column
