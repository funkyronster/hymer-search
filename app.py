import re
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "Search the Classic Hymers Technical Facebook Group archive.\n\n"
    "📱 *Tip:* Open this page in Safari or Chrome for seamless post links."
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
                clean_title_js = title.replace("'", "\\'")
                copy_button_html = f"""
                <button onclick="navigator.clipboard.writeText('{clean_title_js}'); alert('Title copied to clipboard!');" 
                        style="background-color:#f0f2f6; border:1px solid #d0d4dc; border-radius:4px; padding:3px 8px; font-size:12px; cursor:pointer; margin-left:10px;">
                    📋 Copy Title
                </button>
                """
                st.markdown(
                    f'<a href="{url}" target="_blank" rel="noopener noreferrer">👉 <b>Open Facebook Post</b></a> {copy_button_html}',
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
