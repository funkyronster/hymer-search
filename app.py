import re
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical Facebook Group. "
    "Type in a search term, and it will return descriptions and links to the relevant Facebook posts."
)

# 1. Load your master text file
try:
    with open("master_archive.txt", "r", encoding="utf-8") as f:
        archive_text = f.read()
        # Split into distinct blocks if entries are separated by blank lines, otherwise line-by-line
        raw_entries = archive_text.split("\n\n") if "\n\n" in archive_text else archive_text.splitlines()
except FileNotFoundError:
    raw_entries = []

# 2. Search Bar
query = st.text_input("Enter a search term (e.g., 'headlight', 'fridge gas', 'split charge'):")

# 3. Local Search & Clickable Link Formatter
if query:
    terms = query.lower().split()
    
    # Match entries containing all typed search terms
    matches = [
        entry.strip() 
        for entry in raw_entries 
        if entry.strip() and all(t in entry.lower() for t in terms)
    ]
    
    if matches:
        st.markdown("### --- FILE MATCHES ---")
        for m in matches:
            # Convert URLs to mobile-friendly permalinks
            clean_entry = (
                m.replace("www.facebook.com", "m.facebook.com")
                 .replace("/posts/", "/permalink/")
            )
            
            # Format URLs as clear, tap-friendly markdown links
            clickable_entry = re.sub(
                r"(https?://\S+)", 
                r"[👉 **Open Facebook Post**](\1)", 
                clean_entry
            )
            
            st.markdown(clickable_entry)
            st.divider()
    else:
        st.warning("No matches found for that term. Try a broader keyword.")
