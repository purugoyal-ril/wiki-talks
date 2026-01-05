"""
Core business logic for The Synthetic Radio Host - Wiki-talks
Contains WikiScraper, ScriptGenerator, and AudioEngine classes
"""

import json
import re
import requests
from google import genai
import wikipediaapi  # Package: wikipedia-api (install via: pip install wikipedia-api)
from typing import List, Dict, Optional, Tuple
import config


class WikiScraper:
    """Handles Wikipedia content extraction with error handling"""
    
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='wiki-talks/1.0 (https://github.com/purugoyal-ril/wiki-talks)',
            language='en'
        )
    
    def scrape(self, url: str, mode: str = "fast") -> Tuple[Optional[str], Optional[str]]:
        """
        Scrape Wikipedia content from URL
        
        Args:
            url: Wikipedia article URL
            mode: "fast" (summary only) or "pro" (sections, capped at 4000 words)
        
        Returns:
            Tuple of (content, error_message). content is None if error occurred.
        """
        try:
            # Extract page title from URL
            page_title = self._extract_title_from_url(url)
            if not page_title:
                return None, "Invalid Wikipedia URL format"
            
            # Get page
            page = self.wiki.page(page_title)
            
            # Check if page exists
            if not page.exists():
                return None, f"Wikipedia page '{page_title}' not found"
            
            # Handle disambiguation
            if 'disambiguation' in page.title.lower():
                # Auto-select first option
                if page.links:
                    first_link = list(page.links.keys())[0]
                    page = self.wiki.page(first_link)
                    if not page.exists():
                        return None, f"Could not access disambiguation option: {first_link}"
            
            # Extract content based on mode
            if mode.lower() == "fast":
                content = page.summary
            else:  # pro mode
                content = self._extract_sections(page, max_words=4000)
            
            if not content or len(content.strip()) < 50:
                return None, "Page content too short or empty"
            
            return content, None
            
        except Exception as e:
            # Handle disambiguation and page errors generically
            # Note: wikipediaapi doesn't have an exceptions module, so we catch all exceptions
            # and check error messages to determine the type
            error_str = str(e).lower()
            if 'disambiguation' in error_str or 'ambiguous' in error_str:
                # Try to auto-select first option from links if we have a page object
                try:
                    # Try to get the page again to access links
                    page_title = self._extract_title_from_url(url)
                    if page_title:
                        page = self.wiki.page(page_title)
                        if hasattr(page, 'links') and page.links:
                            first_link = list(page.links.keys())[0]
                            selected_page = self.wiki.page(first_link)
                            if selected_page.exists():
                                content = selected_page.summary if mode.lower() == "fast" else self._extract_sections(selected_page, max_words=4000)
                                return content, None
                except Exception:
                    pass
                return None, f"Disambiguation error: {str(e)}"
            elif 'page' in error_str or 'not found' in error_str:
                return None, f"Page error: {str(e)}"
            else:
                return None, f"Error scraping Wikipedia: {str(e)}"
    
    def _extract_title_from_url(self, url: str) -> Optional[str]:
        """Extract page title from Wikipedia URL"""
        # Handle various URL formats
        patterns = [
            r'wikipedia\.org/wiki/([^?#]+)',
            r'wikipedia\.org/wiki/([^/?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                title = match.group(1)
                # URL decode
                title = title.replace('_', ' ')
                return title
        
        return None
    
    def _extract_sections(self, page, max_words: int = 4000) -> str:
        """Extract content from sections, capped at max_words"""
        content_parts = []
        word_count = 0
        
        # Add summary first
        if page.summary:
            words = page.summary.split()
            if word_count + len(words) <= max_words:
                content_parts.append(page.summary)
                word_count += len(words)
        
        # Add sections
        for section in page.sections:
            if word_count >= max_words:
                break
            
            section_title = section.title
            section_text = section.text
            words = section_text.split()
            
            if word_count + len(words) <= max_words:
                content_parts.append(f"\n\n## {section_title}\n\n{section_text}")
                word_count += len(words)
            else:
                # Add partial section
                remaining_words = max_words - word_count
                partial_text = ' '.join(words[:remaining_words])
                content_parts.append(f"\n\n## {section_title}\n\n{partial_text}")
                break
        
        return '\n'.join(content_parts)


class ScriptGenerator:
    """Generates Hinglish conversation scripts using Google Gemini"""
    
    def __init__(self, api_key: str):
        """
        Initialize ScriptGenerator with Gemini API key
        
        Args:
            api_key: Google Gemini API key
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'
        # Store generation config for use in generate_content
        self.generation_config = {
            "response_mime_type": "application/json",
            "temperature": 0.8
        }
    
    def generate_script(self, text: str, variant: str = "RJ", duration: int = 120) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Generate Hinglish conversation script from Wikipedia content
        
        Args:
            text: Wikipedia content text
            variant: "RJ", "Business", or "Teams"
            duration: Target duration in seconds (default 120 for 2 minutes)
        
        Returns:
            Tuple of (script_json, error_message). script_json is None if error occurred.
        """
        try:
            # Get variant-specific system prompt
            system_prompt = config.VARIANTS.get(variant, config.VARIANTS["RJ"])
            
            # Calculate target word count (~150 WPM for conversational)
            target_words = int((duration / 60) * 150)  # ~300 words for 2 minutes
            
            # Create user prompt
            user_prompt = f"""Convert the following Wikipedia content into a natural 2-minute Hinglish conversation between Host and Guest.

Target: Approximately {target_words} words total for ~{duration} seconds of conversation.

Content:
{text[:3000]}  # Limit input to avoid token limits

Requirements:
- Output strict JSON array format: [{{"speaker": "Host", "text": "..."}}, {{"speaker": "Guest", "text": "..."}}]
- Use natural Hinglish (Hindi-English mix)
- Include interruptions (end line with -, next starts with [fast])
- Use audio tags: [laughs], [sighs], [whispers], [clears throat], [gasps]
- Use ... for hesitation
- Use CAPS for emphasis
- Make it conversational and natural
- NO SSML tags
- NO markdown code fences in output"""
            
            # Generate script
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_prompt}\n\n{user_prompt}",
                config=self.generation_config
            )
            
            # Extract JSON from response
            script_text = response.text
            
            # Strip markdown code fences if present
            script_text = self._strip_markdown(script_text)
            
            # Parse JSON
            script_json = json.loads(script_text)
            
            # Validate structure
            if not isinstance(script_json, list):
                return None, "Script must be a JSON array"
            
            # Validate each entry
            for entry in script_json:
                if not isinstance(entry, dict):
                    return None, "Each script entry must be a dictionary"
                if "speaker" not in entry or "text" not in entry:
                    return None, "Each entry must have 'speaker' and 'text' fields"
                if entry["speaker"] not in ["Host", "Guest"]:
                    return None, f"Speaker must be 'Host' or 'Guest', got: {entry['speaker']}"
            
            return script_json, None
            
        except json.JSONDecodeError as e:
            return None, f"JSON parsing error: {str(e)}"
        except Exception as e:
            return None, f"Error generating script: {str(e)}"
    
    def _strip_markdown(self, text: str) -> str:
        """Strip markdown code fences from JSON response"""
        # Remove ```json and ``` markers
        text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'```$', '', text, flags=re.MULTILINE)
        return text.strip()


class AudioEngine:
    """Generates audio using ElevenLabs V3 Dialogue API"""
    
    def __init__(self):
        """Initialize AudioEngine"""
        pass
    
    def generate_dialogue_v3(self, script_json: List[Dict], api_key: str, base_url: Optional[str] = None) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Generate audio using ElevenLabs V3 text-to-dialogue endpoint
        
        Args:
            script_json: List of dicts with "speaker" and "text" keys
            api_key: ElevenLabs API key
            base_url: Optional custom base URL (defaults to config.ELEVENLABS_BASE_URL)
        
        Returns:
            Tuple of (audio_bytes, error_message). audio_bytes is None if error occurred.
        """
        try:
            # Use provided base_url or default from config
            url = base_url or config.ELEVENLABS_BASE_URL
            
            # Build dialogue_inputs array
            dialogue_inputs = []
            
            for line in script_json:
                speaker = line.get("speaker", "Host")
                text = line.get("text", "")
                
                # Look up voice_id from VOICE_CAST
                voice_id = config.VOICE_CAST.get(speaker)
                if not voice_id:
                    return None, f"Voice ID not found for speaker: {speaker}"
                
                dialogue_inputs.append({
                    "text": text,
                    "voice_id": voice_id
                })
            
            # Prepare API request
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            body = {
                "inputs": dialogue_inputs,
                "model_id": config.MODEL_ID
            }
            
            # Make API call
            response = requests.post(url, json=body, headers=headers, timeout=120)
            
            # Check response
            if response.status_code != 200:
                error_msg = f"ElevenLabs API error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text[:200]}"
                return None, error_msg
            
            # Return binary audio content
            audio_bytes = response.content
            return audio_bytes, None
            
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Error generating audio: {str(e)}"

