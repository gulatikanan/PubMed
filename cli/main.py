
import argparse
import sys
import os
import logging
from typing import List, Optional
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_takehome.fetch import fetch_papers
from backend_takehome.filter import filter_papers
from backend_takehome.export import export_to_csv, print_csv


# from papers_fetcher.fetch import fetch_papers
# from papers_fetcher.filter import filter_papers
# from papers_fetcher.export import export_to_csv, print_csv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Find research papers with authors from pharmaceutical/biotech companies."
    )
    
    parser.add_argument(
        "query",
        help="PubMed search query"
    )
    
    parser.add_argument(
        "-e", "--email",
        required=True,
        help="Email address for PubMed API (required)"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Output filename (if not provided, results are printed to console)"
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Print debug information"
    )
    
    parser.add_argument(
        "-m", "--max-results",
        type=int,
        default=100,
        help="Maximum number of results to return (default: 100)"
    )
    
    parser.add_argument(
        "-k", "--api-key",
        help="NCBI API key for higher request limits (can also be set in .env file)"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s 0.1.0"
    )
    
    return parser.parse_args(args)

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Parse arguments
        parsed_args = parse_args(args)
        
        if parsed_args.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
            logger.debug(f"Arguments: {parsed_args}")
        
        # Get API key from arguments or environment
        api_key = parsed_args.api_key or os.getenv("PUBMED_API_KEY")
        
        # Fetch papers
        logger.info(f"Fetching papers for query: {parsed_args.query}")
        articles = fetch_papers(
            query=parsed_args.query,
            email=parsed_args.email,
            max_results=parsed_args.max_results,
            debug=parsed_args.debug,
            api_key=api_key
        )
        
        # Filter papers
        logger.info("Filtering papers for non-academic authors")
        results = filter_papers(articles, debug=parsed_args.debug)
        
        # Output results
        if parsed_args.file:
            # If path doesn't include directory, add data/ prefix
            filename = parsed_args.file
            # if not os.path.dirname(filename):
            #     filename = os.path.join("data", filename)
            if not os.path.dirname(filename):
                filename = os.path.join("data", filename)

            # Ensure data directory exists before saving
            os.makedirs(os.path.dirname(filename), exist_ok=True)
                
            export_to_csv(results, filename)
        else:
            print_csv(results)
            
        logger.info(f"Found {len(results)} papers with non-academic authors")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if parsed_args and parsed_args.debug:
            logger.exception("Detailed error information:")
        return 1

if __name__ == "__main__":
    sys.exit(main())