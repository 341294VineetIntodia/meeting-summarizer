import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="AI Meeting Summarizer", page_icon="📝")

st.title("📝 Meeting Notes to Action Items Summarizer")
st.caption("Transform messy meeting transcripts into structured action items instantly.")

# Sidebar - API Key Input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to get started.")
    st.stop()

genai.configure(api_key=api_key)

# Sample Text Generator Button
sample_transcript = """
Meeting Title: Q4 Marketing Strategy Sync
Attendees: Sarah Jenkins (Lead), David Chen (Developer), Priya Sharma (Designer)

Sarah: Welcome everyone. First, we need to finalize the landing page redesign by next Friday. Priya, can you take ownership of updating the Figma wireframes by Tuesday?
Priya: Sure, I will complete the wireframes by Tuesday EOD.
David: I will review the API endpoints once Priya uploads the wireframes, likely by Thursday.
Sarah: Great. Also, David, please fix the login bug reported by customer support by Monday.
Priya: I'll also send out the brand color guidelines to the agency by Wednesday.
Sarah: Perfect. Let's reconvene on Friday.
"""

if st.button("Load Sample Transcript"):
    st.session_state["transcript_input"] = sample_transcript.strip()

# Input Text Area
transcript = st.text_area(
    "Paste Meeting Transcript / Notes:", 
    value=st.session_state.get("transcript_input", ""), 
    height=200
)

# Process Button
if st.button("Generate Summary & Action Items", type="primary"):
    if not transcript.strip():
        st.warning("Please enter or paste a transcript first.")
        st.stop()

    with st.spinner("Analyzing transcript with Gemini..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            Analyze the following meeting transcript:

            "{transcript}"

            Perform two tasks:
            1. Provide a concise executive summary (3-4 bullet points).
            2. Extract all action items in a strict Markdown Table format with columns: Action Item | Owner | Due Date.
            """

            response = model.generate_content(prompt)
            st.success("Analysis Complete!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error calling Gemini API: {e}")
