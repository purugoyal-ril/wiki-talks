---
name: wiki-talks - V3 Dialogue API
overview: Build a complete Python pipeline for "Winter 30" Hackathon using ElevenLabs V3 text-to-dialogue endpoint. The main deliverable is colab_submission.py - a standalone Colab-compatible script. V3 API handles conversation flow automatically, eliminating pydub stitching. Includes comprehensive documentation, unit tests, and evaluation criteria compliance.
todos:
  - id: create-goals
    content: Create PROJECT_GOALS.md with project objectives, tech stack (V3 API), constraints, evaluation criteria checklist, and success criteria
    status: completed
  - id: create-requirements
    content: "Create requirements.txt with Python dependencies (google-generativeai, wikipedia-api, requests, pytest, streamlit) - NOTE: NO pydub"
    status: completed
  - id: implement-config
    content: Implement config.py with VARIANTS dict, MODEL_ID="eleven_v3", ELEVENLABS_BASE_URL (configurable endpoint), VOICE_CAST dict (Host/Guest with example Voice IDs), get_api_key() helper, GEMINI_API_KEY and ELEVEN_API_KEY constants
    status: completed
  - id: implement-wikiscraper
    content: Implement WikiScraper class in core_logic.py with DisambiguationError/PageError handling, Fast mode (summary), Pro mode (sections capped at 4000 words)
    status: completed
    dependencies:
      - implement-config
  - id: implement-scriptgenerator
    content: Implement ScriptGenerator class in core_logic.py using Gemini 1.5 Flash with JSON response, STRICT V3 system prompt (no SSML, audio tags, CAPS, interruptions with - and [fast]), markdown stripping, generate_script() method with duration parameter
    status: completed
    dependencies:
      - implement-config
  - id: implement-audioengine
    content: "Implement AudioEngine class in core_logic.py with generate_dialogue_v3() method: build dialogue_inputs array from script_json using VOICE_CAST mapping, call ElevenLabs V3 text-to-dialogue endpoint (configurable base_url), return binary MP3 audio content"
    status: completed
    dependencies:
      - implement-config
  - id: implement-colab-submission
    content: Create colab_submission.py as MAIN STANDALONE submission file - complete pipeline that imports core_logic, uses google.colab.userdata for API keys, includes example usage, generates 2-minute MP3 output using V3 API
    status: completed
    dependencies:
      - implement-wikiscraper
      - implement-scriptgenerator
      - implement-audioengine
  - id: implement-streamlit-ui
    content: Implement app.py with sidebar (API key inputs with st.secrets check, URL, mode, variant selectors), main page (generate button, progress bar, script JSON display, audio player, cost stats)
    status: completed
    dependencies:
      - implement-wikiscraper
      - implement-scriptgenerator
      - implement-audioengine
  - id: create-technical-doc
    content: Create TECHNICAL_DESIGN.md with project overview, V3 Dialogue API architecture diagrams (Mermaid), setup/deployment instructions, code explanations, V3 vs previous approach comparison
    status: completed
    dependencies:
      - implement-colab-submission
  - id: create-hinglish-doc
    content: Create HINGLISH_PROMPTING.md with 100-word explanation of Hinglish prompting, V3 audio tag usage, interruption patterns, emphasis techniques
    status: completed
    dependencies:
      - implement-scriptgenerator
  - id: create-readme
    content: Create README.md with quick start guide, installation instructions, usage examples, GitHub repository information
    status: completed
    dependencies:
      - implement-colab-submission
  - id: create-unit-tests
    content: "Create comprehensive unit tests in tests/ directory: test_wikiscraper.py, test_scriptgenerator.py (with V3 tag validation), test_audioengine.py (V3 API structure) using pytest with mocked API calls"
    status: completed
    dependencies:
      - implement-wikiscraper
      - implement-scriptgenerator
      - implement-audioengine
  - id: generate-sample-mp3
    content: Generate sample_output.mp3 using colab_submission.py with a sample Wikipedia URL (e.g., Mumbai Indians) and save to samples/ directory
    status: pending
    dependencies:
      - implement-colab-submission
  - id: add-error-handling
    content: "Add comprehensive error handling: friendly errors for bad URLs, JSON parsing fallbacks (strip markdown), V3 API failures with retry logic, user-friendly error messages"
    status: completed
    dependencies:
      - implement-colab-submission
      - implement-streamlit-ui
---

# The Synthetic Radio Host - Wiki-talks - V3 Dialogue API Implementation Plan

## Architecture Overview

The application uses ElevenLabs V3 text-to-dialogue endpoint which handles the entire conversation flow automatically, eliminating the need for pydub stitching:

```javascript
┌─────────────────────────┐
│  colab_submission.py    │  MAIN SUBMISSION (Standalone Colab Script)
│  (Primary Deliverable)  │  ├── Uses google.colab.userdata for keys
│                         │  ├── Complete pipeline: Wiki → Script → Audio
│                         │  └── Generates 2-minute Hinglish conversation
└─────────────────────────┘
         │ (can import)
         ▼
┌─────────────────────────┐
│    core_logic.py        │  Reusable Business Logic
│    (Shared Library)     │  ├── WikiScraper
│                         │  ├── ScriptGenerator (Gemini + V3 Rules)
│                         │  └── AudioEngine (V3 Dialogue API)
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│      config.py          │  Configuration & Variants
│                         │  ├── VARIANTS (RJ, Business, Teams)
│                         │  ├── VOICE_CAST (Host/Guest mapping)
│                         │  └── Helper functions
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│       app.py            │  Streamlit UI (Optional - for local testing)
│    (Development Tool)   │
└─────────────────────────┘
```



## Key Changes from Previous Version

1. **ElevenLabs V3 Dialogue API**: Single API call handles entire conversation flow
2. **No pydub**: Removed pydub dependency and stitching logic
3. **Simplified Script Schema**: Only `{"speaker": "Host", "text": "..."}` (no emotion/interrupt fields)
4. **V3 Prompting Rules**: Strict rules for audio tags, punctuation, CAPS, interruptions
5. **Voice Mapping**: Uses "Host"/"Guest" names instead of A/B
6. **Model ID**: Changed to `"eleven_v3"`

## File Structure

```javascript
wiki-talks/
├── colab_submission.py       # MAIN SUBMISSION - Standalone Colab script
├── core_logic.py             # Reusable business logic classes
├── config.py                 # Configuration, variants, VOICE_CAST
├── app.py                    # Streamlit UI (optional, for testing)
├── requirements.txt          # Python dependencies (NO pydub)
├── PROJECT_GOALS.md          # Master goals + Evaluation criteria
├── TECHNICAL_DESIGN.md       # Technical design document (required)
├── HINGLISH_PROMPTING.md     # 100-word explanation of Hinglish prompting
├── tests/
│   ├── test_wikiscraper.py
│   ├── test_scriptgenerator.py
│   └── test_audioengine.py
├── samples/
│   └── sample_output.mp3     # Sample MP3 deliverable
└── README.md                 # Setup, deployment, usage instructions
```



## Evaluation Criteria Compliance

All requirements from the evaluation criteria are incorporated:

1. **Project Completion**: Fully functional by Jan 5, 2026
2. **Documentation**: TECHNICAL_DESIGN.md with architecture diagrams
3. **Demo Video**: YouTube link (to be provided)
4. **GitHub Submission**: All code in repository
5. **Unit Tests**: Comprehensive test coverage in `tests/` directory
6. **Deliverables**:

- Python Script (colab_submission.py - Colab link)
- MP3 sample (samples/sample_output.mp3)
- 100-word Hinglish prompting explanation (HINGLISH_PROMPTING.md)

## Implementation Details

### 1. PROJECT_GOALS.md (Master Document)

- **Purpose**: Maintain project vision, prevent scope creep, track evaluation criteria
- **Contents**:
- Project objectives (2-minute Hinglish conversation from Wikipedia)
- Tech stack requirements (Gemini, ElevenLabs V3, wikipedia-api, requests)
- Key constraints (conversational audio, V3 audio tags, interruptions)
- Evaluation criteria checklist
- Success criteria (natural-sounding, non-robotic audio via V3 API)

### 2. colab_submission.py (MAIN SUBMISSION FILE)

- **Standalone script** that can run entirely in Google Colab
- **Structure**:
  ```python
                # Cell 1: Install dependencies
                # Cell 2: Import libraries
                # Cell 3: Configuration (or import from config.py if uploaded)
                # Cell 4: Main pipeline function
                # Cell 5: Execution example
  ```




- **Features**:
- Uses `google.colab.userdata.get()` for API keys (Gemini, ElevenLabs)
- Complete pipeline: Wikipedia URL → Scraped content → Script generation → V3 Dialogue audio
- Generates exactly 2-minute conversation (script length calculation)
- Outputs MP3 file (binary from V3 API)
- Can import from `core_logic.py` OR include all logic inline (prefer import for maintainability)
- Includes example usage with sample Wikipedia URL

### 3. config.py

- **VARIANTS dict**: Three variants with Hinglish-focused system prompts:
- `RJ`: Casual, engaging radio host style with natural Hinglish
- `Business`: Professional Hinglish business discussion
- `Teams`: Sports/team-focused energetic Hinglish conversation
- **MODEL_ID**: `"eleven_v3"` (ElevenLabs V3 model)
- **ELEVENLABS_BASE_URL**: Configurable endpoint (default: `"https://api.elevenlabs.io/v1/text-to-dialogue"`, alternative: `"https://api.in.residency.elevenlabs.io/v1/text-to-dialogue"`)
- **VOICE_CAST dict**: Speaker name to Voice ID mapping:
- `"Host": "JBFqnCBsd6RMkjVDRZzb"` (example - use real Voice ID)
- `"Guest": "Aw4FAjKCGjjNkVhN1Xmq"` (example - use real Voice ID)
- **get_api_key(service_name)**: Three-tier priority (st.secrets → os.environ → None)
- **API Keys**: `GEMINI_API_KEY` and `ELEVEN_API_KEY` constants

### 4. core_logic.py (Reusable Business Logic)

#### WikiScraper class:

- Handles `DisambiguationError` (auto-selects first option)
- Handles `PageError` (returns None with error message)
- `scrape(url, mode)`: Fast mode (summary) vs Pro mode (sections, capped at 4000 words)
- Returns clean text for script generation

#### ScriptGenerator class:

- Uses `genai.GenerativeModel("gemini-1.5-flash")`
- `generation_config={"response_mime_type": "application/json"}`
- `generate_script(text, variant, duration=120)`: 
- Returns strict JSON list of dicts
- Each dict: `{"speaker": "Host", "text": "..."}` (simplified schema)
- **CRITICAL V3 System Prompt**:
    ```javascript
                                "You are a Bollywood Radio Scriptwriter. Convert the summary into a dialogue (Hinglish). 
                                STRICT V3 AUDIO RULES:
                                1. Do NOT use SSML (no <break>, no <prosody>).
                                2. Use Audio Tags inside the text: [laughs], [sighs], [whispers], [clears throat], [gasps].
                                3. Use Punctuation for Pacing: Use ... for hesitation.
                                4. Use CAPS for emphasis (e.g., 'Arre BAS! Stop it!').
                                5. Interruptions: To simulate an interruption, end one speaker's line with - and start the next with [fast].
                                6. Output: Strict JSON. No Markdown ticks."
    ```




- Strips markdown code fences (```json) before parsing
- Validates JSON structure
- Calculates script length to target ~2 minutes

#### AudioEngine class:

- `generate_dialogue_v3(script_json, api_key, base_url=None)`: 
- Initialize empty list `dialogue_inputs`
- Iterate `script_json` items
- Look up `voice_id` from `config.VOICE_CAST` based on speaker name ("Host" or "Guest")
- Append `{"text": line['text'], "voice_id": voice_id} `to `dialogue_inputs`
- **API Call**:
    - URL: `base_url` or `config.ELEVENLABS_BASE_URL` (default: `"https://api.elevenlabs.io/v1/text-to-dialogue"`, alternative: `"https://api.in.residency.elevenlabs.io/v1/text-to-dialogue"`)
    - Headers: `{"xi-api-key": api_key}`
    - Body: `{"inputs": dialogue_inputs, "model_id": "eleven_v3"}`
- Returns: Binary audio content (MP3) directly from API response
- Save to file if needed (for Colab/Streamlit display)

### 5. app.py (Streamlit UI - Optional)

- **Purpose**: Local testing and development tool
- **Sidebar**: 
- API key inputs (check st.secrets first, then show text_input if missing)
- Wikipedia URL input
- Mode selector (Fast/Pro)
- Variant selector (RJ/Business/Teams)
- **Main Page**: 
- "Generate Broadcast" button
- Progress bar showing stages (Scraping → Scripting → Audio Rendering)
- Display generated Script (JSON) in expandable section
- Audio Player (st.audio) for generated MP3
- Stats section: "Estimated Cost" (script length * ElevenLabs character pricing)

### 6. Documentation Files

- **TECHNICAL_DESIGN.md**:
- Project overview and track selection
- System architecture diagrams (Mermaid flowcharts)
- Setup and deployment instructions
- Code explanations and assumptions
- V3 Dialogue API integration details
- Comparison with previous approach (V3 vs individual TTS + stitching)
- **HINGLISH_PROMPTING.md**: 
- 100-word explanation of how LLM prompting achieves natural Hinglish
- V3 audio tag usage ([laughs], [sighs], etc.)
- Interruption patterns (ending with "-", starting with [fast])
- CAPS for emphasis, punctuation for pacing
- **README.md**:
- Quick start guide
- Installation instructions
- Usage examples
- GitHub repository link

### 7. Unit Tests (tests/)

- **test_wikiscraper.py**: Test disambiguation handling, page errors, content extraction
- **test_scriptgenerator.py**: Test JSON generation, Hinglish output, V3 audio tag validation
- **test_audioengine.py**: Test V3 API call structure, voice mapping, binary audio handling
- Use pytest framework
- Mock API calls to avoid costs during testing

### 8. requirements.txt

- google-generativeai
- wikipedia-api
- requests (for ElevenLabs API calls)
- pytest (for testing)
- streamlit (optional, for app.py)
- **NOTE**: pydub is NOT required (removed from dependencies)

## Key Implementation Notes

1. **V3 Audio Tag Rules**: ScriptGenerator must enforce:

- Audio tags: `[laughs]`, `[sighs]`, `[whispers]`, `[clears throat]`, `[gasps]`
- No SSML tags (`<break>`, `<prosody>` are forbidden)
- Punctuation: `...` for hesitation
- CAPS for emphasis: `"Arre BAS! Stop it!"`
- Interruptions: End line with `-`, next line starts with `[fast]`

2. **2-Minute Target**: ScriptGenerator calculates approximate duration based on:

- Average words per minute (~150 WPM for conversational)
- Account for interruptions and pauses
- Generate script with ~300-350 words total

3. **V3 Dialogue API Benefits**:

- Single API call handles entire conversation
- Automatic conversation flow and timing
- No manual audio stitching required
- Natural interruptions handled by API

4. **Error Handling**: 

- Never crash on bad Wikipedia URLs
- Graceful API failures with retry logic
- JSON parsing fallbacks (strip markdown)
- User-friendly error messages

5. **Colab Compatibility**:

- All file paths use relative paths or temp directories
- Audio files saved to Colab's file system
- No hardcoded absolute paths
- Works with Colab's runtime environment

6. **Voice IDs**: 

- Use real ElevenLabs Voice IDs in VOICE_CAST
- Ensure Host and Guest have distinct, natural-sounding voices