import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical"
    " Facebook Group. Type in a search term, and it will return descriptions"
    " and links to the relevant Facebook posts."
)

# 1. Load your master text file
try:
  with open("master_archive.txt", "r", encoding="utf-8") as f:
    archive_lines = f.readlines()
except FileNotFoundError:
  archive_lines = []

# 2. Search Bar
query = st.text_input(
    "Enter a search term (e.g., 'headlight', 'fridge gas', 'split charge'):"
)

# 3. Local Search Logic
if query:
  terms = query.lower().split()

  # Match lines containing all typed search terms
  matches = [
      line.strip()
      for line in archive_lines
      if all(t in line.lower() for t in terms)
  ]

  if matches:
    st.markdown("### --- FILE MATCHES ---")
    for m in matches:
      # Convert URLs to mobile-safe permalinks
      clean_match = m.replace("www.facebook.com", "m.facebook.com").replace(
          "/posts/", "/permalink/"
      )
      st.write(clean_match)
  else:
    st.warning("No matches found for that term. Try a broader keyword.")
