from typing import List, Dict, Optional, TypeVar, Type, Any
import logging
from pydantic import BaseModel, Field
import instructor
from openai import AsyncOpenAI
from ..config import settings

logger = logging.getLogger(__name__)

# Initialize the OpenAI client with Instructor
client = instructor.patch(AsyncOpenAI(api_key=settings.API_KEY))

class Section(BaseModel):
    """Represents a section in the report outline"""
    title: str = Field(..., description="The title of the section")
    description: str = Field(..., description="A brief description of what this section will cover")

class ReportOutline(BaseModel):
    """Structured outline for the report"""
    sections: List[Section] = Field(..., description="List of sections in the report")
    
    def get_section_titles(self) -> List[str]:
        """Extract just the section titles"""
        return [section.title for section in self.sections]

class AIService:
    """Service for interacting with AI models using Instructor for structured outputs"""
    
    def __init__(self):
        self.model = settings.MODEL_NAME
        self.client = client

    async def _call_structured_llm(
        self,
        response_model: Type[BaseModel],
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        **kwargs: Any
    ) -> BaseModel:
        """Generic method to call the LLM with structured output"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                response_model=response_model,
                messages=messages,
                temperature=temperature,
                **kwargs
            )
            return response
        except Exception as e:
            logger.error(f"Error calling AI API: {str(e)}")
            raise

    async def generate_outline(self, topic: str) -> List[str]:
        """Generate a structured outline for the given topic"""
        system_prompt = """You are an expert researcher and writer. 
        Create a detailed, well-structured outline for a comprehensive report.
        """
        
        user_prompt = f"""
        Create a detailed outline for a report about: {topic}
        
        The outline should cover all major aspects of the topic in a logical flow.
        For each section, provide a clear title and a brief description of what it will cover.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            outline = await self._call_structured_llm(
                response_model=ReportOutline,
                messages=messages,
                temperature=0.7
            )
            return outline.get_section_titles()
        except Exception as e:
            logger.error(f"Error generating outline: {str(e)}")
            raise

    async def generate_section_content(self, topic: str, section: str) -> str:
        """Generate detailed content for a specific section of the report"""
        system_prompt = """You are a professional researcher and writer. 
        Write a comprehensive, well-structured section for a report.
        """
        
        user_prompt = f"""
        Write a detailed section about "{section}" for a report about "{topic}".
        
        The section should be:
        - Comprehensive and informative
        - Well-structured with clear paragraphs
        - Written in a professional, academic tone
        - Include relevant facts, examples, and analysis
        - At least 3-5 paragraphs long
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                response_model=str
            )
            return response
        except Exception as e:
            logger.error(f"Error generating section content: {str(e)}")
            raise

# Create a singleton instance
ai_service = AIService()
