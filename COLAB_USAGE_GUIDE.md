# TrialScope AI - Google Colab Usage Guide

## Quick Start in Google Colab

### Step 1: Setup
1. Open a new Google Colab notebook
2. Upload these files to your Colab environment:
   - `colab_api.py`
   - `colab_requirements.txt`
   - `colab_example.py` (optional)

### Step 2: Install Dependencies
```python
!pip install requests pandas openpyxl anthropic
```

### Step 3: Basic Usage (No API Key Required)
```python
from colab_api import search_and_export

# Search for clinical trials
excel_file = search_and_export(
    query="diabetes treatment",
    max_results=30,
    filename="my_clinical_trials.xlsx"
)

print(f"Results saved to: {excel_file}")
```

### Step 4: Advanced Usage (With AI Classification)
```python
# Add your Anthropic API key for AI-powered relevance scoring
ANTHROPIC_API_KEY = "your-api-key-here"

excel_file = search_and_export(
    query="alzheimer's disease treatment",
    anthropic_api_key=ANTHROPIC_API_KEY,
    max_results=50,
    filename="alzheimers_trials_ai_scored.xlsx"
)
```

## Search Examples

### Disease-focused searches:
```python
# Diabetes research
search_and_export("diabetes treatment", max_results=25)

# Cancer studies
search_and_export("breast cancer clinical trial", max_results=30)

# Neurological conditions
search_and_export("alzheimer's disease", max_results=40)
```

### Drug-focused searches:
```python
# Specific drug studies
search_and_export("metformin diabetes", max_results=20)

# Drug categories
search_and_export("immunotherapy cancer", max_results=35)

# Combination therapies
search_and_export("chemotherapy radiation therapy", max_results=25)
```

## Excel Output Columns

Your exported Excel file will contain these columns:

| Column | Description |
|--------|-------------|
| **Title** | Official study title |
| **URL** | Direct link to study details |
| **Source** | Database source (ClinicalTrials.gov, PubMed) |
| **Abstract** | Study summary and description |
| **AI_Score** | AI relevance score (0-100, if using API key) |
| **AI_Classification** | Relevance category (Highly Relevant, Relevant, Less Relevant) |
| **Confidence** | AI confidence in classification |
| **Conditions** | Medical conditions being studied |
| **Phase** | Trial phase (Phase I, II, III, IV) |
| **Status** | Current study status (Recruiting, Active, Completed) |
| **Start_Date** | Study start date |
| **Sponsor** | Primary sponsor organization |
| **Interventions** | Treatments/drugs being tested |
| **NCT_ID** | ClinicalTrials.gov identifier |

## Advanced API Usage

### Direct API Class Usage:
```python
from colab_api import TrialScopeAPI

# Initialize API client
api = TrialScopeAPI(anthropic_api_key="your-key-here")

# Custom search with specific parameters
results = api.search_trials(
    query="cancer immunotherapy",
    max_results=100,
    include_pubmed=True,
    use_ai_classification=True
)

# Export with custom formatting
excel_file = api.export_to_excel(results, "custom_search.xlsx")
```

### Search Multiple Queries:
```python
queries = [
    "diabetes type 2 treatment",
    "alzheimer's disease therapy",
    "cancer immunotherapy",
    "heart disease prevention"
]

for query in queries:
    filename = f"{query.replace(' ', '_')}_trials.xlsx"
    search_and_export(query, max_results=30, filename=filename)
    print(f"Completed: {query}")
```

## Data Sources

- **ClinicalTrials.gov**: 450,000+ clinical trials (primary source)
- **PubMed**: Related research papers and literature
- **AI Classification**: Anthropic Claude AI for relevance scoring

## API Key Setup

### Getting an Anthropic API Key:
1. Visit: https://console.anthropic.com/
2. Create an account or sign in
3. Go to API Keys section
4. Create a new API key
5. Copy and use in your scripts

### Benefits of Using API Key:
- AI-powered relevance scoring (0-100)
- Intelligent classification categories
- Confidence scores for each result
- Better result ranking and filtering

## Troubleshooting

### Common Issues:
1. **Import Error**: Make sure you've uploaded `colab_api.py` to your Colab environment
2. **Missing Dependencies**: Run `!pip install requests pandas openpyxl anthropic`
3. **No Results**: Try broader search terms or increase `max_results`
4. **API Errors**: Check your Anthropic API key and internet connection

### Rate Limiting:
- The API includes automatic rate limiting to respect service limits
- Large searches (100+ results) may take several minutes
- AI classification adds processing time but provides better results

## Example Complete Colab Notebook:

```python
# Cell 1: Setup
!pip install requests pandas openpyxl anthropic

# Cell 2: Upload files and import
from google.colab import files
uploaded = files.upload()  # Upload colab_api.py

from colab_api import search_and_export

# Cell 3: Search and export
excel_file = search_and_export(
    query="diabetes treatment clinical trial",
    max_results=50,
    filename="diabetes_research_2024.xlsx"
)

# Cell 4: Download results
from google.colab import files
files.download(excel_file)
```

## Support

For issues or questions:
1. Check the error messages in the Colab output
2. Verify all dependencies are installed
3. Ensure proper file uploads and API key format
4. Try with smaller `max_results` values first

Happy researching! 🔬📊