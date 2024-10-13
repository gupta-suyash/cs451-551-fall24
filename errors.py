class NotUniqueError(Exception):
    def __init__(self, message="Value must be unique"):
        self.message = message
        super().__init__(self.message)