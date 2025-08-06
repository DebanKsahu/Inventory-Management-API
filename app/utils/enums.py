from enum import Enum


class TransactionType(str, Enum):
    IN = "In"
    OUT = "Out"

class ResponseStatus(str, Enum):
    SUCCESS = "Success"
    FAIL = "Failure"