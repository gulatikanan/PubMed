# tests/test_cli.py
import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli.main import parse_args, main

class TestCLI(unittest.TestCase):
    """Tests for the CLI module."""
    
    def test_parse_args(self):
        """Test parsing of command-line arguments."""
        args = parse_args(['cancer', '-e', 'test@example.com', '-f', 'output.csv', '-d'])
        
        self.assertEqual(args.query, 'cancer')
        self.assertEqual(args.email, 'test@example.com')
        self.assertEqual(args.file, 'output.csv')
        self.assertTrue(args.debug)
        
    @patch('cli.main.fetch_papers')
    @patch('cli.main.filter_papers')
    @patch('cli.main.export_to_csv')
    def test_main_with_file(self, mock_export, mock_filter, mock_fetch):
        """Test main function with file output."""
        # Mock the fetch and filter responses
        mock_fetch.return_value = [{'PMID': '12345', 'TI': 'Test Paper'}]
        mock_filter.return_value = [
            {
                'PubmedID': '12345',
                'Title': 'Test Paper',
                'PublicationDate': '2023-01-15',
                'Non-academicAuthor(s)': 'Smith J',
                'CompanyAffiliation(s)': 'Pfizer Inc',
                'CorrespondingAuthorEmail': 'smith.j@pfizer.com'
            }
        ]
        
        # Call the function
        exit_code = main(['cancer', '-e', 'test@example.com', '-f', 'output.csv'])
        
        # Check the result
        self.assertEqual(exit_code, 0)
        mock_fetch.assert_called_once()
        mock_filter.assert_called_once()
        mock_export.assert_called_once()
        
    @patch('cli.main.fetch_papers')
    @patch('cli.main.filter_papers')
    @patch('cli.main.print_csv')
    def test_main_without_file(self, mock_print, mock_filter, mock_fetch):
        """Test main function without file output."""
        # Mock the fetch and filter responses
        mock_fetch.return_value = [{'PMID': '12345', 'TI': 'Test Paper'}]
        mock_filter.return_value = [
            {
                'PubmedID': '12345',
                'Title': 'Test Paper',
                'PublicationDate': '2023-01-15',
                'Non-academicAuthor(s)': 'Smith J',
                'CompanyAffiliation(s)': 'Pfizer Inc',
                'CorrespondingAuthorEmail': 'smith.j@pfizer.com'
            }
        ]
        
        # Call the function
        exit_code = main(['cancer', '-e', 'test@example.com'])
        
        # Check the result
        self.assertEqual(exit_code, 0)
        mock_fetch.assert_called_once()
        mock_filter.assert_called_once()
        mock_print.assert_called_once()
        
    @patch('cli.main.fetch_papers')
    def test_main_error(self, mock_fetch):
        """Test error handling in the main function."""
        # Mock an error
        mock_fetch.side_effect = Exception("Test error")
        
        # Call the function
        exit_code = main(['cancer', '-e', 'test@example.com'])
        
        # Check the result
        self.assertEqual(exit_code, 1)
        mock_fetch.assert_called_once()

if __name__ == "__main__":
    unittest.main()