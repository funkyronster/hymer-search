import difflib
import re
import streamlit as st

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This search contains the entire index of the Classic Hymers Technical"
    " Facebook Group. Type in a search term, and it will return descriptions"
    " and links to the relevant Facebook posts."
)

# 1. Load archive and parse cleanly
records = []
try:
  with open("master_archive.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

  # Split into blocks separated by blank lines
  blocks = re.split(r"\n\s*\n", raw_text)

  for block in blocks:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
      continue

    url_match = None
    desc_lines = []

    for l in lines:
      if "http://" in l or "https://" in l or "facebook.com" in l:
        found = re.search(r"(https?://\S+)", l)
        url_match = found.group(1) if found else l
      else:
        desc_lines.append(l)

    if url_match:
      title = desc_lines[0] if desc_lines else "Facebook Post"
      # Store full text for searching, but display only the title
      search_context = " ".join(desc_lines)
      records.append((title, search_context, url_match))

except FileNotFoundError:
  records = []

# 2. Search Bar
query = st.text_input(
    "Enter a search term (e.g., 'rooflight', 'fridge gas', 'split charge'):"
)

# 3. Search & Render Clean Title + Link Only
if query:
  search_terms = query.lower().split()
  matches = []

  for title, search_context, url in records:
    full_searchable = f"{title} {search_context}".lower()

    all_matched = True
    for term in search_terms:
      if term in full_searchable:
        continue
      words_in_text = re.findall(r"\w+", full_searchable)
      close_matches = difflib.get_close_matches(
          term, words_in_text, n=1, cutoff=0.75
      )
      if not close_matches:
        all_matched = False
        break

    if all_matched:
      matches.append((title, url))

  if matches:
    st.markdown(f"### Found {len(matches)} result(s):")
    for title, url in matches:
      clean_url = url.replace("www.facebook.com", "m.facebook.com").replace(
          "/posts/", "/permalink/"
      )

      st.markdown(f"**{title}**")
      st.markdown(f"[👉 Open Facebook Post]({clean_url})")
      st.divider()
  else:
    st.warning("No matches found for that term. Try a broader keyword.")
