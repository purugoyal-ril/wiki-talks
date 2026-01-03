"""
Unit tests for AudioEngine class
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core_logic import AudioEngine
import config


class TestAudioEngine:
    """Test cases for AudioEngine"""
    
    @patch('core_logic.requests.post')
    def test_generate_dialogue_v3_success(self, mock_post):
        """Test successful audio generation"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_mp3_content"
        mock_post.return_value = mock_response
        
        script_json = [
            {"speaker": "Host", "text": "Achcha, so Mumbai Indians..."},
            {"speaker": "Guest", "text": "Haan bhai, amazing team!"}
        ]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_api_key")
        
        assert error is None
        assert audio_bytes == b"fake_audio_mp3_content"
        
        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check URL
        assert call_args[0][0] == config.ELEVENLABS_BASE_URL
        
        # Check headers
        assert call_args[1]["headers"]["xi-api-key"] == "test_api_key"
        
        # Check body structure
        body = call_args[1]["json"]
        assert "inputs" in body
        assert "model_id" in body
        assert body["model_id"] == config.MODEL_ID
        assert len(body["inputs"]) == 2
    
    @patch('core_logic.requests.post')
    def test_voice_mapping(self, mock_post):
        """Test correct voice ID mapping"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"audio"
        mock_post.return_value = mock_response
        
        script_json = [
            {"speaker": "Host", "text": "Test"},
            {"speaker": "Guest", "text": "Test"}
        ]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key")
        
        assert error is None
        
        # Verify voice IDs in request
        call_args = mock_post.call_args
        body = call_args[1]["json"]
        
        assert body["inputs"][0]["voice_id"] == config.VOICE_CAST["Host"]
        assert body["inputs"][1]["voice_id"] == config.VOICE_CAST["Guest"]
    
    @patch('core_logic.requests.post')
    def test_custom_base_url(self, mock_post):
        """Test using custom base URL"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"audio"
        mock_post.return_value = mock_response
        
        custom_url = "https://api.in.residency.elevenlabs.io/v1/text-to-dialogue"
        script_json = [{"speaker": "Host", "text": "Test"}]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key", custom_url)
        
        assert error is None
        
        # Verify custom URL was used
        call_args = mock_post.call_args
        assert call_args[0][0] == custom_url
    
    @patch('core_logic.requests.post')
    def test_api_error_handling(self, mock_post):
        """Test handling of API errors"""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid request"}
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        script_json = [{"speaker": "Host", "text": "Test"}]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key")
        
        assert audio_bytes is None
        assert "ElevenLabs API error" in error
        assert "400" in error
    
    @patch('core_logic.requests.post')
    def test_invalid_speaker_handling(self, mock_post):
        """Test handling of invalid speaker names"""
        script_json = [
            {"speaker": "InvalidSpeaker", "text": "Test"}
        ]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key")
        
        assert audio_bytes is None
        assert "Voice ID not found" in error
    
    @patch('core_logic.requests.post')
    def test_network_error_handling(self, mock_post):
        """Test handling of network errors"""
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")
        
        script_json = [{"speaker": "Host", "text": "Test"}]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key")
        
        assert audio_bytes is None
        assert "Network error" in error
    
    @patch('core_logic.requests.post')
    def test_request_timeout(self, mock_post):
        """Test request timeout handling"""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Request timeout")
        
        script_json = [{"speaker": "Host", "text": "Test"}]
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key")
        
        assert audio_bytes is None
        assert "Network error" in error or "timeout" in error.lower()
    
    @patch('core_logic.requests.post')
    def test_empty_script_handling(self, mock_post):
        """Test handling of empty script"""
        script_json = []
        
        audio_engine = AudioEngine()
        audio_bytes, error = audio_engine.generate_dialogue_v3(script_json, "test_key")
        
        # Should still make API call with empty inputs
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        body = call_args[1]["json"]
        assert body["inputs"] == []

