import uuid
from typing import List, Optional
from datetime import datetime
from igrafx_mining_sdk.dtos.PredictionStatusDto import PredictionStatusDto
from igrafx_mining_sdk.dtos.PredictionTaskTypeDto import PredictionTaskTypeDto

class WorkflowStatusDto:
    def __init__(self, prediction_id: uuid.UUID, project_id: uuid.UUID, status: PredictionStatusDto, start_time: datetime,
                 end_time: Optional[datetime] = None, completed_tasks: Optional[List[PredictionTaskTypeDto]] = None):
        self.prediction_id = prediction_id
        self.project_id = project_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.completed_tasks = completed_tasks

    def __eq__(self, other):
        if not isinstance(other, WorkflowStatusDto):
            return False

        return (
                self.prediction_id == other.prediction_id and
                self.project_id == other.project_id and
                self.status == other.status and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.completed_tasks == other.completed_tasks
        )
