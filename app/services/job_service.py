from datetime import datetime, timezone
from typing import Dict, Optional
import redis.asyncio as redis
from ..config import settings
from ..models import Job, JobStatus, JobUpdate
import logging

logger = logging.getLogger(__name__)

class JobService:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    async def _get_job_key(self, job_id: str) -> str:
        return f"job:{job_id}"

    async def create_job(self, topic: str) -> Job:
        job = Job(topic=topic)
        job_key = await self._get_job_key(job.id)
        
        await self.redis.set(
            job_key,
            job.model_dump_json(),
            ex=86400  # 24h TTL
        )
        
        return job

    async def get_job(self, job_id: str) -> Optional[Job]:
        job_key = await self._get_job_key(job_id)
        job_data = await self.redis.get(job_key)
        
        if not job_data:
            return None
            
        return Job.model_validate_json(job_data)

    async def update_job(self, job_id: str, update_data: JobUpdate) -> Optional[Job]:
        job = await self.get_job(job_id)
        if not job:
            return None
            
        # Update job fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            if hasattr(job, field):
                setattr(job, field, value)
        
        job.updated_at = update_data.updated_at
        
        # Save back to Redis
        job_key = await self._get_job_key(job_id)
        await self.redis.set(
            job_key,
            job.model_dump_json(),
            ex=86400  # Refresh TTL
        )
        
        return job

    async def update_job_status(
        self, 
        job_id: str, 
        status: JobStatus, 
        error: Optional[str] = None,
        progress: Optional[float] = None
    ) -> Optional[Job]:
        update_data = JobUpdate(
            status=status,
            error=error,
            progress=progress,
            updated_at=datetime.now(timezone.utc)
        )
        return await self.update_job(job_id, update_data)

    async def set_job_result(self, job_id: str, result: Dict) -> Optional[Job]:
        update_data = JobUpdate(
            result=result,
            status=JobStatus.COMPLETED,
            progress=1.0,
            updated_at=datetime.utcnow()
        )
        return await self.update_job(job_id, update_data)

    async def fail_job(self, job_id: str, error: str) -> Optional[Job]:
        return await self.update_job_status(
            job_id=job_id,
            status=JobStatus.FAILED,
            error=error,
            progress=1.0
        )

# Create a singleton instance
job_service = JobService()
