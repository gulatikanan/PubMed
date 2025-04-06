
from typing import Dict, List, Tuple, Set, Any, Optional
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Common academic institution keywords
ACADEMIC_KEYWORDS = {
    'university', 'college', 'institute', 'school', 'academy', 'faculty',
    'hospital', 'clinic', 'medical center', 'health center', 'laboratory',
    'research center', 'national', 'federal', 'ministry', 'department',
    'center for', 'centre for', 'institution', 'foundation', 'association',
}

# Common pharmaceutical/biotech company keywords
PHARMA_BIOTECH_KEYWORDS = {
    'pharma', 'pharmaceutical', 'biotech', 'bioscience', 'therapeutics',
    'biologics', 'biopharmaceutical', 'laboratories', 'labs', 'inc', 'llc',
    'ltd', 'limited', 'corp', 'corporation', 'co.', 'company', 'gmbh',
    'biopharma', 'genomics', 'health', 'technologies', 'diagnostics',
    'genentech', 'moderna', 'pfizer', 'astrazeneca', 'novartis'
}

# Common email domains for academic institutions
ACADEMIC_EMAIL_DOMAINS = {
    'edu', 'ac.uk', 'ac.jp', 'edu.au', 'ac.cn', 'ac.in', 'edu.sg',
    'uni-', '.uni.', 'nih.gov', 'gov', 'org', 'net',
}

def is_academic_affiliation(affiliation: str) -> bool:
    """
    Determine if an affiliation is academic based on keywords.
    
    Args:
        affiliation: The affiliation string to check
        
    Returns:
        True if the affiliation appears to be academic, False otherwise
    """
    if not affiliation:
        return False
        
    affiliation_lower = affiliation.lower()
    
    # Check for academic keywords
    for keyword in ACADEMIC_KEYWORDS:
        if keyword in affiliation_lower:
            return True
            
    return False

def is_company_affiliation(affiliation: str) -> bool:
    """
    Determine if an affiliation is a pharmaceutical or biotech company.
    
    Args:
        affiliation: The affiliation string to check
        
    Returns:
        True if the affiliation appears to be a company, False otherwise
    """
    if not affiliation:
        return False
        
    affiliation_lower = affiliation.lower()
    
    # Check for company keywords
    for keyword in PHARMA_BIOTECH_KEYWORDS:
        if keyword in affiliation_lower:
            return True
            
    # Check for common company indicators
    company_patterns = [
        r'\b[A-Z][a-z]*[A-Z][a-z]*\b',  # CamelCase company names
        r'\b[A-Z][a-z]+, Inc\b',
        r'\b[A-Z][a-z]+ Pharmaceuticals\b',
        r'\b[A-Z][a-z]+ Biotech\b',
        r'\b[A-Z][a-z]+ Therapeutics\b',
    ]
    
    for pattern in company_patterns:
        if re.search(pattern, affiliation):
            return True
            
    return False

def is_academic_email(email: str) -> bool:
    """
    Determine if an email address is from an academic institution.
    
    Args:
        email: The email address to check
        
    Returns:
        True if the email appears to be academic, False otherwise
    """
    if not email:
        return False
        
    email_lower = email.lower()
    
    # Extract domain
    try:
        domain = email_lower.split('@')[1]
    except IndexError:
        return False
        
    # Check for academic domains
    for academic_domain in ACADEMIC_EMAIL_DOMAINS:
        if academic_domain in domain:
            return True
            
    return False

def extract_company_name(affiliation: str) -> Optional[str]:
    """
    Extract the company name from an affiliation string.
    
    Args:
        affiliation: The affiliation string
        
    Returns:
        The extracted company name or None if not found
    """
    if not affiliation:
        return None
        
    # Try to extract company name using common patterns
    company_patterns = [
        r'([A-Z][a-z]*[A-Z][a-z]*(?:\s[A-Z][a-z]+)*)',  # CamelCase names
        r'([A-Z][a-z]+ (?:Pharmaceuticals|Pharma|Biotech|Therapeutics|Inc\.|LLC|Ltd\.|GmbH))',
        r'([A-Z][a-z]+ [A-Z][a-z]+ (?:Pharmaceuticals|Pharma|Biotech|Therapeutics|Inc\.|LLC|Ltd\.|GmbH))',
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, affiliation)
        if match:
            return match.group(1)
            
    # If no specific pattern matches, return the first part of the affiliation
    # that might be a company name (up to the first comma or period)
    parts = re.split(r'[,.]', affiliation)
    if parts:
        return parts[0].strip()
        
    return None

def analyze_author_affiliations(article: Dict[str, Any]) -> Tuple[List[str], List[str], Optional[str]]:
    """
    Analyze author affiliations in a PubMed article.
    
    Args:
        article: PubMed article data
        
    Returns:
        Tuple containing:
        - List of non-academic authors
        - List of company affiliations
        - Corresponding author email (if available)
    """
    non_academic_authors = []
    company_affiliations = set()
    corresponding_email = None
    
    # Extract author information
    if 'AU' not in article or 'AD' not in article:
        return [], [], None
        
    authors = article.get('AU', [])
    affiliations = article.get('AD', [])
    
    # Process each affiliation
    for i, affiliation in enumerate(affiliations):
        if i < len(authors) and affiliation:
            author = authors[i]
            
            # Check if this is a company affiliation
            if not is_academic_affiliation(affiliation) and is_company_affiliation(affiliation):
                non_academic_authors.append(author)
                
                # Extract company name
                company = extract_company_name(affiliation)
                if company:
                    company_affiliations.add(company)
                    
            # Look for email addresses
            email_match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', affiliation)
            if email_match:
                # If this is the first email or it's from a company, use it
                email = email_match.group(1)
                if not corresponding_email or not is_academic_email(email):
                    corresponding_email = email
    
    return non_academic_authors, list(company_affiliations), corresponding_email

def parse_publication_date(article: Dict[str, Any]) -> str:
    """
    Parse the publication date from a PubMed article.
    
    Args:
        article: PubMed article data
        
    Returns:
        Formatted publication date string (YYYY-MM-DD)
    """
    # Try different date fields in order of preference
    date_fields = ['DP', 'DEP', 'EDAT', 'MHDA']
    
    for field in date_fields:
        if field in article and article[field]:
            date_str = article[field]
            
            # Handle different date formats
            try:
                # Full date format: YYYY Mon DD
                if len(date_str.split()) >= 3:
                    date_obj = datetime.strptime(date_str, '%Y %b %d')
                    return date_obj.strftime('%Y-%m-%d')
                # Year and month: YYYY Mon
                elif len(date_str.split()) == 2:
                    date_obj = datetime.strptime(date_str, '%Y %b')
                    return date_obj.strftime('%Y-%m-01')
                # Just year: YYYY
                else:
                    return f"{date_str.strip()}-01-01"
            except ValueError:
                # Try alternative formats
                try:
                    # ISO format
                    if 'T' in date_str:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        return date_obj.strftime('%Y-%m-%d')
                    # YYYY/MM/DD format
                    elif '/' in date_str:
                        date_parts = date_str.split('/')
                        if len(date_parts) >= 3:
                            return f"{date_parts[0]}-{date_parts[1]}-{date_parts[2]}"
                except Exception:
                    pass
    
    # Default to empty string if no valid date found
    return ""

def extract_paper_details(article: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant details from a PubMed article.
    
    Args:
        article: PubMed article data
        
    Returns:
        Dictionary with extracted paper details
    """
    # Extract basic information
    pmid = article.get('PMID', '')
    title = article.get('TI', '')
    publication_date = parse_publication_date(article)
    
    # Analyze author affiliations
    non_academic_authors, company_affiliations, corresponding_email = analyze_author_affiliations(article)
    
    # Create result dictionary
    result = {
        'PubmedID': pmid,
        'Title': title,
        'PublicationDate': publication_date,
        'Non-academicAuthor(s)': '; '.join(non_academic_authors),
        'CompanyAffiliation(s)': '; '.join(company_affiliations),
        'CorrespondingAuthorEmail': corresponding_email or ''
    }
    
    return result

def filter_papers(articles: List[Dict[str, Any]], debug: bool = False) -> List[Dict[str, Any]]:
    """
    Filter papers to include only those with non-academic authors.
    
    Args:
        articles: List of PubMed article data
        debug: Whether to print debug information
        
    Returns:
        List of dictionaries with extracted paper details
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug(f"Filtering {len(articles)} articles")
    
    results = []
    
    for article in articles:
        try:
            # Extract paper details
            paper_details = extract_paper_details(article)
            
            # Only include papers with non-academic authors
            if paper_details['Non-academicAuthor(s)']:
                results.append(paper_details)
                if debug:
                    logger.debug(f"Found paper with non-academic authors: {paper_details['Title']}")
        except Exception as e:
            if debug:
                logger.error(f"Error processing article {article.get('PMID', 'unknown')}: {str(e)}")
    
    if debug:
        logger.debug(f"Found {len(results)} papers with non-academic authors")
        
    return results

