#!/usr/bin/env python3
"""
Google Colab Example - TrialScope AI Clinical Trials Search
Copy and paste this code into your Google Colab notebook
"""

# Step 1: Install required packages
# !pip install requests pandas openpyxl anthropic beautifulsoup4 lxml

# Step 2: Import and use the API
from colab_api import search_and_export

# Step 3: Comprehensive multi-registry search examples

# Example 1: Basic multi-registry search (no API keys needed)
print("🌍 Example 1: Multi-registry diabetes research...")
excel_file = search_and_export(
    query="diabetes treatment",
    max_results=50,
    include_international=True,
    include_academic=True,
    filename="diabetes_multi_registry.xlsx"
)
print(f"✅ Multi-registry results saved to: {excel_file}")

# Example 2: Full-featured search with all APIs (requires API keys)
print("\n🚀 Example 2: Complete search with AI + Google Scholar...")
# Add your API keys here:
# ANTHROPIC_API_KEY = "your-anthropic-key-here"
# SERPAPI_KEY = "your-serpapi-key-here"
# 
# excel_file = search_and_export(
#     query="alzheimer's disease treatment",
#     anthropic_api_key=ANTHROPIC_API_KEY,
#     serpapi_key=SERPAPI_KEY,
#     max_results=80,
#     include_international=True,
#     include_academic=True,
#     filename="alzheimers_comprehensive_search.xlsx"
# )

# Example 3: International registries focus
print("\n🌐 Example 3: Global cancer immunotherapy search...")
excel_file = search_and_export(
    query="cancer immunotherapy checkpoint inhibitor",
    max_results=60,
    include_international=True,
    include_academic=True,
    filename="cancer_global_registries.xlsx"
)
print(f"✅ Global registry search completed: {excel_file}")

# Example 4: Academic literature focus
print("\n📚 Example 4: Academic literature + trials...")
excel_file = search_and_export(
    query="COVID-19 vaccine efficacy",
    max_results=40,
    include_international=False,  # Only ClinicalTrials.gov
    include_academic=True,        # Focus on academic papers
    filename="covid_academic_focus.xlsx"
)
print(f"✅ Academic-focused search saved: {excel_file}")

print("\n📋 Your Excel files contain these columns:")
print("- Title: Study title")
print("- URL: Link to full study details")
print("- Source: Database source (ClinicalTrials.gov, PubMed)")
print("- Abstract: Study summary/description")
print("- AI_Score: Relevance score 0-100 (if using AI)")
print("- AI_Classification: Relevance category")
print("- Conditions: Medical conditions studied")
print("- Phase: Trial phase (I, II, III, IV)")
print("- Status: Current study status")
print("- Sponsor: Study sponsor organization")
print("- Interventions: Treatments being tested")

print("\n🎉 Search completed! Download your Excel files from the Colab file browser.")