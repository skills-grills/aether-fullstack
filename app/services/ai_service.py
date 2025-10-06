import json
import httpx
from typing import List, Dict, Optional
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.API_BASE_URL
        self.model = settings.MODEL_NAME
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _call_ai(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Generic method to call the AI API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Error calling AI API: {str(e)}")
                raise

    async def generate_outline(self, topic: str) -> List[str]:
        """Generate an outline for the given topic"""
        prompt = f"""
        Generate a detailed outline for a report about: {topic}
        
        The outline should be in the following format:
        - Main Topic 1
        - Main Topic 2
        - Main Topic 3
        
        Each main topic should be a clear, concise heading that covers a major aspect of the topic.
        Return ONLY the outline, with each item on a new line, prefixed with a dash and space ("- ").
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates detailed report outlines."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await self._call_ai(messages)
            # Parse the response into a list of outline items
            outline = [line.strip(" -\n") for line in result.split("\n") if line.strip()]
            return outline
        except Exception as e:
            logger.error(f"Error generating outline: {str(e)}")
            raise

    async def generate_section_content(self, topic: str, section: str) -> str:
        """Generate detailed content for a specific section of the report"""
        prompt = f"""
        Write a detailed, informative section about "{section}" as part of a larger report about "{topic}".
        
        The section should be comprehensive, well-structured, and written in a professional tone.
        Include relevant facts, examples, and analysis where appropriate.
        The content should be at least 3-5 paragraphs long.
        """
        
        messages = [
            {"role": "system", "content": "You are a professional researcher and writer."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            return await self._call_ai(messages)
        except Exception as e:
            logger.error(f"Error generating section content: {str(e)}")
            raise

# Create a singleton instance
ai_service = AIService()
