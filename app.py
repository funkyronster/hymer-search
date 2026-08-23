import re
import urllib.parse
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "Search the Classic Hymers Technical Facebook Group index by keyword. "
    "Type a search term below to find specific guides and discussions."
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
query = st.text_input("Enter a search term (e.g., 'rooflight', 'fridge gas', 'curtain hooks'):")

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

            if "facebook.com" in url:
                # 1. Direct clean URL
                clean_url = url.replace("m.facebook.com", "www.facebook.com")
                
                # 2. Fallback Group Search URL (100% reliable on iOS inside Facebook app)
                # Encodes the exact post title to search within group 297054424534823
                encoded_search = urllib.parse.quote(title)
                search_fallback_url = f"https://www.facebook.com/groups/297054424534823/search/?q={encoded_search}"

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f'<a href="{clean_url}" target="_blank" rel="noopener noreferrer">👉 <b>Open Post</b></a>',
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.markdown(
                        f'<a href="{search_fallback_url}" target="_blank" rel="noopener noreferrer">🔍 <b>Find in Group</b></a>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f'<a href="{url}" target="_blank" rel="noopener noreferrer">👉 <b>Open Link</b></a>',
                    unsafe_allow_html=True,
                )

            st.divider()
    else:
        st.warning("No matches found for that term. Try a broader keyword.")
