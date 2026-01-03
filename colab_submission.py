"""
wiki-talks - Main Submission File for Google Colab
Winter 30 Hackathon

This is the standalone submission script that runs in Google Colab.
It imports core_logic and uses google.colab.userdata for API keys.
"""

# Cell 1: Install dependencies
# !pip install google-generativeai wikipedia-api requests

# Cell 2: Import libraries
import json
import os

# Try to import Colab userdata, fallback to environment variables for local testing
try:
    from google.colab import userdata
    IN_COLAB = True
except ImportError:
    IN_COLAB = False
    print("Note: Not running in Colab. Using environment variables for API keys.")

from core_logic import WikiScraper, ScriptGenerator, AudioEngine
import config

# Cell 3: Configuration and API Keys
def get_colab_api_keys():
    """Get API keys from Colab userdata or environment variables"""
    if IN_COLAB:
        try:
            gemini_key = userdata.get('GEMINI_API_KEY')
            eleven_key = userdata.get('ELEVEN_API_KEY')
            return gemini_key, eleven_key
        except Exception as e:
            print(f"Error getting API keys from Colab userdata: {e}")
            print("\nTo set API keys in Colab:")
            print("1. Go to: Runtime > Manage secrets")
            print("2. Add secrets: GEMINI_API_KEY and ELEVEN_API_KEY")
            return None, None
    else:
        # Local environment: use environment variables
        gemini_key = os.environ.get('GEMINI_API_KEY')
        eleven_key = os.environ.get('ELEVEN_API_KEY')
        
        if not gemini_key:
            print("⚠️  GEMINI_API_KEY not found in environment variables")
        if not eleven_key:
            print("⚠️  ELEVEN_API_KEY not found in environment variables")
        
        return gemini_key, eleven_key

# Cell 4: Main Pipeline Function
def generate_wiki_talk(wikipedia_url: str, variant: str = "RJ", mode: str = "fast", output_file: str = "wiki_talk_output.mp3"):
    """
    Complete pipeline: Wikipedia URL → Script → Audio
    
    Args:
        wikipedia_url: Full Wikipedia article URL
        variant: "RJ", "Business", or "Teams"
        mode: "fast" (summary) or "pro" (sections)
        output_file: Output MP3 filename
    
    Returns:
        Tuple of (success: bool, message: str, script_json: list, audio_path: str)
    """
    print("=" * 60)
    print("wiki-talks - Generating Hinglish Conversation")
    print("=" * 60)
    
    # Get API keys
    gemini_key, eleven_key = get_colab_api_keys()
    if not gemini_key:
        return False, "Gemini API key not found. Please set GEMINI_API_KEY in Colab secrets.", None, None
    if not eleven_key:
        return False, "ElevenLabs API key not found. Please set ELEVEN_API_KEY in Colab secrets.", None, None
    
    # Step 1: Scrape Wikipedia
    print("\n[1/3] Scraping Wikipedia...")
    scraper = WikiScraper()
    content, error = scraper.scrape(wikipedia_url, mode)
    if error:
        return False, f"Wikipedia scraping failed: {error}", None, None
    print(f"✓ Scraped {len(content)} characters from Wikipedia")
    
    # Step 2: Generate Script
    print("\n[2/3] Generating Hinglish conversation script...")
    script_gen = ScriptGenerator(gemini_key)
    script_json, error = script_gen.generate_script(content, variant, duration=120)
    if error:
        return False, f"Script generation failed: {error}", None, None
    print(f"✓ Generated script with {len(script_json)} dialogue entries")
    
    # Display script preview
    print("\nScript Preview:")
    for i, entry in enumerate(script_json[:3], 1):
        print(f"  {i}. {entry['speaker']}: {entry['text'][:80]}...")
    if len(script_json) > 3:
        print(f"  ... and {len(script_json) - 3} more entries")
    
    # Step 3: Generate Audio
    print("\n[3/3] Generating audio with ElevenLabs V3...")
    audio_engine = AudioEngine()
    audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, eleven_key)
    if error:
        return False, f"Audio generation failed: {error}", script_json, None
    print(f"✓ Generated audio ({len(audio_bytes)} bytes)")
    
    # Save audio file
    try:
        with open(output_file, 'wb') as f:
            f.write(audio_bytes)
        print(f"\n✓ Audio saved to: {output_file}")
        audio_path = os.path.abspath(output_file)
    except Exception as e:
        return False, f"Error saving audio file: {str(e)}", script_json, None
    
    print("\n" + "=" * 60)
    print("✓ Success! wiki-talks generation complete")
    print("=" * 60)
    
    return True, "Success", script_json, audio_path

# Cell 5: Example Usage
if __name__ == "__main__":
    # Example: Mumbai Indians Wikipedia article
    example_url = "https://en.wikipedia.org/wiki/Mumbai_Indians"
    
    print("wiki-talks - Example Run")
    print(f"URL: {example_url}")
    print(f"Variant: RJ")
    print(f"Mode: fast\n")
    
    success, message, script, audio_path = generate_wiki_talk(
        wikipedia_url=example_url,
        variant="RJ",
        mode="fast",
        output_file="mumbai_indians_talk.mp3"
    )
    
    if success:
        print(f"\n✓ Script JSON:")
        print(json.dumps(script, indent=2, ensure_ascii=False))
        print(f"\n✓ Audio file: {audio_path}")
        print("\nYou can play the audio file or download it from Colab.")
    else:
        print(f"\n✗ Error: {message}")

