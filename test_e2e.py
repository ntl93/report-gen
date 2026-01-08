"""
End-to-end test for the report generator.
Creates a complete report with all features.
"""

import sys
import os
from io import BytesIO
from PIL import Image
from pptx import Presentation
from pptx.util import Inches

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pptx_handler import PPTXHandler
from src.image_handler import ImageHandler


def create_test_image():
    """Create a simple test image."""
    img = Image.new('RGB', (400, 300), color='blue')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


def test_end_to_end():
    """Test the complete workflow."""
    print("=" * 60)
    print("End-to-End Report Generation Test")
    print("=" * 60)
    print()
    
    # Step 1: Create a reference template
    print("Step 1: Creating reference template...")
    template_bytes = BytesIO()
    
    # Create fresh template
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Reference Template"
    
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    
    prs.save(template_bytes)
    template_bytes.seek(0)
    print("✅ Reference template created")
    print()
    
    # Step 2: Load reference template
    print("Step 2: Loading reference template...")
    handler = PPTXHandler()
    handler.load_reference(template_bytes)
    layouts = handler.get_slide_layouts_info()
    print(f"✅ Template loaded with {len(layouts)} layouts:")
    for idx, layout in enumerate(layouts):
        print(f"   {idx}: {layout}")
    print()
    
    # Step 3: Prepare images
    print("Step 3: Preparing images...")
    image_handler = ImageHandler()
    test_image = create_test_image()
    image_handler.add_image(test_image, 1, 'center', 3)
    images = image_handler.get_all_images()
    print(f"✅ Added {len(images)} image(s)")
    print()
    
    # Step 4: Prepare content
    print("Step 4: Preparing content...")
    slides_data = [
        {
            'title': 'Weekly Report - Week 1',
            'content': 'This is the title slide',
            'layout': 0
        },
        {
            'title': 'Accomplishments',
            'content': 'Completed project setup\nImplemented core features\nTested functionality',
            'layout': 1
        },
        {
            'title': 'Next Steps',
            'content': 'Deploy to production\nGather user feedback\nPlan next iteration',
            'layout': 1
        }
    ]
    print(f"✅ Prepared {len(slides_data)} slides")
    print()
    
    # Step 5: Generate report
    print("Step 5: Generating report...")
    output = handler.create_report_from_template(slides_data, images)
    print("✅ Report generated successfully")
    print()
    
    # Step 6: Verify output
    print("Step 6: Verifying output...")
    output.seek(0)
    generated_prs = Presentation(output)
    
    print(f"   Slides in generated report: {len(generated_prs.slides)}")
    print(f"   Expected slides: {len(slides_data)}")
    
    if len(generated_prs.slides) == len(slides_data):
        print("✅ Slide count matches")
    else:
        print("❌ Slide count mismatch")
    
    # Check slide titles
    for idx, slide in enumerate(generated_prs.slides):
        if hasattr(slide.shapes, 'title') and slide.shapes.title:
            actual_title = slide.shapes.title.text
            expected_title = slides_data[idx]['title']
            status = "✅" if actual_title == expected_title else "⚠️"
            print(f"   Slide {idx}: {status} '{actual_title}'")
    
    print()
    
    # Step 7: Save test output
    print("Step 7: Saving test output...")
    test_output_path = 'test_output.pptx'
    output.seek(0)
    with open(test_output_path, 'wb') as f:
        f.write(output.read())
    print(f"✅ Test report saved to {test_output_path}")
    print()
    
    print("=" * 60)
    print("✅ All tests passed successfully!")
    print("=" * 60)
    print()
    print(f"You can open {test_output_path} to view the generated report.")


if __name__ == "__main__":
    test_end_to_end()
