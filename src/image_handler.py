"""
Image handler for managing uploaded images and their placement in presentations.
"""

from PIL import Image
import io
from pptx.util import Inches


class ImageHandler:
    """Handles image processing and placement information."""
    
    def __init__(self):
        self.images = []
    
    def add_image(self, image_file, slide_index, position_description="center", width=4):
        """
        Add an image with placement information.
        
        Args:
            image_file: File-like object containing the image
            slide_index: Index of the slide where the image should be placed
            position_description: Description of where to place the image
            width: Width of the image in inches
        
        Returns:
            Dictionary containing image data
        """
        # Calculate position based on description
        left, top = self._parse_position(position_description)
        
        image_data = {
            'image': image_file,
            'slide_index': slide_index,
            'left': Inches(left),
            'top': Inches(top),
            'width': Inches(width),
            'position_description': position_description
        }
        
        self.images.append(image_data)
        return image_data
    
    def _parse_position(self, position_description):
        """
        Parse position description into coordinates.
        
        Args:
            position_description: String describing position (e.g., "center", "top-left", "bottom-right")
        
        Returns:
            Tuple of (left, top) in inches
        """
        position_map = {
            'center': (2.5, 2.5),
            'top-left': (0.5, 0.5),
            'top-right': (5.5, 0.5),
            'bottom-left': (0.5, 5),
            'bottom-right': (5.5, 5),
            'top-center': (2.5, 0.5),
            'bottom-center': (2.5, 5),
            'middle-left': (0.5, 2.5),
            'middle-right': (5.5, 2.5),
        }
        
        return position_map.get(position_description.lower(), (2.5, 2.5))
    
    def get_all_images(self):
        """
        Get all stored image data.
        
        Returns:
            List of image data dictionaries
        """
        return self.images
    
    def clear_images(self):
        """Clear all stored images."""
        self.images = []
    
    def validate_image(self, image_file):
        """
        Validate that the file is a valid image.
        
        Args:
            image_file: File-like object
        
        Returns:
            Boolean indicating if the image is valid
        """
        try:
            img = Image.open(image_file)
            img.verify()
            return True
        except Exception:
            return False
