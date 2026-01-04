"""
wiki-talks - Streamlit UI for local testing and development
"""

import streamlit as st
import json
import os
from core_logic import WikiScraper, ScriptGenerator, AudioEngine
import config

# Page configuration
st.set_page_config(
    page_title="wiki-talks",
    page_icon="🎙️",
    layout="wide"
)

# Initialize session state
if 'script_json' not in st.session_state:
    st.session_state.script_json = None
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'wikipedia_content' not in st.session_state:
    st.session_state.wikipedia_content = None
if 'scrape_mode' not in st.session_state:
    st.session_state.scrape_mode = None

# Sidebar
with st.sidebar:
    st.title("wiki-talks 🎙️")
    st.markdown("Generate Hinglish radio conversations from Wikipedia articles")
    
    st.divider()
    
    # API Key Management
    st.subheader("API Keys")
    
    # Check for keys in secrets
    gemini_key = config.get_api_key("gemini")
    eleven_key = config.get_api_key("elevenlabs")
    
    if not gemini_key:
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key"
        )
    else:
        st.success("✓ Gemini API key found")
    
    if not eleven_key:
        eleven_key = st.text_input(
            "ElevenLabs API Key",
            type="password",
            help="Enter your ElevenLabs API key"
        )
    else:
        st.success("✓ ElevenLabs API key found")
    
    st.divider()
    
    # Input Configuration
    st.subheader("Configuration")
    
    wikipedia_url = st.text_input(
        "Wikipedia URL",
        value="https://en.wikipedia.org/wiki/Mumbai_Indians",
        help="Enter the full URL of a Wikipedia article"
    )
    
    variant = st.selectbox(
        "Conversation Style",
        options=["RJ", "Business", "Teams"],
        help="Select the conversation variant"
    )
    
    mode = st.selectbox(
        "Scraping Mode",
        options=["fast", "pro"],
        help="Fast: summary only | Pro: sections (capped at 4000 words)"
    )
    
    st.divider()
    
    # Advanced Options
    with st.expander("Advanced Options"):
        debug_mode = st.checkbox(
            "Debug Mode",
            help="Generate only 3 lines of script to save credits"
        )
        
        custom_endpoint = st.text_input(
            "Custom ElevenLabs Endpoint (optional)",
            value="",
            help="Leave empty to use default endpoint"
        )

# Main Page
st.title("wiki-talks")
st.markdown("**Generate natural Hinglish radio conversations from Wikipedia articles**")

# Generate Button
if st.button("🎙️ Generate Broadcast", type="primary", use_container_width=True):
    # Validate inputs
    if not gemini_key:
        st.error("❌ Please enter Gemini API key in the sidebar")
        st.stop()
    
    if not eleven_key:
        st.error("❌ Please enter ElevenLabs API key in the sidebar")
        st.stop()
    
    if not wikipedia_url:
        st.error("❌ Please enter a Wikipedia URL")
        st.stop()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Scrape Wikipedia
        status_text.text("📖 Scraping Wikipedia...")
        progress_bar.progress(10)
        
        scraper = WikiScraper()
        content, error = scraper.scrape(wikipedia_url, mode)
        
        if error:
            st.error(f"❌ Wikipedia scraping failed: {error}")
            st.stop()
        
        # Store in session state
        st.session_state.wikipedia_content = content
        st.session_state.scrape_mode = mode
        
        st.success(f"✓ Scraped {len(content)} characters from Wikipedia")
        progress_bar.progress(30)
        
        # Display Wikipedia content in expander
        with st.expander("📖 Step 1: Wikipedia Content", expanded=True):
            st.text_area("Scraped Content", content, height=200, disabled=True, key="wiki_content_display")
            st.caption(f"Mode: {mode} | Characters: {len(content):,}")
        
        # Step 2: Generate Script
        status_text.text("✍️ Generating Hinglish conversation script...")
        progress_bar.progress(40)
        
        script_gen = ScriptGenerator(gemini_key)
        
        # Debug mode: limit script length
        if debug_mode:
            # Modify prompt to generate only 3 lines
            original_generate = script_gen.generate_script
            def debug_generate(*args, **kwargs):
                script, err = original_generate(*args, **kwargs)
                if script and len(script) > 3:
                    script = script[:3]
                return script, err
            script_gen.generate_script = debug_generate
        
        script_json, error = script_gen.generate_script(content, variant, duration=120)
        
        if error:
            st.error(f"❌ Script generation failed: {error}")
            st.stop()
        
        st.session_state.script_json = script_json
        st.success(f"✓ Generated script with {len(script_json)} dialogue entries")
        progress_bar.progress(70)
        
        # Display generated script in expander
        with st.expander("✍️ Step 2: Generated Script", expanded=True):
            for i, entry in enumerate(script_json):
                speaker_icon = "🎙️" if entry['speaker'] == "Host" else "🗣️"
                st.markdown(f"**{speaker_icon} {entry['speaker']}:** {entry['text']}")
            st.caption(f"Total entries: {len(script_json)}")
        
        # Step 3: Generate Audio
        status_text.text("🎵 Generating audio with ElevenLabs V3...")
        progress_bar.progress(80)
        
        audio_engine = AudioEngine()
        base_url = custom_endpoint if custom_endpoint else None
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, eleven_key, base_url)
        
        if error:
            st.error(f"❌ Audio generation failed: {error}")
            st.stop()
        
        st.session_state.audio_bytes = audio_bytes
        st.success(f"✓ Generated audio ({len(audio_bytes)} bytes)")
        progress_bar.progress(100)
        status_text.text("✓ Complete!")
        
        # Display audio in expander
        with st.expander("🎵 Step 3: Generated Audio", expanded=True):
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="📥 Download MP3",
                data=audio_bytes,
                file_name="wiki_talk_output.mp3",
                mime="audio/mp3",
                key="download_audio_realtime"
            )
        
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.stop()

# Display Results (persistent view of all outputs)
if st.session_state.wikipedia_content or st.session_state.script_json or st.session_state.audio_bytes:
    st.divider()
    
    # Show Step 1 output if available
    if st.session_state.wikipedia_content:
        with st.expander("📖 Step 1: Wikipedia Content", expanded=False):
            st.text_area("Scraped Content", st.session_state.wikipedia_content, height=200, disabled=True, key="wiki_content_persistent")
            mode_display = st.session_state.scrape_mode or "unknown"
            st.caption(f"Mode: {mode_display} | Characters: {len(st.session_state.wikipedia_content):,}")
    
    # Show Step 2 output if available
    if st.session_state.script_json:
        with st.expander("✍️ Step 2: Generated Script", expanded=False):
            for i, entry in enumerate(st.session_state.script_json):
                speaker_icon = "🎙️" if entry['speaker'] == "Host" else "🗣️"
                st.markdown(f"**{speaker_icon} {entry['speaker']}:** {entry['text']}")
            st.caption(f"Total entries: {len(st.session_state.script_json)}")
    
    # Show Step 3 output if available
    if st.session_state.audio_bytes:
        with st.expander("🎵 Step 3: Generated Audio", expanded=False):
            st.audio(st.session_state.audio_bytes, format="audio/mp3")
            st.download_button(
                label="📥 Download MP3",
                data=st.session_state.audio_bytes,
                file_name="wiki_talk_output.mp3",
                mime="audio/mp3",
                key="download_audio_persistent"
            )
    
    # Stats Section (only if we have script)
    if st.session_state.script_json:
        st.divider()
        st.subheader("📊 Stats for Nerds")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_chars = sum(len(entry['text']) for entry in st.session_state.script_json)
            st.metric("Total Characters", f"{total_chars:,}")
        
        with col2:
            # Rough estimate: $0.30 per 1000 characters for ElevenLabs
            estimated_cost = (total_chars / 1000) * 0.30
            st.metric("Estimated Cost", f"${estimated_cost:.4f}")
        
        with col3:
            st.metric("Dialogue Entries", len(st.session_state.script_json))
        
        st.divider()
        
        # Script JSON Display
        with st.expander("📝 View Generated Script (JSON)"):
            st.json(st.session_state.script_json)
            
            # Copy button
            script_json_str = json.dumps(st.session_state.script_json, indent=2, ensure_ascii=False)
            st.code(script_json_str, language="json")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>wiki-talks | Winter 30 Hackathon</div>",
    unsafe_allow_html=True
)

