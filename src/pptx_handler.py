"""
PowerPoint handler for extracting and applying styles from reference presentations.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from copy import deepcopy
import io


class PPTXHandler:
    """Handles PowerPoint file operations including style extraction and application."""
    
    def __init__(self):
        self.reference_pres = None
        self.slide_layouts = []
        self.theme_colors = {}
        
    def load_reference(self, pptx_file):
        """
        Load a reference PowerPoint file to extract styles.
        
        Args:
            pptx_file: File-like object or path to PPTX file
        """
        self.reference_pres = Presentation(pptx_file)
        self._extract_theme_info()
        return True
    
    def _extract_theme_info(self):
        """Extract theme colors and fonts from the reference presentation."""
        if not self.reference_pres:
            return
        
        # Store slide layouts
        self.slide_layouts = list(self.reference_pres.slide_layouts)
        
        # Extract theme colors
        try:
            theme = self.reference_pres.slide_master.theme
            for i, color in enumerate(theme.theme_color_scheme):
                self.theme_colors[f'color_{i}'] = color
        except (AttributeError, NotImplementedError) as e:
            # Some presentations may not have theme colors accessible
            pass
    
    def create_report_from_template(self, content_data, images_data=None):
        """
        Create a new presentation using the reference template.
        
        Args:
            content_data: List of dictionaries containing slide content
                         [{'title': str, 'content': str, 'layout': int}, ...]
            images_data: List of dictionaries containing image information
                        [{'slide_index': int, 'image': file, 'position': tuple}, ...]
        
        Returns:
            BytesIO object containing the generated PPTX
        """
        if not self.reference_pres:
            raise ValueError("No reference presentation loaded")
        
        # Create a new presentation using the reference as a base
        # This preserves the slide master and theme
        prs = Presentation(io.BytesIO(self._get_reference_bytes()))
        
        # Remove all existing slides except the first one (we'll use it as template)
        while len(prs.slides) > 1:
            rId = prs.slides._sldIdLst[1].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[1]
        
        # Clear the first slide or remove it if we have content
        if content_data:
            rId = prs.slides._sldIdLst[0].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[0]
        
        # Add new slides with content
        for slide_data in content_data:
            layout_index = slide_data.get('layout', 0)
            if layout_index >= len(prs.slide_layouts):
                layout_index = 0
            
            slide_layout = prs.slide_layouts[layout_index]
            slide = prs.slides.add_slide(slide_layout)
            
            # Add title
            if hasattr(slide.shapes, 'title') and slide.shapes.title:
                slide.shapes.title.text = slide_data.get('title', '')
            
            # Add content to text placeholders
            content = slide_data.get('content', '')
            for shape in slide.shapes:
                if hasattr(shape, "text_frame") and shape != slide.shapes.title:
                    if shape.is_placeholder:
                        shape.text_frame.text = content
                        break
        
        # Add images if provided
        if images_data:
            self._add_images_to_presentation(prs, images_data)
        
        # Save to BytesIO
        output = io.BytesIO()
        prs.save(output)
        output.seek(0)
        return output
    
    def _get_reference_bytes(self):
        """Get the reference presentation as bytes."""
        output = io.BytesIO()
        self.reference_pres.save(output)
        output.seek(0)
        return output.read()
    
    def _add_images_to_presentation(self, prs, images_data):
        """
        Add images to specific slides in the presentation.
        
        Args:
            prs: Presentation object
            images_data: List of image data dictionaries
        """
        for img_data in images_data:
            slide_index = img_data.get('slide_index', 0)
            if slide_index >= len(prs.slides):
                continue
            
            slide = prs.slides[slide_index]
            image_file = img_data.get('image')
            
            # Default position (center of slide)
            left = img_data.get('left', Inches(2))
            top = img_data.get('top', Inches(2))
            width = img_data.get('width', Inches(4))
            
            try:
                slide.shapes.add_picture(image_file, left, top, width=width)
            except Exception as e:
                print(f"Error adding image to slide {slide_index}: {e}")
    
    def get_slide_layouts_info(self):
        """
        Get information about available slide layouts.
        
        Returns:
            List of layout names
        """
        if not self.reference_pres:
            return []
        
        return [layout.name for layout in self.reference_pres.slide_layouts]
