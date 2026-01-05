# The Synthetic Radio Host - Wiki-talks 🎙️

Generate natural-sounding Hinglish radio conversations from Wikipedia articles using Google Gemini and ElevenLabs V3 Dialogue API.

## Overview

The Synthetic Radio Host - Wiki-talks is a Python pipeline that:
1. Scrapes content from Wikipedia articles
2. Generates natural Hinglish conversation scripts using Google Gemini
3. Converts scripts to audio using ElevenLabs V3 text-to-dialogue endpoint

**Project for**: Winter 30 Hackathon

## Features

- 🎙️ Natural Hinglish conversations with interruptions and filler words
- 🎭 Three conversation styles: RJ, Business, Teams
- ⚡ Fast mode (summary) or Pro mode (detailed sections)
- 🎵 ElevenLabs V3 Dialogue API for natural conversation flow
- 📱 Streamlit UI for local testing
- 🔧 Standalone Colab submission script

## Quick Start

### Installation

**Recommended: Use a virtual environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Without virtual environment (not recommended):**
```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Streamlit UI (Local Testing)

```bash
streamlit run app.py
```

1. Enter API keys in the sidebar (or set in `.streamlit/secrets.toml`)
2. Enter a Wikipedia URL
3. Select conversation style and mode
4. Click "Generate Broadcast"

#### Option 2: Local Runner Script

```bash
python run_local.py --url "https://en.wikipedia.org/wiki/Mumbai_Indians" --variant RJ --mode fast
```

Or set environment variables and run:
```bash
export GEMINI_API_KEY="your_key"
export ELEVEN_API_KEY="your_key"
python run_local.py
```

#### Option 3: Colab Submission Script

1. Upload `colab_submission.py` and `core_logic.py` to Google Colab
2. Set API keys in Colab secrets:
   - `GEMINI_API_KEY`
   - `ELEVEN_API_KEY`
3. Run the cells in order

**Note**: `colab_submission.py` also works locally if you set environment variables!

#### Option 4: Python Script (Direct API)

```python
from core_logic import WikiScraper, ScriptGenerator, AudioEngine

# Scrape Wikipedia
scraper = WikiScraper()
content, error = scraper.scrape("https://en.wikipedia.org/wiki/Mumbai_Indians", "fast")

# Generate script
script_gen = ScriptGenerator("your_gemini_api_key")
script_json, error = script_gen.generate_script(content, variant="RJ", duration=120)

# Generate audio
audio_engine = AudioEngine()
audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "your_elevenlabs_api_key")

# Save audio
with open("output.mp3", "wb") as f:
    f.write(audio_bytes)
```

## Setup

For detailed setup instructions including virtual environment setup, see [SETUP.md](SETUP.md).

## Configuration

### API Keys

Set API keys via:
1. **Streamlit secrets** (`.streamlit/secrets.toml`):
   ```toml
   GEMINI_API_KEY = "your_key"
   ELEVEN_API_KEY = "your_key"
   ```

2. **Environment variables**:
   ```bash
   export GEMINI_API_KEY="your_key"
   export ELEVEN_API_KEY="your_key"
   ```

3. **Colab secrets**: Runtime > Manage secrets

### Voice Configuration

Edit `config.py` to set ElevenLabs Voice IDs:

```python
VOICE_CAST = {
    "Host": "your_host_voice_id",
    "Guest": "your_guest_voice_id"
}
```

### ElevenLabs Endpoint

Default: `https://api.elevenlabs.io/v1/text-to-dialogue`

Alternative: `https://api.in.residency.elevenlabs.io/v1/text-to-dialogue`

## Project Structure

```
wiki-talks/
├── colab_submission.py    # Main Colab submission script
├── core_logic.py          # Core business logic (WikiScraper, ScriptGenerator, AudioEngine)
├── config.py              # Configuration and variants
├── app.py                 # Streamlit UI
├── requirements.txt       # Python dependencies
├── PROJECT_GOALS.md       # Master goals document
├── TECHNICAL_DESIGN.md    # Technical documentation
├── HINGLISH_PROMPTING.md  # Hinglish prompting explanation
├── tests/                 # Unit tests
│   ├── test_wikiscraper.py
│   ├── test_scriptgenerator.py
│   └── test_audioengine.py
└── samples/               # Sample outputs
    └── sample_output.mp3
```

## Running Tests

```bash
pytest tests/
```

## Variants

- **RJ**: Casual, engaging radio host style with natural Hinglish
- **Business**: Professional Hinglish business discussion
- **Teams**: Sports/team-focused energetic Hinglish conversation

## Requirements

- Python 3.8+
- Google Gemini API key
- ElevenLabs API key
- See `requirements.txt` for dependencies

## Evaluation Criteria Compliance

✅ Python Script (colab_submission.py)  
✅ MP3 sample  
✅ 100-word Hinglish prompting explanation  
✅ Technical design document  
✅ Unit tests  
✅ Documentation  

## License

This project is part of the Winter 30 Hackathon submission.

## Contributing

This is a hackathon submission. For questions or issues, please refer to the project documentation.

