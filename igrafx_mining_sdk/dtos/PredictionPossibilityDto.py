from enum import Enum


class PredictionPossibilityDto(Enum):
    """Class PredictionPossibilityDto for the prediction possiblility: CAN_LAUNCH_PREDICTION if prediction can be
    launched, explicit error code if can not be launched."""

    CAN_LAUNCH_PREDICTION = "CAN_LAUNCH_PREDICTION"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    NO_DATA_IN_PROJECT = "NO_DATA_IN_PROJECT"
    NO_END_CASE_RULE = "NO_END_CASE_RULE"
    NO_COMPLETED_CASE = "NO_COMPLETED_CASE"
    NO_NON_COMPLETED_CASE = "NO_NON_COMPLETED_CASE"
    PREDICTION_SERVICE_FAILURE = "PREDICTION_SERVICE_FAILURE"
    NON_ACTIVATED_PREDICTION = "NON_ACTIVATED_PREDICTION"
    FORBIDDEN = "FORBIDDEN"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INVALID_RESPONSE = "INVALID_RESPONSE"
