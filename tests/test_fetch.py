# tests/test_fetch.py
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_takehome.fetch import setup_entrez, search_pubmed, fetch_article_details, fetch_papers

class TestFetch(unittest.TestCase):
    """Tests for the fetch module."""
    
    @patch('backend_takehome.fetch.Entrez')
    def test_setup_entrez(self, mock_entrez):
        """Test setup of Entrez."""
        # Test with API key
        setup_entrez("test@example.com", "test_api_key")
        self.assertEqual(mock_entrez.email, "test@example.com")
        self.assertEqual(mock_entrez.tool, "PapersFetcher")
        self.assertEqual(mock_entrez.api_key, "test_api_key")
        
        # Test without API key
        setup_entrez("test@example.com")
        self.assertEqual(mock_entrez.email, "test@example.com")
        
    @patch('backend_takehome.fetch.Entrez')
    def test_search_pubmed(self, mock_entrez):
        """Test searching PubMed."""
        # Mock the esearch response
        mock_handle = MagicMock()
        mock_entrez.esearch.return_value = mock_handle
        mock_entrez.read.return_value = {"IdList": ["12345", "67890"]}
        
        # Call the function
        result = search_pubmed("cancer", 10, True)
        
        # Check the result
        self.assertEqual(result, ["12345", "67890"])
        mock_entrez.esearch.assert_called_once_with(db="pubmed", term="cancer", retmax=10)
        
    @patch('backend_takehome.fetch.Entrez')
    @patch('backend_takehome.fetch.Medline')
    def test_fetch_article_details(self, mock_medline, mock_entrez):
        """Test fetching article details."""
        # Mock the efetch response
        mock_handle = MagicMock()
        mock_entrez.efetch.return_value = mock_handle
        # Update the mock data to include the PMID field correctly
        mock_medline.parse.return_value = [{"PMID": "12345", "TI": "Test Paper"}]
        
        # Call the function
        result = fetch_article_details(["12345"], True)
        
        # Check the result
        self.assertEqual(len(result), 1)
        # self.assertEqual(result[0]["PMID"], "12345")
        self.assertEqual(result[0]["PubmedID"], "12345")  # ✅ Match the actual key name
        # self.assertEqual(result[0]["TI"], "Test Paper")
        self.assertEqual(result[0]["Title"], "Test Paper")
        mock_entrez.efetch.assert_called_once_with(
            db="pubmed", id="12345", rettype="medline", retmode="text"
        )
        
    @patch('backend_takehome.fetch.setup_entrez')
    @patch('backend_takehome.fetch.search_pubmed')
    @patch('backend_takehome.fetch.fetch_article_details')
    def test_fetch_papers(self, mock_fetch_details, mock_search, mock_setup):
        """Test fetching papers."""
        # Mock the search and fetch responses
        mock_search.return_value = ["12345", "67890"]
        mock_fetch_details.return_value = [
            {"PMID": "12345", "TI": "Test Paper 1"},
            {"PMID": "67890", "TI": "Test Paper 2"}
        ]
        
        # Call the function
        result = fetch_papers("cancer", "test@example.com", 10, True)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["PMID"], "12345")
        self.assertEqual(result[1]["PMID"], "67890")
        mock_setup.assert_called_once_with("test@example.com", None)
        mock_search.assert_called_once_with("cancer", 10, True)
        mock_fetch_details.assert_called_once_with(["12345", "67890"], True)

if __name__ == "__main__":
    unittest.main()



# # tests/test_fetch.py
# import unittest
# import os
# import sys
# from unittest.mock import patch, MagicMock

# # Add the parent directory to the path so we can import the modules
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from backend_takehome.fetch import setup_entrez, search_pubmed, fetch_article_details, fetch_papers

# class TestFetch(unittest.TestCase):
#     """Tests for the fetch module."""
    
#     @patch('backend_takehome.fetch.Entrez')
#     def test_setup_entrez(self, mock_entrez):
#         """Test setup of Entrez."""
#         # Test with API key
#         setup_entrez("test@example.com", "test_api_key")
#         self.assertEqual(mock_entrez.email, "test@example.com")
#         self.assertEqual(mock_entrez.tool, "PapersFetcher")
#         self.assertEqual(mock_entrez.api_key, "test_api_key")
        
#         # Test without API key
#         setup_entrez("test@example.com")
#         self.assertEqual(mock_entrez.email, "test@example.com")
        
#     @patch('backend_takehome.fetch.Entrez')
#     def test_search_pubmed(self, mock_entrez):
#         """Test searching PubMed."""
#         # Mock the esearch response
#         mock_handle = MagicMock()
#         mock_entrez.esearch.return_value = mock_handle
#         mock_entrez.read.return_value = {"IdList": ["12345", "67890"]}
        
#         # Call the function
#         result = search_pubmed("cancer", 10, True)
        
#         # Check the result
#         self.assertEqual(result, ["12345", "67890"])
#         mock_entrez.esearch.assert_called_once_with(db="pubmed", term="cancer", retmax=10)
        
#     @patch('backend_takehome.fetch.Entrez')
#     @patch('backend_takehome.fetch.Medline')
#     def test_fetch_article_details(self, mock_medline, mock_entrez):
#         """Test fetching article details."""
#         # Mock the efetch response
#         mock_handle = MagicMock()
#         mock_entrez.efetch.return_value = mock_handle
#         mock_medline.parse.return_value = [{"PMID": "12345", "TI": "Test Paper"}]
        
#         # Call the function
#         result = fetch_article_details(["12345"], True)
        
#         # Check the result
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["PMID"], "12345")
#         self.assertEqual(result[0]["TI"], "Test Paper")
#         mock_entrez.efetch.assert_called_once_with(
#             db="pubmed", id="12345", rettype="medline", retmode="text"
#         )
        
#     @patch('backend_takehome.fetch.setup_entrez')
#     @patch('backend_takehome.fetch.search_pubmed')
#     @patch('backend_takehome.fetch.fetch_article_details')
#     def test_fetch_papers(self, mock_fetch_details, mock_search, mock_setup):
#         """Test fetching papers."""
#         # Mock the search and fetch responses
#         mock_search.return_value = ["12345", "67890"]
#         mock_fetch_details.return_value = [
#             {"PMID": "12345", "TI": "Test Paper 1"},
#             {"PMID": "67890", "TI": "Test Paper 2"}
#         ]
        
#         # Call the function
#         result = fetch_papers("cancer", "test@example.com", 10, True)
        
#         # Check the result
#         self.assertEqual(len(result), 2)
#         self.assertEqual(result[0]["PMID"], "12345")
#         self.assertEqual(result[1]["PMID"], "67890")
#         mock_setup.assert_called_once_with("test@example.com", None)
#         mock_search.assert_called_once_with("cancer", 10, True)
#         mock_fetch_details.assert_called_once_with(["12345", "67890"], True)

# if __name__ == "__main__":
#     unittest.main()