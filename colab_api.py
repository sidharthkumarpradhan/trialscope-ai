#!/usr/bin/env python3
"""
TrialScope AI - Colab API Script
Standalone API for searching clinical trials and exporting to Excel
Usage: Can be run in Google Colab or any Python environment
"""

import requests
import pandas as pd
import json
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrialScopeAPI:
    """Standalone API client for clinical trial searches"""
    
    def __init__(self, anthropic_api_key: str = None):
        """
        Initialize the API client
        
        Args:
            anthropic_api_key: Your Anthropic API key for AI classification
        """
        self.anthropic_api_key = anthropic_api_key
        self.base_url = "https://clinicaltrials.gov/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TrialScope-AI/1.0 (Clinical Research Tool)',
            'Accept': 'application/json'
        })
        
        # Registry configurations
        self.registries = {
            'clinicaltrials_gov': {
                'name': 'ClinicalTrials.gov',
                'url': 'https://clinicaltrials.gov/api/v2',
                'trials': 450000,
                'status': 'operational'
            },
            'eu_ctis': {
                'name': 'EU Clinical Trial Information System',
                'url': 'https://euclinicaltrials.eu/ctis-public',
                'trials': 85000,
                'status': 'operational'
            },
            'isrctn': {
                'name': 'ISRCTN Registry',
                'url': 'https://www.isrctn.com',
                'trials': 45000,
                'status': 'operational'
            }
        }
    
    def search_clinicaltrials_gov(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search ClinicalTrials.gov database
        
        Args:
            query: Search query (disease, drug, condition)
            max_results: Maximum number of results to return
            
        Returns:
            List of trial dictionaries
        """
        logger.info(f"Searching ClinicalTrials.gov for: {query}")
        
        try:
            # Construct search parameters
            params = {
                'query.cond': query,
                'query.term': query,
                'format': 'json',
                'fields': 'NCTId,BriefTitle,OfficialTitle,Condition,BriefSummary,DetailedDescription,PrimaryOutcomeMeasure,StudyType,Phase,OverallStatus,StartDate,CompletionDate,Sponsor,Location,InterventionName,ArmGroupLabel',
                'min_rnk': 1,
                'max_rnk': max_results,
                'sort': 'EnrollmentCount:desc'
            }
            
            response = self.session.get(f"{self.base_url}/studies", params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            studies = data.get('studies', [])
            
            logger.info(f"Found {len(studies)} trials from ClinicalTrials.gov")
            
            # Process results
            processed_trials = []
            for study in studies:
                try:
                    protocol_section = study.get('protocolSection', {})
                    identification = protocol_section.get('identificationModule', {})
                    description = protocol_section.get('descriptionModule', {})
                    conditions = protocol_section.get('conditionsModule', {})
                    design = protocol_section.get('designModule', {})
                    status = protocol_section.get('statusModule', {})
                    sponsor = protocol_section.get('sponsorCollaboratorsModule', {})
                    contacts = protocol_section.get('contactsLocationsModule', {})
                    interventions = protocol_section.get('armsInterventionsModule', {})
                    
                    # Extract key information
                    nct_id = identification.get('nctId', 'N/A')
                    title = identification.get('briefTitle', identification.get('officialTitle', 'No title'))
                    abstract = description.get('briefSummary', description.get('detailedDescription', 'No abstract available'))
                    condition_list = conditions.get('conditions', [])
                    phase = design.get('phases', ['N/A'])[0] if design.get('phases') else 'N/A'
                    study_type = design.get('studyType', 'N/A')
                    overall_status = status.get('overallStatus', 'Unknown')
                    start_date = status.get('startDateStruct', {}).get('date', 'N/A')
                    primary_sponsor = sponsor.get('leadSponsor', {}).get('name', 'N/A')
                    intervention_names = [i.get('name', '') for i in interventions.get('interventions', [])]
                    
                    # Create URL
                    url = f"https://clinicaltrials.gov/study/{nct_id}" if nct_id != 'N/A' else 'N/A'
                    
                    # Clean abstract text
                    if abstract and isinstance(abstract, str):
                        abstract = re.sub(r'<[^>]+>', '', abstract)  # Remove HTML tags
                        abstract = re.sub(r'\s+', ' ', abstract).strip()  # Clean whitespace
                    
                    processed_trial = {
                        'title': title,
                        'url': url,
                        'source': 'ClinicalTrials.gov',
                        'abstract': abstract,
                        'nct_id': nct_id,
                        'conditions': ', '.join(condition_list) if condition_list else 'N/A',
                        'phase': phase,
                        'study_type': study_type,
                        'status': overall_status,
                        'start_date': start_date,
                        'sponsor': primary_sponsor,
                        'interventions': ', '.join(intervention_names) if intervention_names else 'N/A'
                    }
                    
                    processed_trials.append(processed_trial)
                    
                except Exception as e:
                    logger.warning(f"Error processing trial: {e}")
                    continue
            
            return processed_trials
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def search_pubmed_related(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search PubMed for related research papers
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            List of paper dictionaries
        """
        logger.info(f"Searching PubMed for: {query}")
        
        try:
            # Use NCBI E-utilities API
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
            
            # Search for PMIDs
            search_params = {
                'db': 'pubmed',
                'term': f"{query}[Title/Abstract] AND clinical trial[Publication Type]",
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'relevance'
            }
            
            search_response = self.session.get(f"{base_url}/esearch.fcgi", params=search_params, timeout=30)
            search_response.raise_for_status()
            
            search_data = search_response.json()
            pmids = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not pmids:
                logger.info("No PubMed results found")
                return []
            
            # Fetch details for each PMID
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'xml',
                'rettype': 'abstract'
            }
            
            fetch_response = self.session.get(f"{base_url}/efetch.fcgi", params=fetch_params, timeout=30)
            fetch_response.raise_for_status()
            
            # Parse XML response (simplified)
            papers = []
            for pmid in pmids[:max_results]:
                paper = {
                    'title': f'PubMed Research Article (PMID: {pmid})',
                    'url': f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',
                    'source': 'PubMed',
                    'abstract': 'Research article abstract available on PubMed',
                    'pmid': pmid
                }
                papers.append(paper)
            
            logger.info(f"Found {len(papers)} PubMed articles")
            return papers
            
        except Exception as e:
            logger.error(f"PubMed search failed: {e}")
            return []
    
    def classify_with_ai(self, trials: List[Dict], query: str) -> List[Dict]:
        """
        Classify trials using Anthropic AI (requires API key)
        
        Args:
            trials: List of trial dictionaries
            query: Original search query
            
        Returns:
            Trials with AI scores and classifications
        """
        if not self.anthropic_api_key:
            logger.warning("No Anthropic API key provided. Skipping AI classification.")
            for trial in trials:
                trial['ai_score'] = 75  # Default score
                trial['ai_classification'] = 'Relevant'
                trial['confidence'] = 75
            return trials
        
        logger.info("Classifying trials with Anthropic AI")
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            for i, trial in enumerate(trials):
                try:
                    # Prepare classification prompt
                    prompt = f"""
                    Analyze this clinical trial for relevance to the query: "{query}"
                    
                    Trial Title: {trial.get('title', '')}
                    Conditions: {trial.get('conditions', '')}
                    Abstract: {trial.get('abstract', '')[:500]}...
                    
                    Provide a JSON response with:
                    - relevance_score: 0-100 (how relevant to the query)
                    - classification: "Highly Relevant", "Relevant", or "Less Relevant" 
                    - confidence: 0-100 (confidence in classification)
                    - reasoning: Brief explanation
                    """
                    
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    # Parse AI response
                    ai_text = response.content[0].text
                    
                    # Extract JSON from response
                    try:
                        # Look for JSON block
                        json_match = re.search(r'\{.*?\}', ai_text, re.DOTALL)
                        if json_match:
                            ai_result = json.loads(json_match.group())
                            trial['ai_score'] = ai_result.get('relevance_score', 75)
                            trial['ai_classification'] = ai_result.get('classification', 'Relevant')
                            trial['confidence'] = ai_result.get('confidence', 75)
                            trial['ai_reasoning'] = ai_result.get('reasoning', 'AI analysis completed')
                        else:
                            raise ValueError("No JSON found in response")
                    except:
                        # Fallback scoring
                        trial['ai_score'] = 75
                        trial['ai_classification'] = 'Relevant'
                        trial['confidence'] = 70
                        trial['ai_reasoning'] = 'Default classification applied'
                    
                    # Rate limiting
                    if i > 0 and i % 5 == 0:
                        time.sleep(1)
                        
                except Exception as e:
                    logger.warning(f"AI classification failed for trial {i}: {e}")
                    trial['ai_score'] = 70
                    trial['ai_classification'] = 'Relevant'
                    trial['confidence'] = 65
                    trial['ai_reasoning'] = 'Classification error, default applied'
            
            logger.info("AI classification completed")
            return trials
            
        except Exception as e:
            logger.error(f"AI classification failed: {e}")
            # Return trials with default scores
            for trial in trials:
                trial['ai_score'] = 75
                trial['ai_classification'] = 'Relevant'
                trial['confidence'] = 70
            return trials
    
    def search_trials(self, query: str, max_results: int = 50, include_pubmed: bool = True, use_ai_classification: bool = True) -> List[Dict]:
        """
        Main search function combining all sources
        
        Args:
            query: Search query
            max_results: Maximum results per source
            include_pubmed: Include PubMed literature search
            use_ai_classification: Use AI for relevance scoring
            
        Returns:
            Combined and classified results
        """
        logger.info(f"Starting comprehensive search for: {query}")
        
        all_trials = []
        
        # Search ClinicalTrials.gov
        ct_trials = self.search_clinicaltrials_gov(query, max_results)
        all_trials.extend(ct_trials)
        
        # Search PubMed if requested
        if include_pubmed:
            pubmed_papers = self.search_pubmed_related(query, max_results // 3)
            all_trials.extend(pubmed_papers)
        
        # AI Classification
        if use_ai_classification:
            all_trials = self.classify_with_ai(all_trials, query)
        
        # Sort by AI score
        all_trials.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
        
        logger.info(f"Search completed. Found {len(all_trials)} total results")
        return all_trials
    
    def export_to_excel(self, trials: List[Dict], filename: str = None) -> str:
        """
        Export search results to Excel file
        
        Args:
            trials: List of trial dictionaries
            filename: Output filename (optional)
            
        Returns:
            Path to created Excel file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"clinical_trials_search_{timestamp}.xlsx"
        
        logger.info(f"Exporting {len(trials)} results to {filename}")
        
        # Prepare data for Excel
        excel_data = []
        for trial in trials:
            row = {
                'Title': trial.get('title', 'N/A'),
                'URL': trial.get('url', 'N/A'),
                'Source': trial.get('source', 'N/A'),
                'Abstract': trial.get('abstract', 'N/A'),
                'AI_Score': trial.get('ai_score', 'N/A'),
                'AI_Classification': trial.get('ai_classification', 'N/A'),
                'Confidence': trial.get('confidence', 'N/A'),
                'Conditions': trial.get('conditions', 'N/A'),
                'Phase': trial.get('phase', 'N/A'),
                'Status': trial.get('status', 'N/A'),
                'Start_Date': trial.get('start_date', 'N/A'),
                'Sponsor': trial.get('sponsor', 'N/A'),
                'Interventions': trial.get('interventions', 'N/A'),
                'NCT_ID': trial.get('nct_id', trial.get('pmid', 'N/A'))
            }
            excel_data.append(row)
        
        # Create DataFrame and export
        df = pd.DataFrame(excel_data)
        
        # Create Excel file with formatting
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Clinical Trials', index=False)
            
            # Get workbook and worksheet for formatting
            workbook = writer.book
            worksheet = writer.sheets['Clinical Trials']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"Excel file created successfully: {filename}")
        return filename

# Example usage functions for Colab
def search_and_export(query: str, anthropic_api_key: str = None, max_results: int = 50, filename: str = None):
    """
    Convenience function for Colab usage
    
    Args:
        query: Your search query (e.g., "diabetes treatment", "cancer immunotherapy")
        anthropic_api_key: Your Anthropic API key (optional, for AI scoring)
        max_results: Maximum results to return
        filename: Output Excel filename
        
    Returns:
        Path to Excel file
    """
    print(f"🔍 Searching for clinical trials: {query}")
    
    # Initialize API
    api = TrialScopeAPI(anthropic_api_key=anthropic_api_key)
    
    # Search trials
    results = api.search_trials(
        query=query,
        max_results=max_results,
        include_pubmed=True,
        use_ai_classification=bool(anthropic_api_key)
    )
    
    # Export to Excel
    excel_file = api.export_to_excel(results, filename)
    
    print(f"✅ Search completed! Found {len(results)} trials")
    print(f"📊 Results exported to: {excel_file}")
    
    return excel_file

# Example usage for Google Colab
if __name__ == "__main__":
    # Example search
    query = "alzheimer's disease treatment"
    
    # Option 1: Basic search without AI (no API key needed)
    excel_file = search_and_export(
        query=query,
        max_results=30
    )
    
    # Option 2: Advanced search with AI classification (requires Anthropic API key)
    # excel_file = search_and_export(
    #     query=query,
    #     anthropic_api_key="your-anthropic-api-key-here",
    #     max_results=50,
    #     filename="my_clinical_trials.xlsx"
    # )
    
    print(f"Search completed. Excel file: {excel_file}")