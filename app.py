import re
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical"
    " Facebook Group. Type in a search term, and it will return descriptions"
    " and links to the relevant Facebook posts."
)

# 1. Parse master_archive.txt into strict [Title, URL] pairs
records = []
try:
  with open("master_archive.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

  for idx, line in enumerate(lines):
    # Whenever a line contains a URL, pair it with the line directly above it
    if "http://" in line or "https://" in line or "facebook.com" in line:
      url_match = re.search(r"(https?://\S+)", line)
      url = url_match.group(1) if url_match else line

      # The title is the preceding line (if it wasn't also a URL)
      if (
          idx > 0
          and not lines[idx - 1].startswith("http")
          and "facebook.com" not in lines[idx - 1]
      ):
        title = lines[idx - 1]
      else:
        title = "Facebook Post"

      records.append((title, url))

except FileNotFoundError:
  records = []

# 2. Search Bar
query = st.text_input(
    "Enter a search term (e.g., 'rooflight', 'fridge gas', 'split charge'):"
)

# 3. Match against Title & Display Clean Results
if query:
  # Split query into words so 'big rooflight' or 'roof light' works
  search_terms = query.lower().replace("roof light", "rooflight").split()

  matches = []
  for title, url in records:
    searchable_title = title.lower().replace("roof light", "rooflight")
    if all(term in searchable_title for term in search_terms):
      matches.append((title, url))

  if matches:
    st.markdown(f"### Found {len(matches)} result(s):")
    for title, url in matches:
      # Format for mobile-safe permalink
      clean_url = url.replace("www.facebook.com", "m.facebook.com").replace(
          "/posts/", "/permalink/"
      )

      st.markdown(f"**{title}**")
      st.markdown(f"[👉 Open Facebook Post]({clean_url})")
      st.divider()
  else:
    st.warning("No matches found for that term. Try a broader keyword.")
