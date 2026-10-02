import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f8fc;
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .hero {
        background: linear-gradient(135deg, #182848 0%, #4b6cb7 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 8px 25px rgba(24, 40, 72, 0.15);
    }

    .hero h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.3rem;
        font-weight: 700;
    }

    .hero p {
        color: #e8ecf8;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.16);
        color: white;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.78rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Section cards */
    .section-card {
        background: white;
        border: 1px solid #e7e9f2;
        border-radius: 15px;
        padding: 1.3rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(30, 40, 80, 0.05);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #182848;
        margin-bottom: 0.7rem;
    }

    /* Info cards */
    .info-card {
        background: #eef3ff;
        border-left: 4px solid #4b6cb7;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #25345b;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f8;
    }

    section[data-testid="stSidebar"] h2 {
        color: #182848;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 2.8rem;
        border: none;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #182848, #4b6cb7);
        color: white;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7b8194;
        font-size: 0.82rem;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e1e3eb;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

    <div class="badge">✨ AI-Powered Productivity Assistant</div>

    <h1>📝 AI Meeting Summarizer</h1>

    <p>
        Transform unstructured meeting conversations into
        clear summaries, actionable tasks and important decisions.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## ⚙️ Configuration")

st.sidebar.markdown(
    "Enter your **Groq API Key** to activate the AI analysis."
)

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_..."
)

st.sidebar.divider()

st.sidebar.markdown("### 💡 How it works")

st.sidebar.markdown("""
**1. 📄 Add Meeting Notes**

Paste a meeting transcript or use our sample.

**2. 🤖 AI Analysis**

The AI identifies important information.

**3. 📊 Structured Output**

Receive a summary, action items, decisions and risks.

**4. 👤 Human Review**

Verify the generated information before taking action.
""")

st.sidebar.divider()

st.sidebar.markdown("### 🛠️ Technology")

st.sidebar.caption("""
**Frontend:** Streamlit  
**AI API:** Groq  
**Model:** GPT-OSS-120B  
**Language:** Python
""")

st.sidebar.divider()

st.sidebar.caption(
    "Academic Project • FORE School of Management"
)


# =========================================================
# API KEY CHECK
# =========================================================

if not api_key:

    st.markdown("""
    <div class="info-card">
        🔐 <b>Getting Started</b><br><br>
        Enter your Groq API key in the sidebar to activate
        the meeting analysis functionality.
    </div>
    """, unsafe_allow_html=True)

    st.stop()


client = Groq(api_key=api_key)


# =========================================================
# SAMPLE TRANSCRIPT
# =========================================================

sample_transcript = """
Meeting Title: New Product Launch Planning Meeting

Date: 2 October 2026

Attendees:
Ananya Mehta – Product Manager
Rohan Kapoor – Marketing Manager
Neha Sharma – Sales Manager
Arjun Malhotra – Operations Lead

Ananya: Thanks everyone. We need to finalize the launch plan for our new smart air purifier. The target launch date is 20 October.

Rohan: From the marketing side, we'll start the digital campaign on 10 October. I need the final product photographs and specifications before we start creating the campaign creatives.

Ananya: The final product specifications will be shared by tomorrow evening.

Neha: For sales, we need the dealer training material at least one week before launch. Otherwise, the distributors won't have enough time to prepare their teams.

Arjun: I can arrange the dealer training material, but I need the final pricing and product specifications first.

Ananya: I'll send the final pricing along with the product specifications tomorrow.

Rohan: Once I receive those, I'll prepare the campaign creatives and share the first draft with everyone by 7 October.

Neha: I'll schedule the distributor training sessions for 13 October.

Arjun: I'll make sure the initial inventory reaches the Delhi NCR distributors by 15 October.

Ananya: Great. Let's also have a final launch-readiness meeting on 17 October to review inventory, marketing, sales readiness and customer support.

Rohan: One more thing. We should prepare a FAQ document because customers may have questions about filter replacement and electricity consumption.

Ananya: Good point. Neha, can your team prepare the first draft of the FAQ?

Neha: Yes, I'll share the first draft by 12 October.

Ananya: Perfect. Let's reconvene on 17 October.
"""


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📄 Meeting Transcript</div>',
    unsafe_allow_html=True
)

st.caption(
    "Paste your meeting transcript below, or load the sample meeting to see how the application works."
)

# Load sample button

if st.button("📄 Load Sample Product Launch Meeting"):

    st.session_state["transcript_input"] = sample_transcript.strip()


transcript = st.text_area(
    "Meeting Notes / Transcript",
    value=st.session_state.get("transcript_input", ""),
    height=320,
    placeholder=(
        "Paste your meeting transcript here..."
    ),
    label_visibility="collapsed"
)


# =========================================================
# GENERATE BUTTON
# =========================================================

generate = st.button(
    "✨ Generate Meeting Insights",
    type="primary",
    use_container_width=True
)


# =========================================================
# AI PROCESSING
# =========================================================

if generate:

    if not transcript.strip():

        st.warning(
            "⚠️ Please enter a meeting transcript before generating insights."
        )

        st.stop()


    prompt = f"""
You are an expert AI Meeting Assistant helping managers
convert unstructured meeting discussions into useful,
actionable business information.

Analyze the following meeting transcript.

MEETING TRANSCRIPT:
{transcript}

Perform the following tasks:

1. EXECUTIVE SUMMARY
Create a concise summary containing the 3–5 most important
points discussed in the meeting.

2. ACTION ITEMS
Identify ALL clearly stated action items.

For every action item provide:
- Action Item
- Owner
- Due Date

IMPORTANT:
Do NOT invent an owner or deadline.
If an owner is not explicitly identifiable, write:
"Not specified"

If a deadline is not explicitly stated, write:
"Not specified"

3. KEY DECISIONS
Identify important decisions or commitments made during
the meeting.

4. DEPENDENCIES AND RISKS
Identify dependencies between tasks and any risks,
uncertainties or potential bottlenecks discussed.

Do NOT invent risks that are not reasonably supported
by the transcript.

5. MEETING FOLLOW-UP
Identify the next meeting or follow-up activity if one
is explicitly mentioned.

Use exactly this structure:

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

## ⚠️ Dependencies & Risks

- Dependency or risk 1
- Dependency or risk 2

If no meaningful dependencies or risks are present,
write:
"No major dependencies or risks identified."

## 📅 Follow-Up

- Mention the next meeting or follow-up activity.

Keep the output professional, concise and suitable
for a business environment.

Do not add information that is not supported by the transcript.
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
                            "You are a professional meeting "
                            "summarization assistant. "
                            "Accuracy and faithful extraction "
                            "of information are more important "
                            "than creativity."
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


        # =================================================
        # RESULTS HEADER
        # =================================================

        st.success("✅ Meeting analysis completed successfully!")

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">📊 Meeting Insights</div>',
            unsafe_allow_html=True
        )

        st.markdown(result)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # HUMAN REVIEW NOTICE
        # =================================================

        st.markdown("""
        <div class="info-card">

        👤 <b>Human Review Recommended</b><br><br>

        AI-generated summaries and action items should be
        reviewed by a meeting participant before they are
        treated as official commitments or deadlines.

        </div>
        """, unsafe_allow_html=True)


    except Exception as e:

        st.error(
            f"❌ Groq API Error: {str(e)}"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

<b>AI Meeting Summarizer</b><br>

Transforming conversations into actionable outcomes

<br><br>

Academic Project • FORE School of Management

</div>
""", unsafe_allow_html=True)
