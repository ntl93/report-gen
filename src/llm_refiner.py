"""
LLM-based text refinement module for converting draft text to formal content.
Supports Azure OpenAI and local LLM endpoints compatible with OpenAI API spec.
"""

import os
from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv
import config

load_dotenv()


class LLMRefiner:
    """Refines draft text using LLM models (Azure OpenAI or local LLM with OpenAI API spec)."""
    
    def __init__(self, api_key=None, base_url=None, api_version=None):
        """
        Initialize the LLM refiner.
        
        Args:
            api_key: API key (optional, will use LLM_API_KEY env var if not provided)
            base_url: Base URL for API endpoint (optional, will use LLM_BASE_URL env var if not provided)
            api_version: API version for Azure OpenAI (optional, will use LLM_API_VERSION env var if not provided)
        """
        self.provider = os.getenv('LLM_PROVIDER', 'azure').lower()
        self.api_key = api_key or os.getenv('LLM_API_KEY')
        self.base_url = base_url or os.getenv('LLM_BASE_URL')
        self.api_version = api_version or os.getenv('LLM_API_VERSION', '2024-02-15-preview')
        
        if not self.api_key:
            raise ValueError("LLM API key not provided and LLM_API_KEY environment variable not set")
        
        # Initialize client based on provider
        if self.provider == 'azure':
            if not self.base_url:
                raise ValueError("Azure OpenAI endpoint not provided. Set LLM_BASE_URL environment variable")
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                azure_endpoint=self.base_url
            )
        else:
            # Local LLM or OpenAI-compatible endpoint
            if self.base_url:
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            else:
                self.client = OpenAI(api_key=self.api_key)
        
        self.model = config.LLM_MODEL
    
    def refine_text(self, draft_text, context=None):
        """
        Refine draft text into formal, professional content.
        
        Args:
            draft_text: The draft text to refine
            context: Context for the refinement (default from config)
        
        Returns:
            Refined text
        """
        if not draft_text or not draft_text.strip():
            return ""
        
        if context is None:
            context = config.REFINEMENT_CONTEXT_TEMPLATE
        
        prompt = config.REFINEMENT_PROMPT_TEMPLATE.format(
            context=context,
            draft_text=draft_text
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.LLM_MAX_TOKENS
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
