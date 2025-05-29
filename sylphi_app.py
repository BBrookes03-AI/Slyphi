
import streamlit as st
import openai

st.set_page_config(page_title="Sylphi - Your Research Credibility Assistant", layout="centered")

st.title("📚 Sylphi – Your Research Credibility Assistant")
st.write("Welcome to Sylphi! Enter a topic to find peer-reviewed sources, or paste a source title to evaluate its credibility.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Section 1: Search for Peer-Reviewed Articles
st.subheader("🔍 Find Peer-Reviewed Articles")
topic = st.text_input("Enter your topic (e.g., 'AI in education'):")

if topic:
    with st.spinner("Searching academic databases..."):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a university research librarian."},
                {"role": "user", "content": f"List 3 peer-reviewed academic articles about {topic}. For each, give the title, author(s), year, journal, and a 1-sentence summary."}
            ]
        )
        st.markdown("### 📝 Search Results:")
        st.write(response.choices[0].message.content)

# Section 2: Credibility Check
st.subheader("✅ Check Source Credibility")
source_title = st.text_area("Paste the title or link of a source to evaluate its credibility:")

if source_title:
    with st.spinner("Evaluating source..."):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an academic integrity expert."},
                {"role": "user", "content": f"Evaluate the credibility of this source: {source_title}. Is it peer-reviewed? Who is the author? Is it a scholarly publication? Return your analysis in 3-4 bullet points."}
            ]
        )
        st.markdown("### 🔎 Credibility Report:")
        st.write(response.choices[0].message.content)

# Section 3: Citation Helper
st.subheader("📌 Generate APA/MLA Citation")
citation_input = st.text_area("Enter article details (title, author, journal, year):")
citation_style = st.radio("Select Citation Style:", ["APA", "MLA"])

if citation_input:
    with st.spinner("Formatting citation..."):
        citation_prompt = f"Format the following source in {citation_style} style: {citation_input}"
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a citation formatting expert."},
                {"role": "user", "content": citation_prompt}
            ]
        )
        st.markdown("### 🧾 Citation Output:")
        st.code(response.choices[0].message.content)
