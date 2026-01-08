"""
Configuration file for the report generator application.
"""

# LLM Configuration
# Supported providers: 'azure' (Azure OpenAI) or 'local' (local LLM with OpenAI API spec)
LLM_PROVIDER = "azure"  # Default provider
LLM_MODEL = "gpt-35-turbo"  # For Azure: deployment name, For local: model name
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1000

# Streamlit Configuration
APP_TITLE = "Weekly PowerPoint Report Generator"
APP_ICON = "📊"
PAGE_LAYOUT = "wide"

# Default slide dimensions (in inches)
DEFAULT_SLIDE_WIDTH = 10
DEFAULT_SLIDE_HEIGHT = 7.5

# Image configuration
DEFAULT_IMAGE_WIDTH = 4.0  # inches
MIN_IMAGE_WIDTH = 1.0
MAX_IMAGE_WIDTH = 8.0

# Slide configuration
MAX_SLIDES_PER_REPORT = 20
DEFAULT_NUM_SLIDES = 3

# LLM Refinement prompts
REFINEMENT_CONTEXT_TEMPLATE = "weekly project report"
SYSTEM_PROMPT = "You are a professional business writer who refines draft text into polished, formal content."

REFINEMENT_PROMPT_TEMPLATE = """You are a professional business writer. Please refine the following draft text into formal, professional content suitable for a {context}.

Requirements:
- Maintain all key information and facts
- Use formal business language
- Make it clear and concise
- Keep the same general structure and length
- Do not add information that isn't in the draft

Draft text:
{draft_text}

Refined text:"""

# File upload configuration
ALLOWED_PPTX_EXTENSIONS = ['pptx']
ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
MAX_FILE_SIZE_MB = 10

# Position presets for image placement
IMAGE_POSITIONS = [
    'center',
    'top-left',
    'top-right',
    'top-center',
    'bottom-left',
    'bottom-right',
    'bottom-center',
    'middle-left',
    'middle-right'
]

# Coordinates for each position (left, top) in inches
POSITION_COORDINATES = {
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
