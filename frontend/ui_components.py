import streamlit as st

def setup_page():
    """Set up the Streamlit page configuration"""
    st.set_page_config(
        page_title="BACTO_PEDIA - Comprehensive Bacteria Information",
        page_icon="🦠",
        layout="wide"
    )

def display_header():
    """Display the application header and description"""
    st.title("🦠 BACTO_PEDIA - Bacteria Information Assistant")
    st.markdown("""
    This bot provides detailed scientific information about bacteria. Simply enter the name of the bacteria you want to learn about!
    """)

def display_search_input():
    """Display the search input field"""
    return st.text_input(
        "Enter bacteria name:", 
        key="bacteria_input", 
        placeholder="Enter any bacteria name (e.g., Vibrio, E coli)..."
    )

def display_bacteria_info(info):
    """Display information about a bacteria"""
    st.success(f"Here's what I know about {info['name']}:")
    
    st.markdown("### Scientific Classification")
    st.write(info['scientific_classification'])
    
    st.markdown("### Detailed Information")
    st.write(info['description'])

def display_online_info(online_info):
    """Display information found online"""
    st.success(f"Here's what I found about {online_info['name']}:")
    
    st.markdown("### Description")
    st.write(online_info['description'])
    
    # Display source
    st.markdown("---")
    st.markdown(f"*Source: [{online_info['source']}]({online_info['url']})*")

def display_error(error_message):
    """Display error message"""
    st.error(error_message)

def display_examples():
    """Display example bacteria names"""
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
        - Vibrio cholerae
        """)

    with col3:
        st.markdown("""
        - Pseudomonas aeruginosa
        - Mycobacterium tuberculosis
        - Helicobacter pylori
        """)

def display_footer():
    """Display footer information"""
    st.markdown("---")
    st.markdown("""
    💡 **Note:** This bot combines a curated database with web searches to provide accurate information about bacteria.
    For best results, try using the scientific name of the bacteria.
    """)
