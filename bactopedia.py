import requests
from bs4 import BeautifulSoup
import re
from difflib import get_close_matches

from database import BACTERIA_DATABASE
from frontend import (
    setup_page,
    display_header,
    display_search_input,
    display_bacteria_info,
    display_online_info,
    display_error,
    display_examples,
    display_footer
)

def get_bacteria_info(input_name, database=BACTERIA_DATABASE):
    """
    Search for bacteria in database using name or common names with flexible matching
    """
    input_lower = input_name.lower().strip()
    input_nodots = input_lower.replace(".", "").strip()
    
    for key, info in database.items():
        # Check common names first since they include variations
        if 'common_names' in info:
            for name in info['common_names']:
                name_lower = name.lower()
                # Simple substring match
                if input_lower in name_lower:
                    return info
                # Try matching without dots
                name_nodots = name_lower.replace(".", "").strip()
                if input_nodots in name_nodots:
                    return info
                    
        # Then check the key and display name
        if input_lower in key.lower() or input_lower in info['name'].lower():
            return info
    
    return None

def get_similar_bacteria(input_name, database=BACTERIA_DATABASE):
    """
    Find similar bacteria names from the database using fuzzy matching
    """
    input_lower = input_name.lower()
    
    # Create a list of all bacteria names (including variations)
    all_names = []
    for key, info in database.items():
        all_names.append(key)
        if 'common_names' in info:
            all_names.extend(info['common_names'])
    
    # Get close matches
    matches = get_close_matches(input_lower, all_names, n=3, cutoff=0.6)
    return matches

def is_bacteria_related(query):
    """
    Check if the query appears to be bacteria-related
    """
    # Common bacteria-related terms and suffixes
    bacteria_terms = [
        'bacteria', 'bacterium', 'bacillus', 'coccus', 'vibrio', 
        'streptococcus', 'staphylococcus', 'mycobacterium', 'clostridium',
        'lactobacillus', 'pseudomonas', 'escherichia', 'helicobacter'
    ]
    
    # Common scientific name patterns
    scientific_patterns = [
        r'\w+\s+\w+',  # Two-word scientific names
        r'[A-Z]\.\s*\w+',  # Abbreviated genus (e.g., "E. coli")
    ]
    
    query_lower = query.lower()
    
    # Check if query contains any bacteria-related terms
    if any(term in query_lower for term in bacteria_terms):
        return True
        
    # Check if query matches scientific name patterns
    if any(re.match(pattern, query, re.IGNORECASE) for pattern in scientific_patterns):
        return True
        
    # Check if query exists in our bacteria database
    if any(query_lower in key.lower() or 
           any(query_lower in common.lower() for common in info.get('common_names', []))
           for key, info in BACTERIA_DATABASE.items()):
        return True
        
    return False

def validate_input(bacteria_name):
    """
    Validate user input and return appropriate error messages
    """
    if not bacteria_name or bacteria_name.isspace():
        return False, "Please enter a bacteria name."
    
    # Check for numbers or special characters
    if any(char.isdigit() for char in bacteria_name):
        return False, "Bacteria names typically don't contain numbers. Please check your input."
    
    if re.search(r'[^a-zA-Z\s\.-]', bacteria_name):
        return False, "Invalid characters detected. Bacteria names usually only contain letters, spaces, dots, and hyphens."
    
    # Check if the query appears to be bacteria-related
    if not is_bacteria_related(bacteria_name):
        return False, "Please enter a valid bacteria name. Your query doesn't appear to be related to bacteria."
    
    return True, None

def search_bacteria_online(bacteria_name):
    """
    Search for bacteria information online using Wikipedia API
    """
    try:
        # Add "bacteria" to the search query if it's not already present
        search_term = bacteria_name
        if "bacteria" not in bacteria_name.lower():
            search_term = f"{bacteria_name} bacteria"
            
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_term,
            "utf8": 1
        }
        
        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()
        
        if "query" in search_data and search_data["query"]["search"]:
            # Get the first result's page ID
            page_id = search_data["query"]["search"][0]["pageid"]
            
            # Get the actual content
            content_params = {
                "action": "query",
                "format": "json",
                "pageids": page_id,
                "prop": "extracts|info",
                "exintro": True,
                "explaintext": True,
                "inprop": "url"
            }
            
            content_response = requests.get(search_url, params=content_params)
            content_data = content_response.json()
            
            if "query" in content_data and "pages" in content_data["query"]:
                page = content_data["query"]["pages"][str(page_id)]
                if "extract" in page and page["extract"].strip():
                    # Verify the content is bacteria-related
                    content_lower = page["extract"].lower()
                    bacteria_indicators = [
                        'bacteria', 'bacterium', 'gram-positive', 'gram-negative',
                        'species', 'genus', 'pathogen', 'microorganism',
                        'strain', 'culture', 'colony'
                    ]
                    
                    if any(indicator in content_lower for indicator in bacteria_indicators):
                        return {
                            "name": page.get("title", bacteria_name.title()),
                            "description": page["extract"],
                            "source": "Wikipedia",
                            "url": page.get("fullurl", f"https://en.wikipedia.org/?curid={page_id}")
                        }
    except Exception as e:
        display_error(f"Error searching online: {str(e)}")
    return None

def main():
    """Main application logic"""
    # Set up the page
    setup_page()
    display_header()

    # Get user input
    user_input = display_search_input()

    # Handle user input
    if user_input:
        # First check local database
        info = get_bacteria_info(user_input)
        
        if info:
            display_bacteria_info(info)
        else:
            # If not in database, search online
            online_info = search_bacteria_online(user_input)
            
            if online_info:
                display_online_info(online_info)
            else:
                # Get validation result
                is_valid, error_message = validate_input(user_input)
                if not is_valid:
                    display_error(error_message)
                else:
                    # Find similar bacteria names
                    similar_names = get_similar_bacteria(user_input)
                    
                    error_message = "Sorry, I couldn't find information about that bacteria."
                    
                    if similar_names:
                        error_message += "\n\nDid you mean one of these?"
                        for name in similar_names:
                            error_message += f"\n- {name.title()}"
                    
                    error_message += "\n\nSuggestions:"
                    error_message += "\n- Check the spelling"
                    error_message += "\n- Try using the scientific name (e.g., 'Escherichia coli' instead of 'E coli')"
                    error_message += "\n- Try one of the example bacteria listed below"
                    
                    display_error(error_message)

    # Display examples and footer
    display_examples()
    display_footer()

if __name__ == "__main__":
    main()
