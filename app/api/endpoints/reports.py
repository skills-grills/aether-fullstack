from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from pydantic import BaseModel
import logging

from ...services.job_service import job_service
from ...models import JobStatus, ReportResponse
from ...tasks import process_report_generation

router = APIRouter()
logger = logging.getLogger(__name__)

class ReportRequest(BaseModel):
    topic: str

@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks
) -> ReportResponse:
    """
    Create a new report generation job
    
    - **topic**: The topic for the report (e.g., "The Roman Empire")
    """
    try:
        # Create a new job
        job = await job_service.create_job(topic=request.topic)
        
        # Start the background task
        background_tasks.add_task(
            process_report_generation,
            job_id=job.id,
            topic=request.topic
        )
        
        return ReportResponse(
            job_id=job.id,
            status=job.status,
            progress=job.progress
        )
        
    except Exception as e:
        logger.error(f"Failed to create report job: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create report job: {str(e)}"
        )

@router.get("/reports/{job_id}", response_model=ReportResponse)
async def get_report_status(job_id: str) -> ReportResponse:
    """
    Get the status of a report generation job
    
    - **job_id**: The ID of the job to check
    """
    job = await job_service.get_job(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )
    
    response = ReportResponse(
        job_id=job.id,
        status=job.status,
        progress=job.progress
    )
    
    if job.status == JobStatus.COMPLETED and job.result:
        response.report = job.result
    elif job.status == JobStatus.FAILED and job.error:
        response.error = job.error
    
    return response
