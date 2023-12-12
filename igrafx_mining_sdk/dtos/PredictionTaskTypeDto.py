from enum import Enum

class PredictionTaskTypeDto(Enum):
    TRAIN_TOPOLOGY = "TRAIN_TOPOLOGY"
    TRAIN_DURATION = "TRAIN_DURATION"
    INFER_PREDICTION = "INFER_PREDICTION"
