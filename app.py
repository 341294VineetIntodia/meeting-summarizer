import streamlit as st
from google import genai

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Meeting Summarizer")
st.caption("Transform messy meeting transcripts into structured summaries and action items.")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Configuration")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key:",
    type="password"
)

if not api_key:
    st.info("👈 Enter your Gemini API Key in the sidebar to get started.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# -----------------------------
# SAMPLE TRANSCRIPT
# -----------------------------
sample_transcript = """
Meeting Title: Q4 Marketing Strategy Sync

Attendees:
Sarah Jenkins (Lead)
David Chen (Developer)
Priya Sharma (Designer)

Sarah: Welcome everyone. First, we need to finalize the landing page redesign by next Friday. Priya, can you take ownership of updating the Figma wireframes by Tuesday?

Priya: Sure, I will complete the wireframes by Tuesday EOD.

David: I will review the API endpoints once Priya uploads the wireframes, likely by Thursday.

Sarah: Great. Also, David, please fix the login bug reported by customer support by Monday.

Priya: I'll also send out the brand color guidelines to the agency by Wednesday.

Sarah: Perfect. Let's reconvene on Friday.
"""

# -----------------------------
# LOAD SAMPLE
# -----------------------------
if st.button("📄 Load Sample Transcript"):
    st.session_state["transcript_input"] = sample_transcript.strip()

# -----------------------------
# INPUT
# -----------------------------
transcript = st.text_area(
    "Paste Meeting Transcript / Notes:",
    value=st.session_state.get("transcript_input", ""),
    height=250
)

# -----------------------------
# GENERATE SUMMARY
# -----------------------------
if st.button("✨ Generate Summary & Action Items", type="primary"):

    if not transcript.strip():
        st.warning("Please enter a meeting transcript first.")
        st.stop()

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript.

MEETING TRANSCRIPT:
{transcript}

Perform the following tasks:

1. Give a concise executive summary in 3-5 bullet points.

2. Extract every important action item.

3. For each action item identify:
   - Action Item
   - Owner
   - Due Date

4. If an owner or due date is not explicitly mentioned, write "Not specified".
   Do not invent information.

Format the response exactly like this:

## 📌 Executive Summary

- Point 1
- Point 2
- Point 3

## ✅ Action Items

| Action Item | Owner | Due Date |
|---|---|---|
| Example task | Person | Date |

## 🎯 Key Decisions

- Decision 1
- Decision 2

Keep the answer professional, concise and easy to understand.
"""

    try:
        with st.spinner("🤖 Gemini is analyzing the meeting..."):

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

        st.success("✅ Analysis Complete!")

        st.markdown(response.text)

    except Exception as e:
        st.error(f"❌ Gemini API Error: {e}")
