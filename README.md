# Weekly PowerPoint Report Generator

A web application that generates weekly PowerPoint reports with consistent styling using reference templates and LLM-refined content.

## Features

- **Upload Multiple Reference Reports**: Use existing PowerPoint presentations as style references
- **Exact Style Preservation**: Maintains slide master, fonts, colors, and formatting from reference reports
- **LLM Content Refinement**: Automatically refines draft text into formal, professional content
- **Image Management**: Upload and specify placement of images in the new report
- **Web Interface**: Easy-to-use interface for uploading files and generating reports

## Requirements

- Python 3.8+
- OpenAI API key (for content refinement)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ntl93/report-gen.git
cd report-gen
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (typically http://localhost:8501)

3. Follow the steps in the web interface:
   - Upload reference PowerPoint reports
   - Upload images and specify their placement
   - Enter draft content for your new report
   - Click "Generate Report" to create your new weekly report

4. Download the generated report

## Project Structure

```
report-gen/
├── app.py                  # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── pptx_handler.py    # PowerPoint style extraction and application
│   ├── llm_refiner.py     # LLM text refinement
│   └── image_handler.py   # Image management
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## How It Works

1. **Style Extraction**: The app analyzes reference PowerPoint files to extract slide masters, theme colors, fonts, and layouts
2. **Content Refinement**: Draft text is sent to OpenAI's GPT model to be refined into formal, professional content
3. **Report Generation**: A new PowerPoint is created using the extracted styles and refined content
4. **Image Insertion**: Uploaded images are inserted at specified locations in the report

## Example

1. Upload 1-3 previous weekly reports as references
2. Upload team photos or charts as images
3. Enter draft content like: "This week we finished feature X, started working on Y"
4. The app generates a professional report with your company's style and refined text like: "During the current reporting period, the team successfully completed the implementation of Feature X and initiated development efforts on Feature Y."

## License

MIT License