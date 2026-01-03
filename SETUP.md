# wiki-talks - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API Keys:
  - Google Gemini API key
  - ElevenLabs API key

## Step-by-Step Setup

### 1. Clone or Navigate to Project Directory

```bash
cd wiki-talks
```

### 2. Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies from system Python
- Prevents conflicts with other projects
- Makes dependency management easier
- Best practice for Python development

**Create the virtual environment:**

```bash
# macOS/Linux
python3 -m venv venv

# Windows
python -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt when activated.

### 4. Upgrade pip (Optional but Recommended)

```bash
pip install --upgrade pip
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `google-generativeai` - For Gemini API
- `wikipedia-api` - For Wikipedia scraping
- `requests` - For ElevenLabs API calls
- `pytest` - For running tests
- `streamlit` - For local UI (optional)

### 6. Set Up API Keys

**Option A: Environment Variables (Recommended for local development)**

```bash
# macOS/Linux
export GEMINI_API_KEY="your_gemini_key_here"
export ELEVEN_API_KEY="your_elevenlabs_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_gemini_key_here
set ELEVEN_API_KEY=your_elevenlabs_key_here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_gemini_key_here"
$env:ELEVEN_API_KEY="your_elevenlabs_key_here"
```

**Option B: Streamlit Secrets (For Streamlit UI)**

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_key_here"
ELEVEN_API_KEY = "your_elevenlabs_key_here"
```

**Option C: Colab Secrets (For Google Colab)**

1. Go to Runtime > Manage secrets
2. Add `GEMINI_API_KEY` and `ELEVEN_API_KEY`

### 7. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.8+

# Check installed packages
pip list

# Run a quick test
python -c "import wikipediaapi; print('✓ wikipedia-api installed')"
python -c "import google.generativeai; print('✓ google-generativeai installed')"
```

### 8. Deactivate Virtual Environment (When Done)

```bash
deactivate
```

## Troubleshooting

### Virtual Environment Not Activating

**macOS/Linux:**
- Make sure you're using `source venv/bin/activate` (not `source ./venv/bin/activate`)
- Check that `venv` directory exists

**Windows:**
- If PowerShell execution policy blocks activation, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Package Installation Fails

- Make sure virtual environment is activated
- Try upgrading pip: `pip install --upgrade pip`
- Check internet connection
- Some packages may require system dependencies

### Import Errors

- Ensure virtual environment is activated
- Verify packages are installed: `pip list`
- Reinstall if needed: `pip install -r requirements.txt --force-reinstall`

## Next Steps

Once setup is complete, see [README.md](README.md) for usage instructions.

## Virtual Environment Best Practices

1. **Always activate** the virtual environment before working on the project
2. **Never commit** the `venv/` directory to git (already in `.gitignore`)
3. **Recreate** the virtual environment if you encounter dependency conflicts
4. **Use** `requirements.txt` to share dependencies with others
5. **Update** `requirements.txt` if you add new dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

