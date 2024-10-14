class TableNotUniqueError(Exception):
    def __init__(self, message="Value must be unique"):
        self.message = message
        super().__init__(self.message)

class TableDoesNotExistError(Exception):
    def __init__(self, message="The table does not exist"):
        self.message = message
        super().__init__(self.message)


class PageNoCapacityError(Exception):
    def __init__(self, message="Page does not have enough capacity to write to"):
        self.message = message
        super().__init__(self.message)