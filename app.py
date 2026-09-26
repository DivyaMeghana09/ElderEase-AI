import streamlit as st
from datetime import datetime

from mood_engine import detect_mood, detect_safety_concern, generate_support_response, get_mood_trend, SAFETY_RESPONSE
from activity_engine import get_activity

st.set_page_config(
    page_title="ElderEase AI",
    page_icon="💙",
    layout="centered"
)


# -------------------------
# Session State
# -------------------------

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------------
# Mood colours — used to tint response cards by emotional tone
# -------------------------

MOOD_BORDER_COLORS = {
    "Lonely":  "#5b9bd5",   # calm blue
    "Sad":     "#7b8ab8",   # muted indigo
    "Anxious": "#e8a838",   # warm amber
    "Tired":   "#82a882",   # soft green
    "Happy":   "#f0a500",   # warm gold
    "Okay":    "#a0a0a0",   # neutral grey
}

MOOD_ICONS = {
    "Happy":  "😊",
    "Okay":   "🙂",
    "Sad":    "😔",
    "Lonely": "💙",
    "Anxious":"😟",
    "Tired":  "😴",
}


# -------------------------
# CSS
# -------------------------

st.markdown("""
<style>

/* ── Page background ── */
.stApp {
    background-color: #f4f7fb;
}

/* ── App-wide readable text ── */
.stApp, .stApp p, .stApp li, .stApp span,
.stMarkdown p, .stMarkdown li {
    font-size: 18px !important;
    line-height: 1.75 !important;
    letter-spacing: 0.01em;
    color: #1a1a2e;
}

/* ── Section headings ── */
h2, h3 {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #1a1a2e !important;
    margin-top: 0.4em !important;
    margin-bottom: 0.3em !important;
}

/* ── App title ── */
.main-title {
    text-align: center;
    font-size: 46px !important;
    font-weight: 800;
    color: #1a1a2e;
    margin-bottom: 4px;
}

/* ── App subtitle ── */
.subtitle {
    text-align: center;
    font-size: 20px !important;
    color: #4a5568;
    margin-bottom: 8px;
    line-height: 1.6;
}

/* ── ElderEase response card ── */
.support-box {
    padding: 22px 24px;
    border-radius: 14px;
    background-color: #ffffff;
    border-left: 6px solid #888;   /* overridden per-render via inline style */
    font-size: 20px !important;
    line-height: 1.75;
    margin-top: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* ── Mood trend notice ── */
.trend-box {
    padding: 14px 20px;
    border-radius: 12px;
    background-color: #f0f4ff;
    font-size: 18px !important;
    line-height: 1.7;
    margin-top: 12px;
    color: #2c3e6b;
}

/* ── Activity suggestion card ── */
.activity-box {
    padding: 20px 24px;
    border-radius: 14px;
    background-color: #f0f7ee;
    border-left: 6px solid #4caf7d;
    font-size: 19px !important;
    line-height: 1.75;
    margin-top: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* ── Mood history card ── */
.mood-card {
    padding: 16px 20px;
    border-radius: 12px;
    background: #ffffff;
    margin-top: 10px;
    border: 1px solid #d0e4f7;
    font-size: 18px !important;
    line-height: 1.6;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* ── Disclaimer footer ── */
.disclaimer {
    font-size: 15px !important;
    color: #666;
    text-align: center;
    line-height: 1.6;
    margin-top: 8px;
}

/* ── Selectbox, text-area, and button text ── */
.stSelectbox label,
.stTextArea label,
.stButton > button {
    font-size: 18px !important;
}

/* ── Buttons: larger tap target, clear visual weight ── */
.stButton > button {
    padding: 12px 20px !important;
    font-size: 18px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# Header
# -------------------------

st.markdown(
    '<div class="main-title">💙 ElderEase AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">A gentle companion for everyday emotional wellbeing</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------
# Step 1 — Quick mood check-in
# -------------------------

st.subheader("😊 How are you feeling right now?")

st.markdown(
    "Choose the mood that feels closest to how you are today.",
    unsafe_allow_html=False
)

mood_options = {
    "😊  Happy — I am feeling good today": "Happy",
    "🙂  Okay — I am getting along fine":   "Okay",
    "😔  Sad — I am feeling low or upset":  "Sad",
    "😟  Anxious — I am worried or nervous": "Anxious",
    "😴  Tired — I am feeling exhausted":   "Tired",
}

selected_option = st.selectbox(
    "Select your mood",
    list(mood_options.keys()),
    label_visibility="collapsed"
)

selected_mood = mood_options[selected_option]

if st.button("✅  Record this mood", use_container_width=True):

    st.session_state.mood_history.append(
        {
            "time": datetime.now().strftime("%d %b %Y – %I:%M %p"),
            "mood": selected_mood
        }
    )

    st.success(f"Noted — you are feeling {selected_mood} right now. 💙")


st.divider()


# -------------------------
# Step 2 — Talk to ElderEase
# -------------------------

st.subheader("💬 Share how you are feeling")

st.markdown(
    "You can write a few words or a few sentences — whatever feels right. "
    "ElderEase will listen and respond with care."
)

user_message = st.text_area(
    "Your message",
    placeholder="For example: I feel a bit lonely today and I miss talking to my family…",
    height=130,
    label_visibility="collapsed"
)

if st.button("💙  Send to ElderEase", use_container_width=True):

    if not user_message.strip():

        st.warning("Please write a few words so ElderEase can understand how you are feeling.")

    elif detect_safety_concern(user_message):

        st.markdown(
            f"""
            <div class="support-box" style="border-left-color: #c0392b;">
            <b>💙 ElderEase is here with you</b><br><br>
            {SAFETY_RESPONSE}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        mood = detect_mood(user_message)
        response = generate_support_response(mood, user_message)
        activity = get_activity(mood)

        st.session_state.chat_history.append(
            {
                "user": user_message,
                "mood": mood,
                "response": response,
                "activity": activity,
                "time": datetime.now().strftime("%d %b %Y – %I:%M %p"),
            }
        )

        st.session_state.mood_history.append(
            {
                "time": datetime.now().strftime("%d %b %Y – %I:%M %p"),
                "mood": mood
            }
        )

        border_color = MOOD_BORDER_COLORS.get(mood, "#a0a0a0")
        mood_icon    = MOOD_ICONS.get(mood, "💙")

        st.markdown(
            f"""
            <div class="support-box" style="border-left-color: {border_color};">
            <b>{mood_icon} ElderEase hears you</b><br><br>
            {response}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Mood trend notice ──
        # Build the sequence from chat history (earliest first, current entry
        # already appended above).  Trend is shown only when meaningful.
        mood_sequence = [c["mood"] for c in st.session_state.chat_history]
        trend = get_mood_trend(mood_sequence)

        _TREND_MESSAGES = {
            "improving": (
                "💚 Your recent check-ins seem to be moving in a more positive direction. "
                "That is good to notice."
            ),
            "declining": (
                "💙 Your recent check-ins have been a little harder lately. "
                "You do not have to face that alone."
            ),
        }

        if trend in _TREND_MESSAGES:
            st.markdown(
                f'<div class="trend-box">{_TREND_MESSAGES[trend]}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div class="activity-box">
            <b>🌿 A gentle suggestion for you</b><br><br>
            {activity}
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# -------------------------
# Step 3 — Recent conversations
# -------------------------

if st.session_state.chat_history:

    st.subheader("💬 Your recent chats with ElderEase")

    for chat in reversed(st.session_state.chat_history[-3:]):

        mood_icon = MOOD_ICONS.get(chat["mood"], "💙")
        timestamp = chat.get("time", "")
        label     = f"{mood_icon}  You said you felt {chat['mood']}"
        if timestamp:
            label += f"  ·  {timestamp}"

        with st.expander(label):

            st.markdown("**You wrote:**")
            st.write(chat["user"])

            st.markdown("**ElderEase replied:**")
            st.write(chat["response"])

            st.markdown("**Suggested activity:**")
            st.write(chat["activity"])


# -------------------------
# Step 4 — Mood History
# -------------------------

st.divider()

st.subheader("📅 Your mood diary")

if not st.session_state.mood_history:

    st.info(
        "Your mood diary will appear here as you check in. "
        "Each time you record a mood or send a message, it is added here."
    )

else:

    for item in reversed(st.session_state.mood_history):

        icon = MOOD_ICONS.get(item["mood"], "💙")

        st.markdown(
            f"""
            <div class="mood-card">
            {icon}&nbsp;&nbsp;<b>{item["mood"]}</b>
            &nbsp;&nbsp;<span style="color:#888; font-size:16px;">{item["time"]}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------
# Disclaimer
# -------------------------

st.divider()

st.markdown(
    '<p class="disclaimer">'
    "ElderEase AI offers gentle emotional support and simple wellbeing suggestions. "
    "It is not a medical service, therapist, or emergency service. "
    "If you are in distress, please speak to a trusted person or call Tele-MANAS: "
    "<b>14416</b> or <b>1800-89-14416</b> (free, 24 hours, available across India)."
    "</p>",
    unsafe_allow_html=True
)
