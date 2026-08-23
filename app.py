import re
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical Facebook Group. "
    "Type in a search term, and it will return descriptions and links to the relevant Facebook posts."
)

# 1. Parse master_archive.txt cleanly into [Title, URL] pairs
records = []
try:
    with open("master_archive.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Split by blank lines to isolate entries cleanly
    blocks = re.split(r'\n\s*\n', content)

    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue

        url = None
        title = None

        for line in lines:
            if "facebook.com" in line or "http://" in line or "https://" in line:
                match = re.search(r'(https?://\S+)', line)
                url = match.group(1) if match else line
            elif title is None:
                # First non-URL line in the block is always the primary headline
                title = line

        if url and title:
            records.append((title, url))

except FileNotFoundError:
    records = []

# 2. Search Bar
query = st.text_input("Enter a search term (e.g., 'rooflight', 'fridge gas', 'split charge'):")

# 3. Search & Display Results
if query:
    # Treat 'roof light' and 'rooflight' identically
    norm_query = query.lower().replace("roof light", "rooflight")
    terms = norm_query.split()

    matches = []
    for title, url in records:
        norm_title = title.lower().replace("roof light", "rooflight")
        if all(t in norm_title for t in terms):
            matches.append((title, url))

    if matches:
        st.markdown(f"### Found {len(matches)} result(s):")
        for title, url in matches:
            clean_url = (
                url.replace("www.facebook.com", "m.facebook.com")
                   .replace("/posts/", "/permalink/")
            )
            st.markdown(f"**{title}**")
            st.markdown(f"[👉 Open Facebook Post]({clean_url})")
            st.divider()
    else:
        st.warning("No matches found for that term. Try a broader keyword.")
