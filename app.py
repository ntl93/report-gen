"""
Weekly PowerPoint Report Generator - Main Application
"""

import streamlit as st
import os
from io import BytesIO
from src.pptx_handler import PPTXHandler
from src.llm_refiner import LLMRefiner
from src.image_handler import ImageHandler
import config


def init_session_state():
    """Initialize session state variables."""
    if 'pptx_handler' not in st.session_state:
        st.session_state.pptx_handler = PPTXHandler()
    if 'image_handler' not in st.session_state:
        st.session_state.image_handler = ImageHandler()
    if 'reference_loaded' not in st.session_state:
        st.session_state.reference_loaded = False
    if 'slides_data' not in st.session_state:
        st.session_state.slides_data = []


def main():
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.PAGE_LAYOUT
    )
    
    init_session_state()
    
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.markdown("""
    Generate professional weekly reports with consistent styling and LLM-refined content.
    """)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.warning("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        st.info("The application will still work, but content will not be refined by AI.")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload Reference Reports",
        "🖼️ Upload Images",
        "✍️ Create Content",
        "🎯 Generate Report"
    ])
    
    with tab1:
        upload_reference_reports()
    
    with tab2:
        upload_images()
    
    with tab3:
        create_content()
    
    with tab4:
        generate_report()


def upload_reference_reports():
    """Handle reference report uploads."""
    st.header("Upload Reference Reports")
    st.markdown("""
    Upload one or more previous PowerPoint reports. The app will extract and preserve:
    - Slide master and layouts
    - Theme colors
    - Font styles
    - Overall design consistency
    """)
    
    uploaded_files = st.file_uploader(
        "Choose PowerPoint files (.pptx)",
        type=config.ALLOWED_PPTX_EXTENSIONS,
        accept_multiple_files=True,
        key="reference_files"
    )
    
    if uploaded_files:
        st.success(f"📁 {len(uploaded_files)} file(s) uploaded")
        
        # Use the first file as the primary reference
        if st.button("Load Reference Template", type="primary"):
            with st.spinner("Loading reference template..."):
                try:
                    # Load the first uploaded file as reference
                    st.session_state.pptx_handler.load_reference(uploaded_files[0])
                    st.session_state.reference_loaded = True
                    
                    # Display available layouts
                    layouts = st.session_state.pptx_handler.get_slide_layouts_info()
                    st.success("✅ Reference template loaded successfully!")
                    
                    st.subheader("Available Slide Layouts:")
                    for idx, layout in enumerate(layouts):
                        st.write(f"{idx}: {layout}")
                    
                except Exception as e:
                    st.error(f"❌ Error loading reference: {str(e)}")
    
    if st.session_state.reference_loaded:
        st.info("✅ Reference template is loaded and ready to use")


def upload_images():
    """Handle image uploads and placement."""
    st.header("Upload Images")
    st.markdown("""
    Upload images that will be included in your report.
    Specify which slide each image should appear on and where it should be positioned.
    """)
    
    if not st.session_state.reference_loaded:
        st.warning("⚠️ Please upload and load a reference template first (Tab 1)")
        return
    
    uploaded_images = st.file_uploader(
        "Choose image files",
        type=config.ALLOWED_IMAGE_EXTENSIONS,
        accept_multiple_files=True,
        key="image_files"
    )
    
    if uploaded_images:
        st.subheader("Configure Image Placement")
        
        for idx, img_file in enumerate(uploaded_images):
            st.markdown(f"### Image {idx + 1}: {img_file.name}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                slide_index = st.number_input(
                    "Slide number",
                    min_value=0,
                    max_value=config.MAX_SLIDES_PER_REPORT,
                    value=0,
                    key=f"slide_idx_{idx}"
                )
            
            with col2:
                position = st.selectbox(
                    "Position",
                    options=config.IMAGE_POSITIONS,
                    key=f"position_{idx}"
                )
            
            with col3:
                width = st.slider(
                    "Width (inches)",
                    min_value=config.MIN_IMAGE_WIDTH,
                    max_value=config.MAX_IMAGE_WIDTH,
                    value=config.DEFAULT_IMAGE_WIDTH,
                    step=0.5,
                    key=f"width_{idx}"
                )
            
            st.divider()
        
        if st.button("Save Image Configurations", type="primary"):
            st.session_state.image_handler.clear_images()
            
            # Validate and add images
            invalid_images = []
            for idx, img_file in enumerate(uploaded_images):
                slide_idx = st.session_state[f"slide_idx_{idx}"]
                position = st.session_state[f"position_{idx}"]
                width = st.session_state[f"width_{idx}"]
                
                # Reset file pointer and validate
                img_file.seek(0)
                if not st.session_state.image_handler.validate_image(img_file):
                    invalid_images.append(img_file.name)
                    continue
                
                # Reset file pointer again after validation
                img_file.seek(0)
                st.session_state.image_handler.add_image(
                    img_file,
                    slide_idx,
                    position,
                    width
                )
            
            if invalid_images:
                st.warning(f"⚠️ Skipped invalid image(s): {', '.join(invalid_images)}")
            
            valid_count = len(uploaded_images) - len(invalid_images)
            if valid_count > 0:
                st.success(f"✅ Configured {valid_count} valid image(s)")
            else:
                st.error("❌ No valid images to configure")


def create_content():
    """Handle content creation for slides."""
    st.header("Create Report Content")
    st.markdown("""
    Enter draft content for your report. The AI will refine it into professional language.
    """)
    
    if not st.session_state.reference_loaded:
        st.warning("⚠️ Please upload and load a reference template first (Tab 1)")
        return
    
    # Get available layouts
    layouts = st.session_state.pptx_handler.get_slide_layouts_info()
    
    st.subheader("Number of Slides")
    num_slides = st.number_input(
        "How many slides do you want to create?",
        min_value=1,
        max_value=config.MAX_SLIDES_PER_REPORT,
        value=config.DEFAULT_NUM_SLIDES,
        key="num_slides"
    )
    
    # Create input fields for each slide
    slides_data = []
    
    for i in range(num_slides):
        with st.expander(f"📄 Slide {i + 1}", expanded=(i == 0)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                title = st.text_input(
                    "Slide Title (draft)",
                    key=f"title_{i}",
                    placeholder="Enter draft title..."
                )
            
            with col2:
                layout = st.selectbox(
                    "Layout",
                    options=list(range(len(layouts))),
                    format_func=lambda x: f"{x}: {layouts[x]}",
                    key=f"layout_{i}"
                )
            
            content = st.text_area(
                "Slide Content (draft)",
                key=f"content_{i}",
                height=150,
                placeholder="Enter draft content... AI will refine this into professional language."
            )
            
            slides_data.append({
                'title': title,
                'content': content,
                'layout': layout
            })
    
    # Store in session state
    st.session_state.slides_data = slides_data
    
    if any(slide['title'] or slide['content'] for slide in slides_data):
        st.success(f"✅ Content prepared for {num_slides} slide(s)")


def generate_report():
    """Generate the final report."""
    st.header("Generate Your Report")
    
    if not st.session_state.reference_loaded:
        st.error("❌ Please upload and load a reference template first (Tab 1)")
        return
    
    if not st.session_state.slides_data:
        st.warning("⚠️ Please create content for your report first (Tab 3)")
        return
    
    # Display summary
    st.subheader("Report Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Number of Slides", len(st.session_state.slides_data))
    
    with col2:
        st.metric("Number of Images", len(st.session_state.image_handler.get_all_images()))
    
    # Option to refine with AI
    use_ai_refinement = st.checkbox(
        "Refine content with AI",
        value=True,
        help="Use OpenAI to refine draft text into professional language"
    )
    
    if st.button("🎯 Generate Report", type="primary"):
        try:
            with st.spinner("Generating your report..."):
                # Prepare slides data
                slides_data = st.session_state.slides_data
                
                # Refine content if requested and API key is available
                if use_ai_refinement and os.getenv('OPENAI_API_KEY'):
                    st.info("🤖 Refining content with AI...")
                    try:
                        llm_refiner = LLMRefiner()
                        slides_data = llm_refiner.refine_all_slides(slides_data)
                        st.success("✅ Content refined successfully")
                    except Exception as e:
                        st.warning(f"⚠️ AI refinement failed: {str(e)}. Using original content.")
                
                # Get images data
                images_data = st.session_state.image_handler.get_all_images()
                
                # Generate the presentation
                st.info("📊 Creating PowerPoint presentation...")
                output = st.session_state.pptx_handler.create_report_from_template(
                    slides_data,
                    images_data if images_data else None
                )
                
                st.success("✅ Report generated successfully!")
                
                # Provide download button
                st.download_button(
                    label="📥 Download Report",
                    data=output,
                    file_name="weekly_report.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
                
                # Show preview of refined content
                if use_ai_refinement and os.getenv('OPENAI_API_KEY'):
                    with st.expander("View Refined Content"):
                        for idx, slide in enumerate(slides_data):
                            st.markdown(f"**Slide {idx + 1}: {slide['title']}**")
                            st.write(slide['content'])
                            st.divider()
        
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            st.exception(e)


if __name__ == "__main__":
    main()
