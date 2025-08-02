#!/usr/bin/env python3
"""
Command Line Interface for PubMed Paper Retrieval with Pharmaceutical/Biotech Company Affiliations

A CLI tool for searching research papers and identifying authors affiliated with pharmaceutical or biotech companies.
"""

import argparse
import sys
import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional, Dict, Any

from get_papers.pubmed_api import PubMedAPI
from get_papers.affiliation_analyzer import AffiliationAnalyzer


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch research papers with pharmaceutical/biotech company affiliations from PubMed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "cancer treatment"
  %(prog)s "COVID-19 vaccine" -f results.csv
  %(prog)s "diabetes research" -d -f diabetes_papers.csv
        """
    )
    
    # Required arguments
    parser.add_argument(
        'query',
        help='Search query for PubMed (supports full PubMed query syntax)'
    )
    
    # Optional arguments
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Print debug information during execution'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Specify the filename to save the results (CSV format). If not provided, print to console'
    )
    
    # Search options
    parser.add_argument(
        '--max-results',
        type=int,
        default=100,
        help='Maximum number of results to retrieve (default: 100)'
    )
    
    parser.add_argument(
        '--api-key',
        help='NCBI API key for higher rate limits'
    )
    
    parser.add_argument(
        '--email',
        help='Email address for NCBI (required for API key usage)'
    )
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()
    
    if args.debug:
        print(f"DEBUG: Searching PubMed for: {args.query}")
        print(f"DEBUG: Max results: {args.max_results}")
        print(f"DEBUG: Output file: {args.file}")
    
    # Initialize API client and analyzer
    try:
        api = PubMedAPI(api_key=args.api_key, email=args.email)
        analyzer = AffiliationAnalyzer()
    except Exception as e:
        print(f"Error initializing components: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Search for papers
        if args.debug:
            print("DEBUG: Searching PubMed...")
        
        search_results = api.search_papers(
            query=args.query,
            max_results=args.max_results
        )
        
        # Extract PMIDs
        pmids = search_results.get('esearchresult', {}).get('idlist', [])
        
        if not pmids:
            print("No papers found matching your query.")
            return
        
        if args.debug:
            print(f"DEBUG: Found {len(pmids)} papers")
            print(f"DEBUG: PMIDs: {pmids[:5]}...")
        
        # Fetch paper details using full fetch for better affiliation data
        if args.debug:
            print("DEBUG: Fetching paper details...")
        
        papers = []
        for pmid in pmids:
            try:
                # Use full fetch to get detailed author information
                paper_xml = api.fetch_paper_details(pmid, retmode="xml")
                papers.append({
                    'uid': pmid,
                    'xml_data': paper_xml
                })
                if args.debug:
                    print(f"DEBUG: Fetched PMID {pmid}")
            except Exception as e:
                if args.debug:
                    print(f"DEBUG: Error fetching PMID {pmid}: {e}")
                continue
        
        if args.debug:
            print(f"DEBUG: Successfully retrieved {len(papers)} papers")
        
        # Process papers to find pharmaceutical/biotech affiliations
        results = []
        
        for paper in papers:
            try:
                # Extract paper information from XML
                pmid = paper.get('uid', '')
                title = ''
                pubdate = ''
                
                if 'xml_data' in paper:
                    # Parse XML to get title and publication date
                    try:
                        root = ET.fromstring(paper['xml_data'])
                        article = root.find('.//Article')
                        if article is not None:
                            title_elem = article.find('.//ArticleTitle')
                            if title_elem is not None:
                                title = title_elem.text or ''
                            
                            # Get publication date
                            pub_date = root.find('.//PubDate')
                            if pub_date is not None:
                                year_elem = pub_date.find('Year')
                                month_elem = pub_date.find('Month')
                                if year_elem is not None:
                                    pubdate = year_elem.text or ''
                                    if month_elem is not None:
                                        pubdate = f"{month_elem.text} {pubdate}"
                    except Exception as e:
                        if args.debug:
                            print(f"DEBUG: Error parsing XML for PMID {pmid}: {e}")
                else:
                    # Fallback to summary data
                    paper_data = paper
                    if 'result' in paper and isinstance(paper['result'], dict):
                        for key, value in paper['result'].items():
                            if key != 'uids' and isinstance(value, dict):
                                paper_data = value
                                break
                    
                    title = paper_data.get('title', '')
                    pubdate = paper_data.get('pubdate', '')
                
                # Analyze affiliations
                authors, company_affiliations = analyzer.analyze_paper_affiliations(paper)
                
                # Only include papers with at least one pharma/biotech affiliation
                if company_affiliations:
                    # Get non-academic authors
                    non_academic_authors = analyzer.get_non_academic_authors(authors)
                    non_academic_names = [author.name for author in non_academic_authors]
                    
                    # Get company affiliations
                    company_names = [aff.company_name for aff in company_affiliations]
                    
                    # Get corresponding author email
                    corresponding_email = analyzer.get_corresponding_author_email(authors)
                    
                    # Create result row
                    result = {
                        'PubmedID': pmid,
                        'Title': title,
                        'Publication Date': pubdate,
                        'Non-academic Author(s)': '; '.join(non_academic_names) if non_academic_names else '',
                        'Company Affiliation(s)': '; '.join(company_names) if company_names else '',
                        'Corresponding Author Email': corresponding_email or ''
                    }
                    
                    results.append(result)
                    
                    if args.debug:
                        print(f"DEBUG: Found pharma affiliation in PMID {pmid}: {company_names}")
            
            except Exception as e:
                if args.debug:
                    print(f"DEBUG: Error processing paper: {e}")
                continue
        
        if not results:
            print("No papers found with pharmaceutical/biotech company affiliations.")
            return
        
        # Output results
        if args.file:
            # Write to CSV file
            write_csv_results(results, args.file)
            print(f"Results saved to: {args.file}")
            print(f"Total papers with pharma/biotech affiliations: {len(results)}")
        else:
            # Print to console
            print_csv_results(results)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        api.close()


def write_csv_results(results: List[Dict[str, str]], filename: str) -> None:
    """Write results to CSV file."""
    fieldnames = [
        'PubmedID', 'Title', 'Publication Date', 
        'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_csv_results(results: List[Dict[str, str]]) -> None:
    """Print results to console in CSV format."""
    fieldnames = [
        'PubmedID', 'Title', 'Publication Date', 
        'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
    ]
    
    # Print header
    print(','.join(fieldnames))
    
    # Print data rows
    for result in results:
        row = []
        for field in fieldnames:
            value = result.get(field, '')
            # Escape commas and quotes in CSV
            if ',' in value or '"' in value:
                value = f'"{value.replace('"', '""')}"'
            row.append(value)
        print(','.join(row))


if __name__ == "__main__":
    main() 