import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical Facebook Group. "
    "Type in a search term, and it will return descriptions and links to the relevant Facebook posts."
)

# 1. Load archive and parse into [Description, URL] pairs
records = []
try:
    with open("master_archive.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if the next line is a URL
        if i + 1 < len(lines) and ("facebook.com" in lines[i+1] or "http" in lines[i+1]):
            records.append((line, lines[i+1]))
            i += 2
        # Or if the current line itself contains the URL
        elif "facebook.com" in line or "http" in line:
            records.append(("Post Link", line))
            i += 1
        else:
            i += 1
except FileNotFoundError:
    records = []

# 2. Search Bar
query = st.text_input("Enter a search term (e.g., 'headlight', 'fridge gas', 'split charge'):")

# 3. Search & Render Clean Pairs
if query:
    terms = query.lower().split()
    matches = [
        (desc, url) for desc, url in records
        if all(t in desc.lower() for t in terms)
    ]
    
    if matches:
        st.markdown("### --- SEARCH RESULTS ---")
        for desc, url in matches:
            # Clean mobile URL
            clean_url = url.replace("www.facebook.com", "m.facebook.com").replace("/posts/", "/permalink/")
            
            # Display Title and Link cleanly
            st.markdown(f"**{desc}**")
            st.markdown(f"[👉 Open Facebook Post]({clean_url})")
            st.divider()
    else:
        st.warning("No matches found for that term. Try a broader keyword.")
