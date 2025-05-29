
import streamlit as st
import openai
import os

# Setup the page
st.set_page_config(page_title="Sylphi – Research Credibility Assistant", layout="centered")
st.title("📚 Sylphi – Your Research Credibility Assistant")
st.write("Use Sylphi to locate credible academic sources and verify if a source is peer-reviewed.")

# Securely load the API key
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# Section 1: Search for Peer-Reviewed Articles
st.subheader("🔍 Find Peer-Reviewed Articles")
topic = st.text_input("Enter a topic to search academic literature (e.g., 'AI in education'):")

# Define prompts BEFORE the API call
system_prompt = (
    "You are a university research librarian helping students locate real, peer-reviewed academic sources. "
    "Only return academic journal articles that are verifiable and have working URLs. Prefer open-access links from sites like doaj.org, pubmed.ncbi.nlm.nih.gov, eric.ed.gov, or arxiv.org. "
    "Avoid broken links, placeholders, or guessed DOIs. Each source must be authentic and link to the full article or abstract page. "
    "Respond in structured format as follows."
)

user_prompt_template = (
    "List 3 peer-reviewed academic articles about {topic}. For each, follow this format:\n"
    "1. Title: [Article Title]\n"
    "   Author(s): [Name(s)]\n"
    "   Year: [Year]\n"
    "   Journal: [Journal Name]\n"
    "   Summary: [1–2 sentence summary]\n"
    "   Link: [Working, verified URL]"
)

if topic:
    with st.spinner("Searching scholarly databases..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt_template.format(topic=topic)}
                ]
            )
            st.markdown("### 📝 Results:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ An error occurred while contacting OpenAI: {e}")

# Section 2: Credibility Check
st.subheader("✅ Check Source Credibility")
source_title = st.text_area("Paste a source title or link to evaluate credibility:")

if source_title:
    with st.spinner("Evaluating source credibility..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an academic integrity expert evaluating sources."},
                    {"role": "user", "content": f"Evaluate the credibility of this source: {source_title}. Respond with whether it's peer-reviewed, author credentials, publication quality, and citation practices."}
                ]
            )
            st.markdown("### 🔍 Credibility Report:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ An error occurred while evaluating the source: {e}")

# Section 3: Citation Generator
st.subheader("📌 Format APA/MLA Citation")
citation_input = st.text_area("Paste source details (title, author, journal, year):")
citation_style = st.radio("Select citation style:", ["APA", "MLA"])

if citation_input:
    with st.spinner("Formatting your citation..."):
        try:
            citation_prompt = f"Format this in {citation_style} style: {citation_input}"
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a citation formatting expert."},
                    {"role": "user", "content": citation_prompt}
                ]
            )
            st.markdown("### 🧾 Citation Output:")
            st.code(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ An error occurred while generating the citation: {e}")
