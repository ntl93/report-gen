"""
LLM-based text refinement module for converting draft text to formal content.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMRefiner:
    """Refines draft text using OpenAI's GPT models."""
    
    def __init__(self, api_key=None):
        """
        Initialize the LLM refiner.
        
        Args:
            api_key: OpenAI API key (optional, will use OPENAI_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
    
    def refine_text(self, draft_text, context="weekly project report"):
        """
        Refine draft text into formal, professional content.
        
        Args:
            draft_text: The draft text to refine
            context: Context for the refinement (e.g., "weekly project report")
        
        Returns:
            Refined text
        """
        if not draft_text or not draft_text.strip():
            return ""
        
        prompt = f"""You are a professional business writer. Please refine the following draft text into formal, professional content suitable for a {context}.

Requirements:
- Maintain all key information and facts
- Use formal business language
- Make it clear and concise
- Keep the same general structure and length
- Do not add information that isn't in the draft

Draft text:
{draft_text}

Refined text:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional business writer who refines draft text into polished, formal content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            refined_text = response.choices[0].message.content.strip()
            return refined_text
        
        except Exception as e:
            print(f"Error refining text with LLM: {e}")
            return draft_text
    
    def refine_slide_content(self, slide_data):
        """
        Refine content for a single slide.
        
        Args:
            slide_data: Dictionary with 'title' and 'content' keys
        
        Returns:
            Dictionary with refined title and content
        """
        refined_title = self.refine_text(
            slide_data.get('title', ''),
            context="slide title"
        )
        
        refined_content = self.refine_text(
            slide_data.get('content', ''),
            context="slide content"
        )
        
        return {
            'title': refined_title,
            'content': refined_content,
            'layout': slide_data.get('layout', 0)
        }
    
    def refine_all_slides(self, slides_data):
        """
        Refine content for multiple slides.
        
        Args:
            slides_data: List of slide data dictionaries
        
        Returns:
            List of refined slide data dictionaries
        """
        return [self.refine_slide_content(slide) for slide in slides_data]
