from enum import Enum

class PredictionStatusDto(Enum):
    RUNNING = "RUNNING"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    CANCELED = "CANCELED"
    ERROR = "ERROR"
