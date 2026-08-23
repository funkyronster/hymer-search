import re
import urllib.parse
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical Facebook Group. "
    "Type in a search term, and it will return descriptions and links to the relevant Facebook posts."
)

# 1. Parse master_archive.txt into [Title, URL] pairs
records = []
try:
    with open("master_archive.txt", "r", encoding="utf-8") as f:
        content = f.read()

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
                title = line

        if url and title:
            records.append((title, url))

except FileNotFoundError:
    records = []

# 2. Search Bar
query = st.text_input("Enter a search term (e.g., 'rooflight', 'fridge gas', 'split charge'):")

# 3. Match and Render
if query:
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
            st.markdown(f"**{title}**")

            # Check if it is a Facebook link or an external link (Google Drive / Blog / Web)
            if "facebook.com" in url:
                encoded_url = urllib.parse.quote(url, safe="")
                fb_app_url = f"fb://facewebmodal/f?href={encoded_url}"
                clean_web_url = url.replace("www.facebook.com", "m.facebook.com")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"[📱 **Open in Facebook App**]({fb_app_url})")
                with col2:
                    st.markdown(f"[🌐 **Open in Browser**]({clean_web_url})")
            else:
                st.markdown(f"[👉 **Open Link**]({url})")

            st.divider()
    else:
        st.warning("No matches found for that term. Try a broader keyword.")
