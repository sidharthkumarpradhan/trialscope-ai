#!/usr/bin/env python3
"""
Google Colab Example - TrialScope AI Clinical Trials Search
Copy and paste this code into your Google Colab notebook
"""

# Step 1: Install required packages
# !pip install requests pandas openpyxl anthropic

# Step 2: Import and use the API
from colab_api import search_and_export

# Step 3: Basic usage examples

# Example 1: Search for diabetes trials (no API key needed)
print("🔍 Example 1: Searching for diabetes trials...")
excel_file = search_and_export(
    query="diabetes treatment clinical trial",
    max_results=25,
    filename="diabetes_trials.xlsx"
)
print(f"✅ Results saved to: {excel_file}")

# Example 2: Search with AI classification (requires Anthropic API key)
print("\n🔍 Example 2: Advanced search with AI scoring...")
# Uncomment and add your API key:
# ANTHROPIC_API_KEY = "your-api-key-here"
# excel_file = search_and_export(
#     query="alzheimer's disease treatment",
#     anthropic_api_key=ANTHROPIC_API_KEY,
#     max_results=50,
#     filename="alzheimers_trials_ai_scored.xlsx"
# )

# Example 3: Cancer immunotherapy search
print("\n🔍 Example 3: Cancer immunotherapy search...")
excel_file = search_and_export(
    query="cancer immunotherapy checkpoint inhibitor",
    max_results=30,
    filename="cancer_immunotherapy_trials.xlsx"
)
print(f"✅ Cancer trials saved to: {excel_file}")

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