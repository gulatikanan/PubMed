import requests
import os
import time
import logging
from typing import List, Dict, Any, Optional
from Bio import Entrez
from Bio import Medline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_entrez(email: str, api_key: Optional[str] = None) -> None:
    """
    Set up Entrez for PubMed API access.
    
    Args:
        email: Email address to identify yourself to NCBI
        api_key: Optional NCBI API key for higher request limits
    """
    Entrez.email = email
    Entrez.tool = "PapersFetcher"
    
    # Use API key from environment variable if not provided
    if not api_key:
        api_key = os.getenv("PUBMED_API_KEY")
        
    if api_key:
        Entrez.api_key = api_key
        logger.info("Using NCBI API key for higher request limits")
    else:
        logger.warning("No API key provided. Request limits will be lower.")

def search_pubmed(query: str, retmax: int = 100, debug: bool = False) -> List[str]:
    """
    Search PubMed for articles matching the query.
    
    Args:
        query: PubMed search query
        retmax: Maximum number of results to return
        debug: Whether to print debug information
        
    Returns:
        List of PubMed IDs matching the query
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug(f"Searching PubMed with query: {query}")
    
    try:
        # Search for articles
        handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
        record = Entrez.read(handle)
        handle.close()
        
        pmids = record["IdList"]
        
        if debug:
            logger.debug(f"Found {len(pmids)} articles")
            
        return pmids
    
    except Exception as e:
        logger.error(f"Error searching PubMed: {str(e)}")
        raise

def fetch_article_details(pmids: List[str], debug: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch detailed information for a list of PubMed IDs.
    
    Args:
        pmids: List of PubMed IDs
        debug: Whether to print debug information
        
    Returns:
        List of dictionaries containing article details
    """
    if not pmids:
        logger.warning("No PubMed IDs provided to fetch_article_details")
        return []
        
    if debug:
        logger.debug(f"Fetching details for {len(pmids)} articles")
    
    try:
        # Fetch article details in batches to avoid API limits
        batch_size = 50
        all_records = []
        
        for i in range(0, len(pmids), batch_size):
            batch = pmids[i:i+batch_size]
            if debug:
                logger.debug(f"Fetching batch {i//batch_size + 1} with {len(batch)} articles")
            
            handle = Entrez.efetch(db="pubmed", id=",".join(batch), rettype="medline", retmode="text")
            records = list(Medline.parse(handle))
            handle.close()
            
            all_records.extend(records)
            
            # Be nice to the NCBI server - with API key we can make more requests
            if Entrez.api_key:
                time.sleep(0.1)  # Faster with API key
            else:
                time.sleep(0.5)  # Slower without API key
        
        if debug:
            logger.debug(f"Successfully fetched details for {len(all_records)} articles")
            
        return all_records
    
    except Exception as e:
        logger.error(f"Error fetching article details: {str(e)}")
        raise

def fetch_papers(query: str, email: str, max_results: int = 100, debug: bool = False, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch papers from PubMed based on a query.
    
    Args:
        query: PubMed search query
        email: Email address for PubMed API
        max_results: Maximum number of results to return
        debug: Whether to print debug information
        api_key: Optional NCBI API key
        
    Returns:
        List of dictionaries containing article details
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug(f"Fetching papers with query: {query}")
    
    # Set up Entrez
    setup_entrez(email, api_key)
    
    # Search PubMed
    pmids = search_pubmed(query, max_results, debug)
    
    # Fetch article details
    articles = fetch_article_details(pmids, debug)
    
    return articles


















































# # Test2
# import requests
# import os
# import time
# import logging
# from typing import List, Dict, Any, Optional
# from Bio import Entrez
# from Bio import Medline
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def setup_entrez(email: str, api_key: Optional[str] = None) -> None:
#     """
#     Set up Entrez for PubMed API access.
    
#     Args:
#         email: Email address to identify yourself to NCBI
#         api_key: Optional NCBI API key for higher request limits
#     """
#     Entrez.email = email
#     Entrez.tool = "PapersFetcher"
    
#     # Use API key from environment variable if not provided
#     if not api_key:
#         api_key = os.getenv("PUBMED_API_KEY")
        
#     if api_key:
#         Entrez.api_key = api_key
#         logger.info("Using NCBI API key for higher request limits")
#     else:
#         logger.warning("No API key provided. Request limits will be lower.")

# def search_pubmed(query: str, retmax: int = 100, debug: bool = False) -> List[str]:
#     """
#     Search PubMed for articles matching the query.
    
#     Args:
#         query: PubMed search query
#         retmax: Maximum number of results to return
#         debug: Whether to print debug information
        
#     Returns:
#         List of PubMed IDs matching the query
#     """
#     if debug:
#         logger.setLevel(logging.DEBUG)
#         logger.debug(f"Searching PubMed with query: {query}")
    
#     try:
#         # Search for articles
#         handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
#         record = Entrez.read(handle)
#         handle.close()
        
#         pmids = record["IdList"]
        
#         if debug:
#             logger.debug(f"Found {len(pmids)} articles")
            
#         return pmids
    
#     except Exception as e:
#         logger.error(f"Error searching PubMed: {str(e)}")
#         raise

# def fetch_article_details(pmids: List[int], debug: bool = False) -> List[Dict[str, Any]]:
#     """
#     Fetch detailed information for a list of PubMed IDs.
    
#     Args:
#         pmids: List of PubMed IDs
#         debug: Whether to print debug information
        
#     Returns:
#         List of dictionaries containing article details
#     """
#     if not pmids:
#         logger.warning("No PubMed IDs provided to fetch_article_details")
#         return []
        
#     if debug:
#         logger.debug(f"Fetching details for {len(pmids)} articles")
    
#     try:
#         # Fetch article details in batches to avoid API limits
#         batch_size = 50
#         all_records = []
        
#         for i in range(0, len(pmids), batch_size):
#             batch = pmids[i:i+batch_size]
#             if debug:
#                 logger.debug(f"Fetching batch {i//batch_size + 1} with {len(batch)} articles")
            
#             # handle = Entrez.efetch(db="pubmed", id=",".join(batch), rettype="medline", retmode="text")
#             handle = Entrez.efetch(db="pubmed", id=",".join(map(str, batch)), rettype="medline", retmode="text")

#             records = list(Medline.parse(handle))
#             handle.close()
            
#             all_records.extend(records)
            
#             # Be nice to the NCBI server - with API key we can make more requests
#             if Entrez.api_key:
#                 time.sleep(0.1)  # Faster with API key
#             else:
#                 time.sleep(0.5)  # Slower without API key
        
#         if debug:
#             logger.debug(f"Successfully fetched details for {len(all_records)} articles")
            
#         # return all_records ----------------------------------------------------------------------------------------------------
#         structured_articles = []

#         for record in all_records:
#             structured_articles.append({
#                 "PubmedID": record.get("PMID", "N/A"),
#                 "Title": record.get("TI", "N/A"),
#                 "PublicationDate": record.get("DP", "N/A"),
#                 "Authors": record.get("AU", []),
#                 "Affiliations": record.get("AD", "N/A"),
#                 "CorrespondingAuthorEmail": record.get("LA", "N/A")  
#             })

#         return structured_articles

    
#     except Exception as e:
#         logger.error(f"Error fetching article details: {str(e)}")
#         raise

# def fetch_papers(query: str, email: str, max_results: int = 100, debug: bool = False, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
#     """
#     Fetch papers from PubMed based on a query.
    
#     Args:
#         query: PubMed search query
#         email: Email address for PubMed API
#         max_results: Maximum number of results to return
#         debug: Whether to print debug information
#         api_key: Optional NCBI API key
        
#     Returns:
#         List of dictionaries containing article details
#     """
#     if debug:
#         logger.setLevel(logging.DEBUG)
#         logger.debug(f"Fetching papers with query: {query}")
    
#     # Set up Entrez
#     setup_entrez(email, api_key)
    
#     # Search PubMed
#     pmids = search_pubmed(query, max_results, debug)
    
#     # Fetch article details
#     articles = fetch_article_details(pmids, debug)
    
#     return articles

