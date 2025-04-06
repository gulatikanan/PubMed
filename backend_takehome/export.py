from typing import Dict, List, Any, Optional
import csv
import io
import os
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define CSV columns
CSV_COLUMNS = [
    'PubmedID', 
    'Title', 
    'PublicationDate', 
    'Non-academicAuthor(s)', 
    'CompanyAffiliation(s)', 
    'CorrespondingAuthorEmail'
]

def format_as_csv(results: List[Dict[str, Any]]) -> str:
    """
    Format results as a CSV string.
    
    Args:
        results: List of paper details
        
    Returns:
        CSV-formatted string
    """
    if not results:
        return ""
        
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    
    for result in results:
        writer.writerow(result)
        
    return output.getvalue()

def export_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """
    Export results to a CSV file.
    
    Args:
        results: List of paper details
        filename: Output filename
    """
    if not results:
        logger.warning("No results to export")
        return
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
        
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(results)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    logger.info(f"Results exported to {filename}")

def print_csv(results: List[Dict[str, Any]]) -> None:
    """
    Print results as CSV to console.
    
    Args:
        results: List of paper details
    """
    if not results:
        logger.warning("No results to print")
        return
        
    csv_string = format_as_csv(results)
    print(csv_string)































































































































































































# # test2 
# # papers_fetcher/export.py
# from typing import Dict, List, Any, Optional
# import csv
# import io
# import os
# import logging
# import pandas as pd

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Define CSV columns
# CSV_COLUMNS = [
#     'PubmedID', 
#     'Title', 
#     'PublicationDate', 
#     'Non-academicAuthor(s)', 
#     'CompanyAffiliation(s)', 
#     'CorrespondingAuthorEmail'
# ]

# def format_as_csv(results: List[Dict[str, Any]]) -> str:
#     """
#     Format results as a CSV string.
    
#     Args:
#         results: List of paper details
        
#     Returns:
#         CSV-formatted string
#     """
#     if not results:
#         return ""
        
#     # Create CSV in memory
#     output = io.StringIO()
#     writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
#     writer.writeheader()
    
#     for result in results:
#         writer.writerow(result)
        
#     return output.getvalue()

# def export_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
#     """
#     Export results to a CSV file.
    
#     Args:
#         results: List of paper details
#         filename: Output filename
#     """
#     if not results:
#         logger.warning("No results to export")
#         return
    
#     # Ensure data directory exists
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
        
#     # Convert to DataFrame for easier handling
#     df = pd.DataFrame(results)
    
#     # Save to CSV
#     df.to_csv(filename, index=False)
#     logger.info(f"Results exported to {filename}")


# # 2def export_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
# #     """
# #     Export results to a CSV file.
    
# #     Args:
# #         results: List of paper details
# #         filename: Output filename
# #     """
# #     if not results:
# #         logger.warning("No results to export")
# #         return
    
# #     # Ensure data directory exists
# #     os.makedirs(os.path.dirname(filename), exist_ok=True)
        
# #     # Convert to DataFrame for easier handling
# #     df = pd.DataFrame(results)
    
# #     # Ensure PubmedID is treated as a string
# #     if 'PubmedID' in df.columns:
# #         df['PubmedID'] = df['PubmedID'].astype(str)
    
# #     # Save to CSV
# #     df.to_csv(filename, index=False)
# #     logger.info(f"Results exported to {filename}")

# def print_csv(results: List[Dict[str, Any]]) -> None:
#     """
#     Print results as CSV to console.
    
#     Args:
#         results: List of paper details
#     """
#     if not results:
#         logger.warning("No results to print")
#         return
        
#     csv_string = format_as_csv(results)
#     print(csv_string)
