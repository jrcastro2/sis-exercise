"""Custom Exception Classes."""

class BulkSaveError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors or []