# tests/test_export.py
import unittest
import os
import sys
import tempfile
import pandas as pd
from io import StringIO
from unittest.mock import patch

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_takehome.export import export_to_csv, print_csv, format_as_csv

class TestExport(unittest.TestCase):
    """Tests for the export module."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_papers = [
            {
                "PubmedID": "12345",
                "Title": "Advances in Drug Research",
                "PublicationDate": "2024-06-15",
                "Non-academicAuthor(s)": "Dr. Jane Smith",
                "CompanyAffiliation(s)": "Pfizer",
                "CorrespondingAuthorEmail": "jane.smith@pfizer.com"
            },
            {
                "PubmedID": "67890",
                "Title": "COVID-19 Vaccine Development",
                "PublicationDate": "2024-05-20",
                "Non-academicAuthor(s)": "Dr. Alice Brown",
                "CompanyAffiliation(s)": "Moderna",
                "CorrespondingAuthorEmail": "alice.brown@moderna.com"
            }
        ]
    
    def test_format_as_csv(self):
        """Test formatting results as CSV."""
        csv_string = format_as_csv(self.sample_papers)
        
        # Check that the CSV string contains the expected headers and data
        self.assertIn('PubmedID,Title,PublicationDate,Non-academicAuthor(s),CompanyAffiliation(s),CorrespondingAuthorEmail', csv_string)
        self.assertIn('12345,Advances in Drug Research,2024-06-15,Dr. Jane Smith,Pfizer,jane.smith@pfizer.com', csv_string.replace('\r\n', '\n'))
        self.assertIn('67890,COVID-19 Vaccine Development,2024-05-20,Dr. Alice Brown,Moderna,alice.brown@moderna.com', csv_string.replace('\r\n', '\n'))
    
    def test_export_to_csv(self):
        """Test exporting results to CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test_output.csv")
            export_to_csv(self.sample_papers, test_file)
            
            # Check that the file was created
            self.assertTrue(os.path.exists(test_file))
            
            # Check the contents of the file
            df = pd.read_csv(test_file)
            self.assertEqual(len(df), 2)
            self.assertEqual(df.iloc[0]["PubmedID"], 12345)
            self.assertEqual(df.iloc[1]["PubmedID"], 67890)
    
    @patch('builtins.print')
    def test_print_csv(self, mock_print):
        """Test printing CSV to console."""
        print_csv(self.sample_papers)
        
        # Check that print was called with the CSV string
        mock_print.assert_called_once()
        csv_string = mock_print.call_args[0][0]
        self.assertIn('PubmedID,Title,PublicationDate,Non-academicAuthor(s),CompanyAffiliation(s),CorrespondingAuthorEmail', csv_string)

if __name__ == "__main__":
    unittest.main()
