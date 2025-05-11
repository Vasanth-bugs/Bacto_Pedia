# BactoBot - Bacteria Information Assistant

## Overview
BactoBot is a Streamlit-based web application that provides detailed information about different types of bacteria. The application combines a local database with web scraping capabilities to deliver comprehensive bacterial information to users.

## Libraries Used

1. **Streamlit (`import streamlit as st`)**
   - Purpose: Creates the web interface and interactive elements
   - Features used:
     - `st.set_page_config()`: Configures the page layout and title
     - `st.title()`, `st.markdown()`: Displays formatted text
     - `st.text_input()`: Creates input field for bacteria names
     - `st.columns()`: Creates columnar layout
     - `st.spinner()`: Shows loading animation during searches
     - `st.success()`, `st.error()`: Displays success/error messages

2. **Requests (`import requests`)**
   - Purpose: Handles HTTP requests for web scraping
   - Used to fetch Wikipedia pages about bacteria

3. **BeautifulSoup (`from bs4 import BeautifulSoup`)**
   - Purpose: Parses HTML content from web pages
   - Used to extract relevant information from Wikipedia pages
   - Helps clean and format the scraped content

4. **Regular Expressions (`import re`)**
   - Purpose: Pattern matching and text cleaning
   - Used to remove reference numbers [1], [2], etc. from Wikipedia content

## Data Sources

1. **Local Database (`BACTERIA_DATABASE`)**
   - Custom-curated information about common bacteria
   - Currently includes detailed information for:
     - Vibrio
     - Escherichia coli (E. coli)
   - Information structure:
     - Scientific name
     - Classification
     - Key characteristics
     - Medical significance
     - Habitat
     - Prevention/importance
   - Sources: Information compiled from medical and microbiological resources

2. **Web Scraping (Wikipedia)**
   - Serves as a fallback when bacteria aren't in the local database
   - Process:
     1. Formats bacteria name for URL
     2. Fetches Wikipedia page
     3. Extracts first few paragraphs
     4. Cleans content (removes references, etc.)
     5. Returns formatted information

## Code Structure

1. **Configuration and Setup**
   ```python
   st.set_page_config(
       page_title="BactoBot - Comprehensive Bacteria Information",
       page_icon="🦠",
       layout="wide"
   )
   ```
   - Sets up the page layout and configuration

2. **Local Database**
   ```python
   BACTERIA_DATABASE = {
       "bacteria_name": {
           "name": "Scientific Name",
           "scientific_classification": "Classification details",
           "description": "Detailed information..."
       }
   }
   ```
   - Dictionary containing curated information about common bacteria

3. **Web Scraping Function**
   ```python
   def search_bacteria_online(bacteria_name):
       # Searches Wikipedia for bacteria information
       # Returns formatted data or None if not found
   ```
   - Handles online searches when local database doesn't have information

4. **User Interface**
   - Input field for bacteria names
   - Information display sections
   - Example suggestions
   - Error handling and feedback

## How It Works

1. **User Input Processing**
   - User enters a bacteria name
   - Input is converted to lowercase for matching

2. **Information Retrieval**
   - First checks local database
   - If not found, attempts web scraping
   - Returns formatted information or error message

3. **Display**
   - Shows information in organized sections
   - Includes source attribution for web-scraped content
   - Provides example suggestions for users

## Running the Application

1. **Requirements**
   ```bash
   pip install streamlit requests beautifulsoup4
   ```

2. **Launch**
   ```bash
   streamlit run bactobot.py
   ```

## Future Improvements

1. **Database Expansion**
   - Add more bacteria to the local database
   - Include more detailed classifications
   - Add images and diagrams

2. **Features**
   - Advanced search capabilities
   - Filtering by bacteria types
   - Comparison tools
   - Interactive visualizations

3. **Data Sources**
   - Integration with scientific databases
   - Real-time updates from research papers
   - Multiple source verification

## Notes
- The local database provides faster and more reliable information
- Web scraping serves as a backup for less common bacteria
- Information is presented in a user-friendly format
- The application is designed to be educational and informative

## Disclaimer
Web-scraped information should be verified with official scientific sources for research or medical purposes.
