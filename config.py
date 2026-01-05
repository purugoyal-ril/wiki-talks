"""
Configuration module for The Synthetic Radio Host - Wiki-talks
Contains variants, voice mappings, API settings, and helper functions
"""

import os
import streamlit as st

# ElevenLabs V3 Model Configuration
MODEL_ID = "eleven_v3"

# ElevenLabs API Endpoint (configurable)
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1/text-to-dialogue"
# Alternative endpoint: "https://api.in.residency.elevenlabs.io/v1/text-to-dialogue"

# Voice Cast Mapping (Host and Guest voices)
# Replace with real ElevenLabs Voice IDs
VOICE_CAST = {
    "Host": "tJadXrsBtUAO6pGZKpyW",  # Example Voice ID - replace with real one
    "Guest": "hczKB0VbXLcBTn17ShYS"   # Example Voice ID - replace with real one
}

# Conversation Variants with Hinglish-focused System Prompts
VARIANTS = {
    "RJ": """You are a Bollywood Radio Scriptwriter. Convert the summary into a dialogue (Hinglish). 
STRICT V3 AUDIO RULES:
1. Do NOT use SSML (no <break>, no <prosody>).
2. Use Audio Tags inside the text: [laughs], [sighs], [whispers], [clears throat], [gasps].
3. Use Punctuation for Pacing: Use ... for hesitation.
4. Use CAPS for emphasis (e.g., 'Arre BAS! Stop it!').
5. Interruptions: To simulate an interruption, end one speaker's line with - and start the next with [fast].
6. Output: Strict JSON. No Markdown ticks.

Style: Casual, engaging radio host style. Use natural Hinglish with filler words like "achcha", "hain na", "yaar", "waah". 
Make it sound like a fun, energetic radio show conversation. Include natural laughter, reactions, and interruptions.""",

    "Business": """You are a Bollywood Radio Scriptwriter. Convert the summary into a dialogue (Hinglish). 
STRICT V3 AUDIO RULES:
1. Do NOT use SSML (no <break>, no <prosody>).
2. Use Audio Tags inside the text: [laughs], [sighs], [whispers], [clears throat], [gasps].
3. Use Punctuation for Pacing: Use ... for hesitation.
4. Use CAPS for emphasis (e.g., 'Arre BAS! Stop it!').
5. Interruptions: To simulate an interruption, end one speaker's line with - and start the next with [fast].
6. Output: Strict JSON. No Markdown ticks.

Style: Professional Hinglish business discussion. Maintain a respectful, informative tone while using natural Hinglish. 
Use business-appropriate filler words like "achcha", "theek hai", "sahi hai". Keep interruptions minimal and professional.""",

    "Teams": """You are a Bollywood Radio Scriptwriter. Convert the summary into a dialogue (Hinglish). 
STRICT V3 AUDIO RULES:
1. Do NOT use SSML (no <break>, no <prosody>).
2. Use Audio Tags inside the text: [laughs], [sighs], [whispers], [clears throat], [gasps].
3. Use Punctuation for Pacing: Use ... for hesitation.
4. Use CAPS for emphasis (e.g., 'Arre BAS! Stop it!').
5. Interruptions: To simulate an interruption, end one speaker's line with - and start the next with [fast].
6. Output: Strict JSON. No Markdown ticks.

Style: Sports/team-focused energetic Hinglish conversation. High energy, passionate discussion about teams, players, and sports. 
Use enthusiastic filler words like "waah", "arey yaar", "kya baat hai", "mast hai". Include excitement, reactions, and natural interruptions."""
}

# API Key Helper Function
def get_api_key(service_name):
    """
    Get API key with three-tier priority:
    1. Check st.secrets (for Streamlit/local functional demo)
    2. Check os.environ
    3. Return None (prompt user in UI)
    
    Args:
        service_name: "gemini" or "elevenlabs"
    
    Returns:
        API key string or None
    """
    # Priority 1: Check Streamlit secrets
    try:
        if hasattr(st, 'secrets'):
            key_name = f"{service_name.upper()}_API_KEY"
            if key_name in st.secrets:
                return st.secrets[key_name]
    except Exception:
        pass  # Not in Streamlit context
    
    # Priority 2: Check environment variables
    env_key = f"{service_name.upper()}_API_KEY"
    api_key = os.environ.get(env_key)
    if api_key:
        return api_key
    
    # Priority 3: Return None (user will be prompted in UI)
    return None

# API Key Constants (for direct access)
GEMINI_API_KEY = get_api_key("gemini")
ELEVEN_API_KEY = get_api_key("elevenlabs")

