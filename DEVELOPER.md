# Developer Guide

## Project Structure

```
report-gen/
├── app.py                      # Main Streamlit application
├── config.py                   # Centralized configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
│
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── pptx_handler.py        # PowerPoint operations
│   ├── llm_refiner.py         # LLM text refinement
│   └── image_handler.py       # Image management
│
├── README.md                  # Main documentation
├── USAGE.md                   # User guide
├── DEVELOPER.md              # This file
│
└── tests/
    ├── test_basic.py          # Basic functionality tests
    ├── test_e2e.py            # End-to-end tests
    └── create_example_template.py  # Template generator
```

## Architecture

### Core Components

1. **app.py** - Streamlit Web Interface
   - Manages 4-tab workflow interface
   - Handles session state for persistence
   - Coordinates between all modules

2. **pptx_handler.py** - PowerPoint Operations
   - Loads reference presentations
   - Extracts slide layouts and themes
   - Creates new presentations with preserved styling
   - Adds images to slides

3. **llm_refiner.py** - AI Content Refinement
   - Integrates with OpenAI API
   - Refines draft text to professional language
   - Configurable prompts and parameters

4. **image_handler.py** - Image Management
   - Stores image upload metadata
   - Manages positioning information
   - Validates image files

5. **config.py** - Configuration
   - Centralized settings
   - Position coordinates
   - LLM prompts
   - UI parameters

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/ntl93/report-gen.git
cd report-gen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will open at http://localhost:8501
```

### Running Tests

```bash
# Run basic tests
python test_basic.py

# Run end-to-end tests
python test_e2e.py

# Create an example template
python create_example_template.py
```

## Code Style

- Follow PEP 8 style guide
- Use docstrings for all functions and classes
- Keep functions focused and small
- Use type hints where beneficial

## Key Design Decisions

### 1. Template Preservation

The app preserves template styling by:
- Loading the reference presentation as a base
- Copying slide layouts and theme
- Removing existing content while keeping structure

### 2. Session State Management

Streamlit session state is used to:
- Persist uploaded files across interactions
- Store configured images
- Maintain slide content between tabs

### 3. Configuration Externalization

All configurable values are in `config.py`:
- Makes customization easy
- Avoids magic numbers in code
- Enables easy testing with different settings

### 4. Error Handling

- Graceful degradation if API key is missing
- User-friendly error messages
- Falls back to original content if refinement fails

## Adding Features

### Adding a New Image Position

1. Add position name to `config.IMAGE_POSITIONS`
2. Add coordinates to `config.POSITION_COORDINATES`
3. The UI will automatically pick it up

### Changing LLM Model

1. Update `config.OPENAI_MODEL` (e.g., "gpt-4")
2. Adjust `config.OPENAI_TEMPERATURE` and `config.OPENAI_MAX_TOKENS` as needed

### Customizing Refinement Prompts

1. Edit `config.REFINEMENT_PROMPT_TEMPLATE`
2. Modify `config.SYSTEM_PROMPT`
3. Test with different content types

## Testing Strategy

### Unit Tests (test_basic.py)

- Tests individual module imports
- Tests basic functionality of each module
- Fast and focused

### Integration Tests (test_e2e.py)

- Tests complete workflow
- Creates actual PowerPoint files
- Verifies end-to-end functionality

### Manual Testing

1. Start the app with `streamlit run app.py`
2. Upload a real PowerPoint template
3. Add sample images
4. Create content and generate report
5. Download and verify the output file

## Common Development Tasks

### Debugging Streamlit App

```bash
# Run with verbose logging
streamlit run app.py --logger.level=debug
```

### Checking Dependencies

```bash
# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Update a specific package
pip install --upgrade package-name
```

### Code Quality Checks

```bash
# Check syntax
python -m py_compile app.py

# Format code (install black first)
pip install black
black app.py src/

# Lint code (install pylint first)
pip install pylint
pylint app.py src/
```

## API Reference

### PPTXHandler

```python
handler = PPTXHandler()
handler.load_reference(file)  # Load reference template
layouts = handler.get_slide_layouts_info()  # Get available layouts
output = handler.create_report_from_template(slides_data, images_data)
```

### LLMRefiner

```python
refiner = LLMRefiner(api_key="optional")
refined = refiner.refine_text(draft_text, context="report")
refined_slides = refiner.refine_all_slides(slides_data)
```

### ImageHandler

```python
handler = ImageHandler()
handler.add_image(file, slide_index, position, width)
images = handler.get_all_images()
handler.clear_images()
```

## Troubleshooting

### "ModuleNotFoundError"
- Ensure you're in the virtual environment
- Run `pip install -r requirements.txt`

### "OpenAI API Error"
- Check `.env` file exists and has valid API key
- Verify API key has credits available
- Check internet connection

### "Streamlit won't start"
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`

### PowerPoint styling not preserved
- Ensure reference file is a valid .pptx
- Some complex themes may not transfer perfectly
- Try using a simpler template

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## Security Considerations

- Never commit `.env` file with API keys
- API keys should be stored in environment variables
- Generated reports may contain sensitive information
- Consider adding authentication for production deployment

## Performance Optimization

- LLM API calls are the slowest part (1-3 seconds per slide)
- Consider caching refined content
- Batch API calls if implementing bulk generation
- Use streaming for large file uploads

## Future Enhancements

Potential areas for improvement:

1. **Multiple LLM Providers**
   - Add support for Anthropic Claude, Azure OpenAI
   - Make provider selectable in UI

2. **Template Gallery**
   - Pre-built templates users can choose from
   - Community-contributed templates

3. **Batch Processing**
   - Generate multiple reports at once
   - CSV/Excel input for data-driven slides

4. **Advanced Styling**
   - Chart/graph generation
   - Table formatting
   - Custom color schemes

5. **Collaboration Features**
   - Save/load draft reports
   - Template sharing
   - Version history

## License

MIT License - See LICENSE file for details
