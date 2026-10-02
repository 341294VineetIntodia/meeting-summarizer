import streamlit as st
from groq import Groq

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="📝",
    layout="centered"
)

# --------------------------------
# HEADER
# --------------------------------

st.title("📝 AI Meeting Summarizer")

st.caption(
    "Transform messy meeting transcripts into structured "
    "summaries and actionable tasks."
)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header("⚙️ Configuration")

api_key = st.sidebar.text_input(
    "Enter Groq API Key:",
    type="password"
)

if not api_key:
    st.info(
        "👈 Enter your Groq API Key in the sidebar to get started."
    )
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# --------------------------------
# SAMPLE MEETING
# --------------------------------

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

# --------------------------------
# LOAD SAMPLE
# --------------------------------

if st.button("📄 Load Sample Transcript"):

    st.session_state["transcript_input"] = (
        sample_transcript.strip()
    )

# --------------------------------
# TRANSCRIPT INPUT
# --------------------------------

transcript = st.text_area(
    "Paste Meeting Transcript / Notes:",
    value=st.session_state.get("transcript_input", ""),
    height=250
)

# --------------------------------
# GENERATE
# --------------------------------

if st.button(
    "✨ Generate Summary & Action Items",
    type="primary"
):

    if not transcript.strip():

        st.warning(
            "Please enter a meeting transcript first."
        )

        st.stop()

    prompt = f"""
You are an AI Meeting Assistant.

Analyze the following meeting transcript.

MEETING TRANSCRIPT:
{transcript}

Your tasks:

1. Create a concise executive summary in 3-5 bullet points.

2. Identify ALL important action items.

3. For every action item identify:
   - Action Item
   - Owner
   - Due Date

4. Identify important decisions made during the meeting.

5. Do NOT invent information.
   If an owner or due date is not mentioned,
   write "Not specified".

Return the answer using EXACTLY this structure:

## 📌 Executive Summary

- Point 1
- Point 2
- Point 3

## ✅ Action Items

| Action Item | Owner | Due Date |
|---|---|---|
| Task | Person | Date |

## 🎯 Key Decisions

- Decision 1
- Decision 2

Keep the output professional, concise,
and easy to understand.
"""

    try:

        with st.spinner(
            "🤖 AI is analyzing the meeting..."
        ):

            response = client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional "
                            "meeting summarization assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                max_tokens=1500
            )

        result = response.choices[0].message.content

        st.success("✅ Analysis Complete!")

        st.markdown(result)

    except Exception as e:

        st.error(
            f"❌ Groq API Error: {str(e)}"
        )
