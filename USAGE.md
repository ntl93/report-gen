# Usage Guide

## Quick Start

### 1. Setup

First, install dependencies and configure your API key:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Step-by-Step Guide

### Step 1: Upload Reference Reports

1. Click on the **"📁 Upload Reference Reports"** tab
2. Click **"Browse files"** and select one or more existing PowerPoint reports
3. Click **"Load Reference Template"** to extract the styling
4. The application will display available slide layouts

**What this does:**
- Extracts the slide master design
- Preserves theme colors and fonts
- Identifies available slide layouts you can use

### Step 2: Upload Images (Optional)

1. Click on the **"🖼️ Upload Images"** tab
2. Upload image files (PNG, JPG, JPEG)
3. For each image, specify:
   - **Slide number**: Which slide the image should appear on (0 = first slide)
   - **Position**: Where on the slide (center, top-left, etc.)
   - **Width**: How wide the image should be (in inches)
4. Click **"Save Image Configurations"**

**Position options:**
- center
- top-left, top-center, top-right
- middle-left, middle-right
- bottom-left, bottom-center, bottom-right

### Step 3: Create Content

1. Click on the **"✍️ Create Content"** tab
2. Specify how many slides you want to create
3. For each slide, enter:
   - **Title**: Draft title for the slide
   - **Content**: Draft content/bullet points
   - **Layout**: Choose from available layouts
4. Don't worry about making it perfect - the AI will refine it!

**Tips:**
- Write in casual, draft language
- Include all key points and data
- The AI will make it formal and professional

**Example Draft:**
```
Title: What we did this week
Content: Finished the login feature. Started working on the dashboard. Had some issues with the database but fixed them.
```

**AI-Refined Output:**
```
Title: Weekly Accomplishments
Content: Successfully completed implementation of the authentication system. Initiated development of the analytics dashboard. Resolved database performance issues through optimization.
```

### Step 4: Generate Report

1. Click on the **"🎯 Generate Report"** tab
2. Review the summary of your report
3. Check **"Refine content with AI"** if you want AI refinement (requires API key)
4. Click **"🎯 Generate Report"**
5. Wait for generation to complete
6. Click **"📥 Download Report"** to save your new PowerPoint file

## Example Workflows

### Weekly Status Report

```
Reference: Previous week's report
Images: Team photo, sprint burndown chart
Slides:
  1. Title: "Week 45 Status Report"
  2. Accomplishments: "Completed user auth, fixed 15 bugs, deployed to staging"
  3. Metrics: "80% sprint completion, 95% test coverage"
  4. Next Steps: "Start payment integration, plan Q4 features"
```

### Project Update

```
Reference: Monthly template
Images: Architecture diagram, screenshot of new feature
Slides:
  1. Title: "Project Alpha - November Update"
  2. Progress: "Backend API complete, frontend 60% done"
  3. Challenges: "Performance issues resolved, waiting on design approval"
  4. Timeline: "On track for December release"
```

## Troubleshooting

### "OpenAI API key not found"
- Make sure you've created a `.env` file
- Add your API key: `OPENAI_API_KEY=sk-...`
- Restart the application

### "No reference presentation loaded"
- Go to Tab 1 and upload a PowerPoint file
- Click "Load Reference Template"

### Images not appearing
- Check that slide numbers start from 0
- Verify image file format (PNG, JPG, JPEG only)
- Try adjusting position and width settings

### Generated report looks different from reference
- Make sure you're using layouts available in the reference
- The first uploaded file is used as the primary reference
- Some complex formatting may not transfer perfectly

## Advanced Features

### Using Different Layouts

Each PowerPoint template has multiple layouts. Common ones:
- Layout 0: Title Slide
- Layout 1: Title and Content
- Layout 2: Section Header
- Layout 5: Title Only
- Layout 6: Blank

Check Tab 1 after loading a reference to see available layouts.

### Customizing Image Placement

You can fine-tune image placement by:
1. Using different position presets
2. Adjusting the width slider
3. Adding multiple images to the same slide

### Batch Generation

To create multiple reports:
1. Keep the reference template loaded
2. Change only the content in Tab 3
3. Generate new reports without reloading the reference

## Tips for Best Results

1. **Use high-quality reference templates** - The better your reference, the better your output
2. **Be specific in draft content** - Include all facts, numbers, and details
3. **Consistent image sizes** - Use similar widths for professional appearance
4. **Review AI output** - Check the "View Refined Content" section before downloading
5. **Save your work** - Download generated reports immediately

## API Key Information

The application uses OpenAI's GPT-3.5-turbo model for content refinement.

**Approximate costs:**
- Per report generation: $0.001 - $0.01 (depending on content length)
- 100 reports: ~$0.10 - $1.00

**Getting an API key:**
1. Go to https://platform.openai.com/api-keys
2. Create an account or sign in
3. Click "Create new secret key"
4. Copy the key to your `.env` file

## Security Notes

- Never commit your `.env` file to version control
- The `.gitignore` file excludes it by default
- Keep your API key secret
- Generated reports are stored temporarily and should be downloaded immediately
