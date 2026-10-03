import streamlit as st
from groq import Groq
import textwrap

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f7f8fc;
    }

    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #182848, #4b6cb7);
        padding: 35px 40px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        padding: 7px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin-bottom: 12px;
    }

    .hero h1 {
        font-size: 38px;
        margin: 0;
        font-weight: 700;
    }

    .hero p {
        font-size: 17px;
        margin-top: 10px;
        opacity: 0.9;
    }

    /* Cards */
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Section headings */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #182848;
        margin-bottom: 8px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 18px;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        font-size: 13px;
        margin-top: 40px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HERO HEADER
# ---------------------------------------------------------
st.markdown(
    textwrap.dedent(
        """
        <div class="hero">
            <div class="hero-badge">✨ AI-Powered Productivity Assistant</div>
            <h1>📝 AI Meeting Summarizer</h1>
            <p>
                Transform unstructured meeting conversations into clear summaries,
                actionable tasks and important decisions.
            </p>
        </div>
        """
    ),
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.markdown("## 📝 AI Meeting Summarizer")

    st.markdown(
        """
        This application converts meeting transcripts into:

        - 📌 Executive Summary
        - ✅ Action Items
        - 👤 Task Owners
        - 📅 Deadlines
        - 🎯 Key Decisions
        - ⚠️ Dependencies & Risks
        """
    )

    st.divider()

    st.markdown("### ⚙️ How It Works")

    st.markdown(
        """
        **1.** Enter or load a meeting transcript.

        **2.** Click **Generate Meeting Insights**.

        **3.** AI analyses the conversation.

        **4.** Structured meeting outcomes are generated.
        """
    )

    st.divider()

    st.markdown("### 🤖 Technology")

    st.markdown(
        """
        **Frontend:** Streamlit

        **Language:** Python

        **AI Model:** GPT-OSS 120B

        **API:** Groq
        """
    )

    st.divider()

    st.caption("Academic Project • FORE School of Management")

# ---------------------------------------------------------
# CONNECT TO GROQ USING STREAMLIT SECRETS
# ---------------------------------------------------------

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)

except Exception:
    st.error(
        "⚠️ Groq API key is not configured. "
        "Please add GROQ_API_KEY in Streamlit Secrets."
    )
    st.stop()

# ---------------------------------------------------------
# SAMPLE TRANSCRIPT
# ---------------------------------------------------------

sample_transcript = """
Meeting Title: New Product Launch Planning Meeting
Date: 2 October 2026

Attendees:
Ananya Mehta – Product Manager
Rohan Kapoor – Marketing Manager
Neha Sharma – Sales Manager
Arjun Malhotra – Operations Lead

Ananya:
We are targeting 20 October as the launch date for the new product. I want everyone to work backwards from this date.

Rohan:
From the marketing side, we can start the digital campaign from 10 October. I will need the final product specifications before we finalize the campaign messaging.

Ananya:
That is fine. I will share the final product specifications and pricing by tomorrow evening.

Neha:
For the distributor network, we need training material at least one week before launch. The training material depends on the final pricing and product specifications.

Ananya:
Understood. I will make sure the final pricing and specifications are shared by tomorrow.

Rohan:
I will prepare the first draft of the campaign creatives by 7 October.

Neha:
For distributors, I can schedule training sessions starting 13 October. I will also prepare the first version of the distributor training material.

Arjun:
From operations, inventory needs to reach the Delhi NCR distributors by 15 October so that they have enough time before launch.

Ananya:
Good. Let's keep 17 October for a final launch-readiness meeting.

Neha:
One more thing. The sales team needs clarity on customer questions around filter replacement and electricity consumption. I will prepare a first draft of the FAQ by 12 October.

Arjun:
I will coordinate with the warehouse team to make sure the inventory reaches distributors on time.

Ananya:
Perfect. Let's reconvene on 17 October for the final readiness check.
"""

# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📄 Meeting Transcript</div>',
    unsafe_allow_html=True
)

st.write(
    "Paste your meeting transcript below, or use the sample meeting to test the application."
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("📄 Load Sample Product Launch Meeting", use_container_width=True):
        st.session_state["transcript"] = sample_transcript

with col2:
    if st.button("🗑️ Clear Transcript", use_container_width=True):
        st.session_state["transcript"] = ""

if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""

transcript = st.text_area(
    "Meeting Transcript",
    value=st.session_state["transcript"],
    height=350,
    placeholder="Paste your meeting transcript here...",
    label_visibility="collapsed"
)

# ---------------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------------

st.write("")

generate = st.button(
    "✨ Generate Meeting Insights",
    type="primary",
    use_container_width=True
)

# ---------------------------------------------------------
# AI PROCESSING
# ---------------------------------------------------------

if generate:

    if not transcript.strip():
        st.warning("⚠️ Please enter a meeting transcript first.")

    else:

        with st.spinner("🤖 Analysing the meeting and generating insights..."):

            prompt = f"""
You are a professional meeting summarization assistant.

Analyse the following meeting transcript and convert it into a concise,
professional and useful meeting outcome.

IMPORTANT RULES:
- Do not invent information.
- Do not create an owner if one is not mentioned.
- Do not create a deadline if one is not mentioned.
- If an owner or deadline is missing, write "Not specified".
- Preserve dates exactly as mentioned in the transcript.
- Keep the output practical and easy to understand.

Return the answer using EXACTLY this structure:

## 1. Executive Summary

Provide 3–5 concise bullet points summarizing the meeting.

## 2. Action Items

Create a Markdown table with these columns:

| Action Item | Owner | Due Date |
|---|---|---|

Include all clearly identifiable action items.

## 3. Key Decisions

List the important decisions made during the meeting.

## 4. Dependencies and Risks

Identify dependencies, blockers, uncertainties or risks mentioned in the discussion.

## 5. Meeting Follow-Up

Provide a short summary of what needs to happen next and mention the next meeting
if a date has been specified.

MEETING TRANSCRIPT:

{transcript}
"""

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a professional meeting summarization "
                                "assistant. Accuracy and faithful extraction "
                                "of information are more important than creativity."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=1800
                )

                result = response.choices[0].message.content

                # -------------------------------------------------
                # RESULTS
                # -------------------------------------------------

                st.markdown(
                    '<div class="section-title">✨ Meeting Insights</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.markdown(result)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

                # -------------------------------------------------
                # HUMAN REVIEW
                # -------------------------------------------------

                st.info(
                    "👤 **Human Review Recommended:** "
                    "AI-generated meeting summaries should be reviewed "
                    "before being used for important business decisions."
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while generating the summary."
                )

                st.caption(f"Technical details: {str(e)}")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    textwrap.dedent(
        """
        <div class="footer">
            <b>AI Meeting Summarizer</b><br>
            Transforming conversations into actionable outcomes<br><br>
            Academic Project • FORE School of Management
        </div>
        """
    ),
    unsafe_allow_html=True
)
