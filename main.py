import streamlit as st
import importlib.util
import os
import sys
import pandas as pd

# Dynamic import utility
def dynamic_import(module_name, path):
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load external modules
base_dir = os.path.dirname(__file__)
scraper = dynamic_import("scraper", os.path.join(base_dir, "scraper.py"))
parser = dynamic_import("parse", os.path.join(base_dir, "parse.py"))
visualizer = dynamic_import("visualizer", os.path.join(base_dir, "visualizer.py"))
ollama_handler = dynamic_import("ollama_handler", os.path.join(base_dir, "ollama_handler.py"))

st.set_page_config(page_title="AI Web & Doc Scraper", layout="wide")
st.title("🕷️ AI Web and Doc Scraper with Visualizer")

# Input section
url = st.text_input("🔗 Enter the URL to scrape (linked pages also included):")
doc_file = st.file_uploader("📄 Or upload a document (PDF, DOCX, XML, CSV):", type=["pdf", "docx", "xml", "csv"])

# Session state
if "context" not in st.session_state:
    st.session_state.context = ""
if "html" not in st.session_state:
    st.session_state.html = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""

# Scrape from URL
if st.button("Scrape the website") and url:
    with st.spinner("Scraping website and linked pages..."):
        html = scraper.scrape_website(url)
        parsed = parser.parse_html(html)
    if parsed.strip():
        st.session_state.context = parsed
        st.session_state.html = html
        st.success("✅ Website (and linked pages) scraped successfully!")
    else:
        st.warning("⚠️ No readable content found.")

# Parse uploaded file
if doc_file:
    file_type = doc_file.name.split('.')[-1].lower()
    with st.spinner("Processing uploaded document..."):
        parsed = parser.parse_document(doc_file, file_type)
    if parsed.strip():
        st.session_state.context = parsed
        st.success("✅ Document parsed successfully!")
    else:
        st.warning("⚠️ Document content empty or unsupported.")

# Ask Question
question = st.text_input("❓ Ask a question about the content:")

if st.button("Ask"):
    context = st.session_state.context.strip()
    if not context:
        st.warning("❗ No context available. Scrape a site or upload a document first.")
    else:
        with st.spinner("Sending query to Ollama..."):
            answer = ollama_handler.ask_ollama(question, context)
        st.session_state.answer = answer
        st.success("✅ Answer received!")

# Display LLM Answer
answer = st.session_state.get("answer", "").strip()
if answer:
    st.markdown("### 🤖 LLM Answer")
    df = visualizer.extract_table_from_text(answer)
    if df is not None:
        st.success("📋 Table detected and parsed.")
        st.dataframe(df)
        visualizer.show_graphs(df)
    else:
        st.markdown(f"**Answer:**\n\n{answer}")
