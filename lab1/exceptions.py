class StoreError(Exception):
    pass

class BookNotFoundError(StoreError):
    pass

class DataError(StoreError):
    pass
