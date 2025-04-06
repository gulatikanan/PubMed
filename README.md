
# PubMed Research Paper Fetcher

## 📖 Overview  
This project is designed to fetch research papers from PubMed using the NCBI Entrez API. It automatically filters papers that include non-academic authors and exports the results into a structured CSV file.

Key features include:
- A Command-Line Interface (CLI) to search and retrieve papers  
- Automatic filtering of authors affiliated with biotech or pharmaceutical companies  
- CSV export functionality for easy data sharing  
- Unit tests to maintain reliability and robustness  

---

## 🛠 Tech Stack & Dependencies

- **Python 3.9+** (Recommended: Python 3.11+)
- **Poetry** for dependency management and virtual environment setup
- **NCBI Entrez API** for retrieving data from PubMed
- **Pandas** for data processing and CSV generation
- **Biopython** for parsing PubMed records
- **Dotenv** for securely storing API keys
- **Logging** for debugging and tracking execution flow

---

## 🚀 Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone <repository_url>
cd backend-takehome
```

### 2️⃣ Install Dependencies
```bash
poetry install
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add your PubMed API key:
```env
PUBMED_API_KEY=your_api_key_here
```
> **Note:** An API key is required to increase request limits to PubMed.

### 4️⃣ Activate the Virtual Environment
```bash
poetry shell
```

### 5️⃣ Run the CLI Application
To search and filter PubMed papers, run:
```bash
poetry run python -m cli.main "cancer research" -e "your_email@example.com" -f output.csv
```

---

## 📂 Project Structure

```
backend-takehome/
├── cli/
│   └── main.py              # CLI entry point
├── backend_takehome/
│   ├── fetch.py             # PubMed fetching logic
│   ├── filter.py            # Filter authors by pharma/biotech affiliation
│   └── export.py            # Export results to CSV
├── tests/
│   ├── test_fetch.py        # Tests for fetch.py
│   ├── test_cli.py          # Tests for CLI
│   └── test_export.py       # Tests for export.py
├── data/                    # CSV output location
├── .env                     # Environment variables (API Key here)
├── .gitignore               # Ignore sensitive or unnecessary files
├── README.md                # Instructions to run
└── pyproject.toml           # Project dependencies and setup
```


## 🛠 File-by-File Breakdown

### `fetch.py` (Fetching Papers)
- Connects to the NCBI Entrez API using your email and API key
- Searches PubMed based on your query
- Collects metadata: authors, affiliations, publication dates, etc.

### `filter.py` (Filtering Papers)
- Detects non-academic authors using a list of predefined keywords
- Extracts company affiliations (e.g., Pfizer, Moderna)
- Filters out academic-only papers, keeping those with industry participation

### `export.py` (Exporting Data)
- Formats the filtered results
- Exports data to a CSV file with columns for:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Authors
  - Company Affiliations
  - Corresponding Author Email

# Basic usage
python -m cli.main "cancer therapy" -e kansssn@gmail.com

# Save to file
python -m cli.main "cancer therapy" -e kansssn@gmail.com -f results.csv

# Debug mode
python -m cli.main "cancer therapy" -e kansssn@gmail.com -d

# Specify max results
python -m cli.main "cancer therapy" -e kansssn@gmail.com -m 50

# Provide API key directly
python -m cli.main "cancer therapy" -e kansssn@gmail.com -k your_api_key
