"""
Unit tests for WikiScraper class
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core_logic import WikiScraper


class TestWikiScraper:
    """Test cases for WikiScraper"""
    
    def test_extract_title_from_url(self):
        """Test URL title extraction"""
        scraper = WikiScraper()
        
        # Test standard Wikipedia URL
        url1 = "https://en.wikipedia.org/wiki/Mumbai_Indians"
        title1 = scraper._extract_title_from_url(url1)
        assert title1 == "Mumbai Indians"
        
        # Test URL with query params
        url2 = "https://en.wikipedia.org/wiki/Mumbai_Indians?oldformat=true"
        title2 = scraper._extract_title_from_url(url2)
        assert title2 == "Mumbai Indians"
        
        # Test invalid URL
        url3 = "https://example.com/page"
        title3 = scraper._extract_title_from_url(url3)
        assert title3 is None
    
    @patch('core_logic.wikipediaapi.Wikipedia')
    def test_scrape_success_fast_mode(self, mock_wiki_class):
        """Test successful scraping in fast mode"""
        # Mock Wikipedia page
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Mumbai Indians"
        mock_page.summary = "Mumbai Indians is a cricket team."
        mock_page.links = {}
        
        # Mock Wikipedia API
        mock_wiki = Mock()
        mock_wiki.page.return_value = mock_page
        mock_wiki_class.return_value = mock_wiki
        
        scraper = WikiScraper()
        scraper.wiki = mock_wiki
        
        content, error = scraper.scrape("https://en.wikipedia.org/wiki/Mumbai_Indians", "fast")
        
        assert error is None
        assert content == "Mumbai Indians is a cricket team."
    
    @patch('core_logic.wikipediaapi.Wikipedia')
    def test_scrape_page_not_found(self, mock_wiki_class):
        """Test handling of non-existent page"""
        mock_page = Mock()
        mock_page.exists.return_value = False
        
        mock_wiki = Mock()
        mock_wiki.page.return_value = mock_page
        mock_wiki_class.return_value = mock_wiki
        
        scraper = WikiScraper()
        scraper.wiki = mock_wiki
        
        content, error = scraper.scrape("https://en.wikipedia.org/wiki/NonExistentPage", "fast")
        
        assert content is None
        assert "not found" in error.lower()
    
    @patch('core_logic.wikipediaapi.Wikipedia')
    def test_scrape_disambiguation_auto_select(self, mock_wiki_class):
        """Test auto-selection of first disambiguation option"""
        # Mock disambiguation page
        mock_disambig_page = Mock()
        mock_disambig_page.exists.return_value = True
        mock_disambig_page.title = "Mumbai (disambiguation)"
        mock_disambig_page.links = {"Mumbai Indians": None, "Mumbai City": None}
        
        # Mock selected page
        mock_selected_page = Mock()
        mock_selected_page.exists.return_value = True
        mock_selected_page.summary = "Mumbai Indians is a cricket team."
        mock_selected_page.links = {}
        
        mock_wiki = Mock()
        mock_wiki.page.side_effect = [mock_disambig_page, mock_selected_page]
        mock_wiki_class.return_value = mock_wiki
        
        scraper = WikiScraper()
        scraper.wiki = mock_wiki
        
        content, error = scraper.scrape("https://en.wikipedia.org/wiki/Mumbai", "fast")
        
        assert error is None
        assert content == "Mumbai Indians is a cricket team."
    
    @patch('core_logic.wikipediaapi.Wikipedia')
    def test_scrape_pro_mode_sections(self, mock_wiki_class):
        """Test scraping in pro mode with sections"""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Test Page"
        mock_page.summary = "Summary text. " * 10
        mock_page.links = {}
        
        # Mock sections
        mock_section = Mock()
        mock_section.text = "Section text. " * 20
        mock_page.sections = {"Section 1": mock_section}
        
        mock_wiki = Mock()
        mock_wiki.page.return_value = mock_page
        mock_wiki_class.return_value = mock_wiki
        
        scraper = WikiScraper()
        scraper.wiki = mock_wiki
        
        content, error = scraper.scrape("https://en.wikipedia.org/wiki/Test", "pro")
        
        assert error is None
        assert "Summary" in content
        assert "Section 1" in content
    
    def test_extract_sections_word_limit(self):
        """Test section extraction respects word limit"""
        scraper = WikiScraper()
        
        # Mock page with sections
        mock_page = Mock()
        mock_page.summary = "Word " * 50  # 50 words
        mock_section1 = Mock()
        mock_section1.text = "Word " * 100  # 100 words
        mock_section2 = Mock()
        mock_section2.text = "Word " * 200  # 200 words
        mock_page.sections = {
            "Section 1": mock_section1,
            "Section 2": mock_section2
        }
        
        content = scraper._extract_sections(mock_page, max_words=200)
        words = content.split()
        
        # Should be capped at 200 words
        assert len(words) <= 200

