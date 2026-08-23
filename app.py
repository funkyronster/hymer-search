import re
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

            # Extract group ID and post/permalink ID
            fb_match = re.search(r'facebook\.com/groups/(\d+)/(?:posts|permalink)/(\d+)', url)
            
            if fb_match:
                group_id = fb_match.group(1)
                post_id = fb_match.group(2)
                # Native iOS and Android direct deep-link scheme
                native_fb_url = f"fb://group/{group_id}?post_id={post_id}"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<a href="{native_fb_url}">📱 <b>Open in Facebook App</b></a>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<a href="{url}" target="_blank" rel="noopener noreferrer">🌐 <b>Open Web Link</b></a>', unsafe_allow_html=True)
            else:
                st.markdown(f'<a href="{url}" target="_blank" rel="noopener noreferrer">👉 <b>Open Link</b></a>', unsafe_allow_html=True)

            st.divider()
    else:
        st.warning("No matches found for that term. Try a broader keyword.")
