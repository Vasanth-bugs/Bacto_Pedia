import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# Local database of common bacteria
BACTERIA_DATABASE = {
    "vibrio": {
        "name": "Vibrio",
        "scientific_classification": "Genus of Gram-negative bacteria in the family Vibrionaceae",
        "description": """
Vibrio is a genus of Gram-negative bacteria, several species of which can cause foodborne infection, usually associated with eating undercooked seafood.

Key characteristics:
- Shape: Curved rods
- Motility: Highly motile with polar flagella
- Habitat: Primarily aquatic environments, especially marine and brackish waters
- Notable species: V. cholerae (causes cholera), V. vulnificus, V. parahaemolyticus

Medical significance:
- V. cholerae causes cholera, a severe diarrheal disease
- V. vulnificus can cause wound infections and septicemia
- V. parahaemolyticus is associated with seafood-borne gastroenteritis

Prevention:
- Proper cooking of seafood
- Avoiding raw or undercooked seafood
- Clean water consumption
- Proper hand hygiene
        """
    },
    "e coli": {
        "name": "Escherichia coli",
        "scientific_classification": "Species of Gram-negative bacteria in the family Enterobacteriaceae",
        "description": """
Escherichia coli (E. coli) is a diverse group of bacteria commonly found in the intestines of humans and animals.

Key characteristics:
- Shape: Rod-shaped
- Type: Gram-negative
- Habitat: Gut microbiota of warm-blooded organisms
- Metabolism: Facultative anaerobe

Medical significance:
- Most strains are harmless and part of normal gut flora
- Some strains can cause food poisoning
- Can cause urinary tract infections
- Certain strains produce Shiga toxin

Research importance:
- Model organism in microbiology
- Used in biotechnology
- Important in genetic studies
        """
    }
}

def search_bacteria_online(bacteria_name):
    """
    Search for bacteria information online using Wikipedia as a fallback
    """
    try:
        # Format the bacteria name for URL
        formatted_name = bacteria_name.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{formatted_name}_bacteria"
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the first few paragraphs of content
            paragraphs = soup.find_all('p')
            main_content = []
            
            for p in paragraphs[:3]:  # Get first 3 paragraphs
                if p.text.strip() and not p.find('class="coordinates"'):
                    # Clean up the content
                    text = re.sub(r'\[\d+\]', '', p.text.strip())  # Remove reference numbers
                    if text:
                        main_content.append(text)
            
            if main_content:
                return {
                    "name": bacteria_name.title(),
                    "description": "\n\n".join(main_content),
                    "source": "Wikipedia",
                    "url": url
                }
    except Exception as e:
        st.error(f"Error searching online: {str(e)}")
    return None

# Set up the Streamlit page
st.set_page_config(
    page_title="BactoBot - Comprehensive Bacteria Information",
    page_icon="🦠",
    layout="wide"
)

# Add title and description
st.title("🦠 BactoBot - Bacteria Information Assistant")
st.markdown("""
This bot provides detailed scientific information about bacteria. Simply enter the name of the bacteria you want to learn about!
""")

# Create the input field
user_input = st.text_input("Enter bacteria name:", key="bacteria_input", placeholder="Enter any bacteria name (e.g., Vibrio, E coli)...")

# Handle user input
if user_input:
    with st.spinner(f'Searching for information about {user_input}...'):
        # First check local database
        info = BACTERIA_DATABASE.get(user_input.lower())
        
        if info:
            st.success(f"Here's what I know about {info['name']}:")
            
            st.markdown("### Scientific Classification")
            st.write(info['scientific_classification'])
            
            st.markdown("### Detailed Information")
            st.write(info['description'])
            
        else:
            # If not in database, search online
            online_info = search_bacteria_online(user_input)
            
            if online_info:
                st.success(f"Here's what I found about {online_info['name']}:")
                
                st.markdown("### Description")
                st.write(online_info['description'])
                
                # Display source
                st.markdown("---")
                st.markdown(f"*Source: [{online_info['source']}]({online_info['url']})*")
                
            else:
                st.error("""
                Sorry, I couldn't find information about that bacteria. Please:
                - Check the spelling
                - Try using the scientific name
                - Try one of the example bacteria below
                """)

# Add some example suggestions
st.markdown("---")
st.markdown("**Try these example bacteria names:**")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    - Escherichia coli
    - Staphylococcus aureus
    - Streptococcus pneumoniae
    """)

with col2:
    st.markdown("""
    - Bacillus subtilis
    - Lactobacillus acidophilus
    - Vibrio
    """)

with col3:
    st.markdown("""
    - Pseudomonas aeruginosa
    - Mycobacterium tuberculosis
    - Helicobacter pylori
    """)

# Add footer with information
st.markdown("---")
st.markdown("""
💡 **Note:** This bot combines a curated database with web searches to provide accurate information about bacteria.
For best results, try using the scientific name of the bacteria.
""")
