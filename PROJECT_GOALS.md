# wiki-talks - Project Goals & Master Document

## Project Overview

**Project Name**: wiki-talks  
**Hackathon**: Winter 30  
**Track**: AI/ML  
**Submission Deadline**: January 5, 2026

## Core Objective

Build a Python pipeline that takes a Wikipedia article (e.g., about "Mumbai Indians"), generates a natural-sounding 2-minute conversation script between two people in Hinglish (using Google Gemini LLM), and converts it into audio using ElevenLabs V3 text-to-dialogue API.

## Key Requirements

### Primary Deliverable
- **Main Submission**: `colab_submission.py` - A standalone, Colab-compatible Python script
- **Sample Output**: `samples/sample_output.mp3` - One MP3 sample demonstrating the pipeline
- **Hinglish Prompting Explanation**: `HINGLISH_PROMPTING.md` - 100-word explanation of LLM prompting strategy

### Technical Constraints
1. **Conversational Audio**: The audio must sound conversational with:
   - Natural interruptions
   - Filler words ("umm", "achcha")
   - Laughter and natural reactions
   - Cannot sound robotic

2. **V3 Dialogue API Requirements**:
   - Use ElevenLabs V3 text-to-dialogue endpoint
   - NO SSML tags (`<break>`, `<prosody>`)
   - Use audio tags: `[laughs]`, `[sighs]`, `[whispers]`, `[clears throat]`, `[gasps]`
   - Use punctuation for pacing (`...` for hesitation)
   - Use CAPS for emphasis
   - Interruptions: End line with `-`, next line starts with `[fast]`

3. **Wikipedia Integration**:
   - Handle DisambiguationError (auto-select first option)
   - Handle PageError gracefully
   - Support Fast mode (summary) and Pro mode (sections, capped at 4000 words)

## Tech Stack

### Core Technologies
- **Frontend/Interface**: Streamlit (for local testing)
- **LLM (Scripting)**: Google Gemini (`gemini-1.5-flash`)
- **Audio (TTS)**: ElevenLabs V3 (`eleven_v3` model)
- **Data Source**: `wikipedia-api` Python library
- **HTTP Client**: `requests` library

### Dependencies
- `google-generativeai` - Gemini API client
- `wikipedia-api` - Wikipedia content extraction
- `requests` - HTTP requests for ElevenLabs API
- `streamlit` - Optional UI for local testing
- `pytest` - Unit testing framework

**Note**: `pydub` is NOT required - ElevenLabs V3 Dialogue API handles all audio processing automatically.

## Architecture Principles

1. **Modularity**: Core logic separated into reusable classes (`core_logic.py`)
2. **Configuration**: Centralized config with variants and voice mappings (`config.py`)
3. **Standalone Submission**: `colab_submission.py` is the main deliverable (works independently)
4. **Error Handling**: Never crash on bad inputs - graceful error messages
5. **Colab Compatibility**: All paths relative, no hardcoded absolute paths

## Evaluation Criteria Compliance Checklist

### Required Deliverables
- [x] Python Script (colab_submission.py - Colab link)
- [ ] MP3 sample (samples/sample_output.mp3)
- [ ] 100-word Hinglish prompting explanation (HINGLISH_PROMPTING.md)

### Documentation Requirements
- [ ] Technical Design Document (TECHNICAL_DESIGN.md)
  - Project overview including track selection
  - System architecture diagrams (Mermaid flowcharts)
  - Setup and deployment instructions
  - Code explanations and assumptions
- [ ] README.md with setup instructions
- [ ] Demo Video (YouTube link - to be provided)

### Code Quality Requirements
- [ ] Comprehensive unit tests (tests/ directory)
- [ ] Clean, readable, maintainable code
- [ ] Proper error handling throughout
- [ ] GitHub repository with all code

### Evaluation Criteria
Projects will be evaluated based on:
1. **Innovation and Creativity**: Originality and uniqueness of the solution
2. **Technical Complexity**: Depth and sophistication of AI models and algorithms
3. **Code Quality**: Cleanliness, readability, and maintainability
4. **Testing and Reliability**: Coverage and effectiveness of unit tests
5. **Documentation**: Clarity and completeness of technical design document
6. **Demo Quality**: Effectiveness and clarity of the demo video

## Success Criteria

### Functional Requirements
- ✅ Pipeline successfully extracts Wikipedia content
- ✅ Generates natural Hinglish conversation script (~2 minutes)
- ✅ Produces conversational audio with interruptions and natural flow
- ✅ Works standalone in Google Colab
- ✅ Handles errors gracefully (bad URLs, API failures, etc.)

### Quality Requirements
- ✅ Audio sounds natural and conversational (not robotic)
- ✅ Hinglish code-switching is natural and appropriate
- ✅ Interruptions and filler words enhance realism
- ✅ Script length targets ~2 minutes accurately
- ✅ All variants (RJ, Business, Teams) work correctly

## Variants

The application supports three conversation styles:

1. **RJ**: Casual, engaging radio host style with natural Hinglish
2. **Business**: Professional Hinglish business discussion
3. **Teams**: Sports/team-focused energetic Hinglish conversation

## Voice Configuration

- **Host Voice**: Mapped via `VOICE_CAST["Host"]` in config.py
- **Guest Voice**: Mapped via `VOICE_CAST["Guest"]` in config.py
- Uses ElevenLabs Voice IDs (configurable)

## API Endpoints

- **ElevenLabs V3**: `https://api.elevenlabs.io/v1/text-to-dialogue` (default)
- **Alternative**: `https://api.in.residency.elevenlabs.io/v1/text-to-dialogue`

## Non-Negotiables

1. **No pydub**: V3 API handles all audio processing
2. **No SSML**: Strict V3 rules - only audio tags and punctuation
3. **Hinglish Required**: All scripts must be in Hinglish (Hindi-English mix)
4. **2-Minute Target**: Scripts must target approximately 2 minutes of audio
5. **Colab Compatible**: Main submission must work in Google Colab
6. **Error Handling**: Never crash - always show friendly error messages

## Project Timeline

- **Start**: Implementation begins
- **Milestone 1**: Core logic complete (WikiScraper, ScriptGenerator, AudioEngine)
- **Milestone 2**: Colab submission script complete
- **Milestone 3**: Documentation and tests complete
- **Final**: Sample MP3 generated, all deliverables ready
- **Deadline**: January 5, 2026

## Notes

- This document serves as the master reference to prevent scope creep
- All implementation decisions should align with these goals
- Evaluation criteria must be met for successful submission
- Focus on natural, conversational Hinglish output above all else

