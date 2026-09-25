import streamlit as st
from datetime import datetime

from mood_engine import detect_mood, generate_support_response
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
# CSS
# -------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fc;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #555;
}

.mood-card {
    padding: 18px;
    border-radius: 15px;
    background: white;
    margin-top: 10px;
    border: 1px solid #eee;
}

.support-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #ffffff;
    border-left: 5px solid #888;
    font-size: 18px;
}

.activity-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #ffffff;
    margin-top: 15px;
    font-size: 18px;
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
    '<div class="subtitle">A gentle AI companion for everyday emotional wellbeing</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------
# Mood Selection
# -------------------------

st.subheader("How are you feeling today?")

mood_options = {
    "😊 Happy": "Happy",
    "🙂 Okay": "Okay",
    "😔 Sad": "Sad",
    "😟 Anxious": "Anxious",
    "😴 Tired": "Tired"
}

selected_option = st.selectbox(
    "Choose your mood",
    list(mood_options.keys())
)

selected_mood = mood_options[selected_option]


if st.button("Save my mood", use_container_width=True):

    st.session_state.mood_history.append(
        {
            "time": datetime.now().strftime("%d %b %Y - %I:%M %p"),
            "mood": selected_mood
        }
    )

    st.success(f"Your mood has been saved: {selected_mood}")


st.divider()


# -------------------------
# AI Companion
# -------------------------

st.subheader("💬 Talk to ElderEase")

user_message = st.text_area(
    "Tell me how you are feeling",
    placeholder="Example: I feel lonely today and I miss talking to my family..."
)


if st.button("Talk to ElderEase", use_container_width=True):

    if not user_message.strip():

        st.warning("Please tell ElderEase how you are feeling.")

    else:

        mood = detect_mood(user_message)

        response = generate_support_response(
            mood,
            user_message
        )

        activity = get_activity(mood)

        st.session_state.chat_history.append(
            {
                "user": user_message,
                "mood": mood,
                "response": response,
                "activity": activity
            }
        )

        st.session_state.mood_history.append(
            {
                "time": datetime.now().strftime("%d %b %Y - %I:%M %p"),
                "mood": mood
            }
        )

        st.markdown(
            f"""
            <div class="support-box">
            <b>Detected mood:</b> {mood}<br><br>
            {response}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="activity-box">
            <b>🌿 A small activity for you</b><br><br>
            {activity}
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# -------------------------
# Conversation
# -------------------------

if st.session_state.chat_history:

    st.subheader("Recent conversation")

    for chat in reversed(st.session_state.chat_history[-3:]):

        with st.expander(
            f"{chat['mood']} conversation"
        ):

            st.write("**You:**")
            st.write(chat["user"])

            st.write("**ElderEase:**")
            st.write(chat["response"])

            st.write("**Suggested activity:**")
            st.write(chat["activity"])


# -------------------------
# Mood History
# -------------------------

st.divider()

st.subheader("📅 Mood History")

if not st.session_state.mood_history:

    st.info("Your mood history will appear here.")

else:

    mood_icons = {
        "Happy": "😊",
        "Okay": "🙂",
        "Sad": "😔",
        "Lonely": "💙",
        "Anxious": "😟",
        "Tired": "😴"
    }

    for item in reversed(st.session_state.mood_history):

        icon = mood_icons.get(
            item["mood"],
            "💙"
        )

        st.markdown(
            f"""
            <div class="mood-card">
            {icon} <b>{item["mood"]}</b><br>
            <small>{item["time"]}</small>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------
# Safety Note
# -------------------------

st.divider()

st.caption(
    "ElderEase AI provides general emotional support and simple wellbeing suggestions. "
    "It is not a medical or emergency service."
)