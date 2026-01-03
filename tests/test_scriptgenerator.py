"""
Unit tests for ScriptGenerator class
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from core_logic import ScriptGenerator


class TestScriptGenerator:
    """Test cases for ScriptGenerator"""
    
    @patch('core_logic.genai.configure')
    @patch('core_logic.genai.GenerativeModel')
    def test_generate_script_success(self, mock_model_class, mock_configure):
        """Test successful script generation"""
        # Mock Gemini response
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"speaker": "Host", "text": "Achcha, so Mumbai Indians..."},
            {"speaker": "Guest", "text": "Haan bhai, amazing team!"}
        ])
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        script_gen = ScriptGenerator("test_api_key")
        script_gen.model = mock_model
        
        script, error = script_gen.generate_script("Test content", "RJ", 120)
        
        assert error is None
        assert isinstance(script, list)
        assert len(script) == 2
        assert script[0]["speaker"] == "Host"
        assert script[1]["speaker"] == "Guest"
    
    @patch('core_logic.genai.configure')
    @patch('core_logic.genai.GenerativeModel')
    def test_strip_markdown_code_fences(self, mock_model_class, mock_configure):
        """Test stripping markdown code fences from response"""
        # Response with markdown fences
        mock_response = Mock()
        mock_response.text = "```json\n[{\"speaker\": \"Host\", \"text\": \"Test\"}]\n```"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        script_gen = ScriptGenerator("test_api_key")
        script_gen.model = mock_model
        
        script, error = script_gen.generate_script("Test content", "RJ", 120)
        
        assert error is None
        assert isinstance(script, list)
    
    @patch('core_logic.genai.configure')
    @patch('core_logic.genai.GenerativeModel')
    def test_validate_speaker_names(self, mock_model_class, mock_configure):
        """Test validation of speaker names"""
        # Invalid speaker name
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"speaker": "InvalidSpeaker", "text": "Test"}
        ])
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        script_gen = ScriptGenerator("test_api_key")
        script_gen.model = mock_model
        
        script, error = script_gen.generate_script("Test content", "RJ", 120)
        
        assert script is None
        assert "Speaker must be" in error
    
    @patch('core_logic.genai.configure')
    @patch('core_logic.genai.GenerativeModel')
    def test_validate_required_fields(self, mock_model_class, mock_configure):
        """Test validation of required fields"""
        # Missing 'text' field
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"speaker": "Host"}
        ])
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        script_gen = ScriptGenerator("test_api_key")
        script_gen.model = mock_model
        
        script, error = script_gen.generate_script("Test content", "RJ", 120)
        
        assert script is None
        assert "must have 'speaker' and 'text' fields" in error
    
    @patch('core_logic.genai.configure')
    @patch('core_logic.genai.GenerativeModel')
    def test_validate_json_array(self, mock_model_class, mock_configure):
        """Test validation that response is a JSON array"""
        # Not an array
        mock_response = Mock()
        mock_response.text = json.dumps({"speaker": "Host", "text": "Test"})
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        script_gen = ScriptGenerator("test_api_key")
        script_gen.model = mock_model
        
        script, error = script_gen.generate_script("Test content", "RJ", 120)
        
        assert script is None
        assert "must be a JSON array" in error
    
    def test_strip_markdown_helper(self):
        """Test markdown stripping helper function"""
        script_gen = ScriptGenerator("test_key")
        
        # Test with markdown fences
        text1 = "```json\n[{\"test\": \"value\"}]\n```"
        result1 = script_gen._strip_markdown(text1)
        assert "```" not in result1
        
        # Test without markdown
        text2 = "[{\"test\": \"value\"}]"
        result2 = script_gen._strip_markdown(text2)
        assert result2 == text2
    
    @patch('core_logic.genai.configure')
    @patch('core_logic.genai.GenerativeModel')
    def test_v3_audio_tags_present(self, mock_model_class, mock_configure):
        """Test that V3 audio tags can be present in generated script"""
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"speaker": "Host", "text": "Achcha [laughs], so..."},
            {"speaker": "Guest", "text": "[sighs] Haan bhai!"}
        ])
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        script_gen = ScriptGenerator("test_api_key")
        script_gen.model = mock_model
        
        script, error = script_gen.generate_script("Test content", "RJ", 120)
        
        assert error is None
        assert "[laughs]" in script[0]["text"]
        assert "[sighs]" in script[1]["text"]

