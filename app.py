import streamlit as st
from google import genai

st.set_page_config(page_title="Classic Hymer Archive Search", layout="centered")

st.title("Classic Hymer Technical Archive Search")

st.info(
    "This AI search contains the entire index of the Classic Hymers Technical Facebook Group. "
    "Type in a search term, and it will return descriptions and links to the Facebook posts that are relevant."
)

# 1. Load your master text file
try:
    with open("master_archive.txt", "r", encoding="utf-8") as f:
        archive_data = f.read()
except FileNotFoundError:
    archive_data = "No archive data found."

# 2. System Instruction
system_instruction = f"""
You are a precise technical group assistant. Your task is to look up the user's query in the attached document for exact matches. Output these strictly inside a Markdown code box labeled "--- FILE MATCHES ---". Inside this box, list only the descriptions and URLs found in the file. No conversational text outside the box.

DOCUMENT DATA:
{archive_data}
"""

# 3. Setup API Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 4. Search Bar
query = st.text_input("Enter a search term (e.g., 'headlight', 'fridge gas', 'split charge'):")

if query:
    with st.spinner("Searching archive..."):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=query,
                config={"system_instruction": system_instruction}
            )
            
            # Automatically format links to avoid the iOS blank "Story" redirect error
            clean_output = (
                response.text
                .replace("www.facebook.com", "m.facebook.com")
                .replace("/posts/", "/permalink/")
            )
            
            st.markdown(clean_output)
            
        except Exception as e:
            st.error(f"Error fetching results: {e}")
