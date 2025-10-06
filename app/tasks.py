import asyncio
import logging
from .services.job_service import job_service
from .services.ai_service import ai_service
from .models import JobStatus

logger = logging.getLogger(__name__)

async def process_report_generation(job_id: str, topic: str):
    """Background task to handle the report generation process"""
    try:
        # Update job status to processing
        job = await job_service.update_job_status(
            job_id=job_id,
            status=JobStatus.PROCESSING,
            progress=0.1
        )
        
        if not job:
            logger.error(f"Job {job_id} not found")
            return
        
        # Step 1: Generate outline
        try:
            outline = await ai_service.generate_outline(topic)
            await job_service.update_job_status(
                job_id=job_id,
                status=JobStatus.PROCESSING,
                progress=0.3
            )
        except Exception as e:
            logger.error(f"Error generating outline for job {job_id}: {str(e)}")
            await job_service.fail_job(
                job_id=job_id,
                error=f"Failed to generate outline: {str(e)}"
            )
            return
        
        # Step 2: Generate content for each section in parallel
        section_tasks = []
        for i, section in enumerate(outline):
            task = asyncio.create_task(
                ai_service.generate_section_content(topic, section)
            )
            section_tasks.append((section, task))
        
        # Update progress based on number of sections
        num_sections = len(section_tasks)
        sections = {}
        
        for i, (section, task) in enumerate(section_tasks):
            try:
                content = await task
                sections[section] = content
                
                # Update progress
                progress = 0.3 + (0.6 * (i + 1) / num_sections)
                await job_service.update_job_status(
                    job_id=job_id,
                    status=JobStatus.PROCESSING,
                    progress=min(progress, 0.9)
                )
                
            except Exception as e:
                logger.error(f"Error generating section '{section}': {str(e)}")
                # Continue with other sections even if one fails
                sections[section] = f"[Error generating this section: {str(e)}]"
        
        # Step 3: Compile the final report
        report = {
            "topic": topic,
            "outline": outline,
            "sections": sections
        }
        
        # Mark job as completed
        await job_service.set_job_result(job_id, report)
        
    except Exception as e:
        logger.error(f"Unexpected error in report generation for job {job_id}: {str(e)}", exc_info=True)
        await job_service.fail_job(
            job_id=job_id,
            error=f"Unexpected error: {str(e)}"
        )
