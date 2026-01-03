"""
wiki-talks - Local Runner Script
Run this on your local machine without Colab

Usage:
    python run_local.py
"""

import json
import os
import sys
from core_logic import WikiScraper, ScriptGenerator, AudioEngine
import config


def get_api_keys():
    """Get API keys from environment variables or user input"""
    gemini_key = os.environ.get('GEMINI_API_KEY')
    eleven_key = os.environ.get('ELEVEN_API_KEY')
    
    if not gemini_key:
        gemini_key = input("Enter your Gemini API key: ").strip()
        if not gemini_key:
            print("❌ Gemini API key is required")
            sys.exit(1)
    
    if not eleven_key:
        eleven_key = input("Enter your ElevenLabs API key: ").strip()
        if not eleven_key:
            print("❌ ElevenLabs API key is required")
            sys.exit(1)
    
    return gemini_key, eleven_key


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
    gemini_key, eleven_key = get_api_keys()
    
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
        text_preview = entry['text'][:80] + "..." if len(entry['text']) > 80 else entry['text']
        print(f"  {i}. {entry['speaker']}: {text_preview}")
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


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="wiki-talks - Generate Hinglish conversations from Wikipedia")
    parser.add_argument(
        "--url",
        type=str,
        default="https://en.wikipedia.org/wiki/Mumbai_Indians",
        help="Wikipedia article URL"
    )
    parser.add_argument(
        "--variant",
        type=str,
        choices=["RJ", "Business", "Teams"],
        default="RJ",
        help="Conversation style variant"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["fast", "pro"],
        default="fast",
        help="Scraping mode: fast (summary) or pro (sections)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="wiki_talk_output.mp3",
        help="Output MP3 filename"
    )
    parser.add_argument(
        "--save-script",
        action="store_true",
        help="Save generated script JSON to file"
    )
    
    args = parser.parse_args()
    
    print("wiki-talks - Local Runner")
    print(f"URL: {args.url}")
    print(f"Variant: {args.variant}")
    print(f"Mode: {args.mode}\n")
    
    success, message, script, audio_path = generate_wiki_talk(
        wikipedia_url=args.url,
        variant=args.variant,
        mode=args.mode,
        output_file=args.output
    )
    
    if success:
        print(f"\n✓ Script JSON:")
        print(json.dumps(script, indent=2, ensure_ascii=False))
        print(f"\n✓ Audio file: {audio_path}")
        
        # Save script if requested
        if args.save_script:
            script_file = args.output.replace('.mp3', '_script.json')
            with open(script_file, 'w', encoding='utf-8') as f:
                json.dump(script, f, indent=2, ensure_ascii=False)
            print(f"✓ Script saved to: {script_file}")
        
        print("\nYou can play the audio file with any media player.")
    else:
        print(f"\n✗ Error: {message}")
        sys.exit(1)

