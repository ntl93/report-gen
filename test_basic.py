"""
Simple test script to verify the basic functionality of the report generator.
"""

import sys
import os
from io import BytesIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pptx_handler import PPTXHandler
from src.image_handler import ImageHandler


def test_pptx_handler():
    """Test basic PPTX handler functionality."""
    print("Testing PPTX Handler...")
    
    handler = PPTXHandler()
    
    # Test creating a simple presentation without reference
    # (will fail, which is expected)
    try:
        handler.create_report_from_template([{'title': 'Test', 'content': 'Test content'}])
        print("❌ Should have raised error without reference")
    except ValueError as e:
        print(f"✅ Correctly raised error: {e}")
    
    print()


def test_image_handler():
    """Test image handler functionality."""
    print("Testing Image Handler...")
    
    handler = ImageHandler()
    
    # Test position parsing
    positions = ['center', 'top-left', 'bottom-right', 'invalid']
    for pos in positions:
        left, top = handler._parse_position(pos)
        print(f"  Position '{pos}': ({left}, {top})")
    
    # Test adding image metadata
    img_data = handler.add_image(
        BytesIO(b'fake_image_data'),
        slide_index=0,
        position_description='center',
        width=4
    )
    print(f"✅ Added image data: slide_index={img_data['slide_index']}, position={img_data['position_description']}")
    
    # Test getting all images
    all_images = handler.get_all_images()
    print(f"✅ Total images stored: {len(all_images)}")
    
    print()


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.pptx_handler import PPTXHandler
        print("✅ pptx_handler imported")
    except Exception as e:
        print(f"❌ Failed to import pptx_handler: {e}")
    
    try:
        from src.llm_refiner import LLMRefiner
        print("✅ llm_refiner imported")
    except Exception as e:
        print(f"❌ Failed to import llm_refiner: {e}")
    
    try:
        from src.image_handler import ImageHandler
        print("✅ image_handler imported")
    except Exception as e:
        print(f"❌ Failed to import image_handler: {e}")
    
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("Running Basic Tests")
    print("=" * 50)
    print()
    
    test_imports()
    test_pptx_handler()
    test_image_handler()
    
    print("=" * 50)
    print("Tests completed!")
    print("=" * 50)
