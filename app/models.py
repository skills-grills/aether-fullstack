from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal
from enum import Enum
import uuid
from datetime import datetime, timezone

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobBase(BaseModel):
    topic: str = Field(..., description="The topic for the report")
    status: JobStatus = Field(default=JobStatus.PENDING, description="Current status of the job")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Progress of the job (0.0 to 1.0)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    topic: Optional[str] = Field(None, description="The topic for the report")
    status: Optional[JobStatus] = None
    progress: Optional[float] = None
    error: Optional[str] = None
    result: Optional[Dict] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Job(JobBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    error: Optional[str] = Field(None, description="Error message if the job failed")
    result: Optional[Dict] = Field(None, description="The generated report")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "topic": "The Roman Empire",
                "status": "completed",
                "progress": 1.0,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:05:30",
                "result": {
                    "topic": "The Roman Empire",
                    "outline": ["I. The Rise of Rome", "II. The Roman Republic", "III. The Roman Empire"],
                    "sections": {
                        "I. The Rise of Rome": "...detailed content...",
                        "II. The Roman Republic": "...detailed content...",
                        "III. The Roman Empire": "...detailed content..."
                    }
                }
            }
        }

class ReportResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress: Optional[float] = None
    report: Optional[Dict] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "processing",
                "progress": 0.5
            }
        }
