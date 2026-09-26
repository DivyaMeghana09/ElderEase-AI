# Distress phrases that must trigger the safety escalation path.
# This check takes precedence over ordinary mood detection.
_DISTRESS_KEYWORDS = [
    "don't want to go on",
    "want to give up",
    "nobody cares about me",
    "no one cares about me",
    "feel like disappearing",
    "thinking of hurting myself",
    "want to hurt myself",
    "don't see the point",
    "life feels meaningless",
    "life is meaningless",
    "want to end it",
    "can't go on",
    "cannot go on",
    # Additional phrases identified during safety review
    "end my life",
    "kill myself",
    "no reason to live",
    "don't want to live",
]

# The single safety response returned whenever a distress phrase is detected.
# Warm, non-medical, signposts real human support.
# Helpline: Tele-MANAS (India) — 14416 or 1800-89-14416 (free, 24 hours).
SAFETY_RESPONSE = (
    "Thank you for trusting me with how you feel. "
    "What you are going through sounds very hard, and your feelings matter. "
    "Please speak with someone you trust — a family member, a friend, or your doctor. "
    "If you need to talk to someone right now, you can call the free Tele-MANAS helpline: "
    "14416 or 1800-89-14416 (free, 24 hours, available across India)."
)


def detect_safety_concern(text):
    """
    Return True if the text contains a serious distress phrase that warrants
    the safety escalation response, False otherwise.

    This check must be run before detect_mood so that distress language is
    never silently absorbed into a standard mood category.

    Args:
        text (str): The user's raw input message.

    Returns:
        bool: True if a distress phrase is present, False otherwise.
    """
    lowered = text.lower()
    for phrase in _DISTRESS_KEYWORDS:
        if phrase in lowered:
            return True
    return False


def detect_mood(text):
    """
    Detect the primary emotional mood expressed in the user's message.

    Uses keyword matching against a fixed vocabulary. Returns the label of
    the first matching mood category, or "Okay" if no keyword matches.
    Note: distress-level language should be screened by detect_safety_concern
    before this function is called.

    Args:
        text (str): The user's raw input message.

    Returns:
        str: One of "Lonely", "Sad", "Anxious", "Tired", "Happy", "Okay".
    """
    text = text.lower()

    mood_keywords = {

        "Lonely": [
            "lonely",
            "alone",
            "miss someone",
            "miss my family",
            "no one to talk"
        ],

        "Sad": [
            "sad",
            "unhappy",
            "upset",
            "cry",
            "depressed",
            "low"
        ],

        "Anxious": [
            "anxious",
            "worried",
            "nervous",
            "scared",
            "afraid",
            "stress"
        ],

        "Tired": [
            "tired",
            "exhausted",
            "sleepy",
            "weak",
            "no energy"
        ],

        "Happy": [
            "happy",
            "great",
            "wonderful",
            "excited",
            "good day"
        ]
    }

    for mood, keywords in mood_keywords.items():

        for keyword in keywords:

            if keyword in text:
                return mood

    return "Okay"


# Wellbeing weights used for within-session mood trend analysis.
# Scale: 1 (lowest wellbeing) – 5 (highest wellbeing).
# Deliberately simple and explainable; not a clinical scale.
_MOOD_WEIGHTS = {
    "Happy":   5,
    "Okay":    4,
    "Tired":   3,
    "Lonely":  2,
    "Anxious": 2,
    "Sad":     1,
}

# Minimum number of chat history entries needed to compute a trend.
_TREND_MIN_ENTRIES = 3

# How much the second-half average must exceed the first-half average
# (in either direction) before the trend is declared improving/declining.
_TREND_THRESHOLD = 1.0


def get_mood_trend(mood_sequence):
    """
    Analyse a sequence of mood labels from recent chat interactions and
    return a simple trend description.

    The sequence is split into a first half and a second half.  If the
    second-half average wellbeing score exceeds the first-half average by
    at least _TREND_THRESHOLD points, the trend is "improving".  The reverse
    gives "declining".  A smaller difference returns "stable".  Fewer than
    _TREND_MIN_ENTRIES entries returns "not_enough_data".

    Unknown mood labels are silently ignored.  If all labels are unknown the
    function returns "not_enough_data".

    Args:
        mood_sequence (list[str]): Ordered list of mood label strings,
            earliest first.  Typically extracted from st.session_state
            chat_history by the caller.

    Returns:
        str: One of "improving", "declining", "stable", "not_enough_data".
    """
    # Filter to only known moods so unknown/invalid labels don't skew scores.
    scored = [_MOOD_WEIGHTS[m] for m in mood_sequence if m in _MOOD_WEIGHTS]

    if len(scored) < _TREND_MIN_ENTRIES:
        return "not_enough_data"

    midpoint   = len(scored) // 2
    first_half = scored[:midpoint]
    second_half = scored[midpoint:]

    avg_first  = sum(first_half)  / len(first_half)
    avg_second = sum(second_half) / len(second_half)

    delta = avg_second - avg_first

    if delta >= _TREND_THRESHOLD:
        return "improving"
    if delta <= -_TREND_THRESHOLD:
        return "declining"
    return "stable"


# Per-mood response templates.
# Each entry is a (opening, closing) pair.  The user's own words are woven
# into the middle so that every response is unique to what they actually said.
_RESPONSE_TEMPLATES = {

    "Lonely": (
        "It sounds like you're feeling a little alone right now. ",
        " Reaching out — even in a small way — can sometimes make the day feel warmer."
    ),

    "Sad": (
        "I'm sorry today feels difficult. ",
        " You don't have to face everything at once — one small step is enough."
    ),

    "Anxious": (
        "It sounds like there is a lot on your mind. ",
        " Try giving yourself a quiet moment and taking a few slow breaths."
    ),

    "Tired": (
        "It sounds like you may need a little rest today. ",
        " A short break and a glass of water can sometimes make a real difference."
    ),

    "Happy": (
        "That's really lovely to hear. ",
        " It's wonderful when a day feels good — enjoy every moment of it."
    ),

    "Okay": (
        "Thank you for sharing how you feel. ",
        " Sometimes one small enjoyable activity is all it takes to brighten the day."
    ),
}


def generate_support_response(mood, user_message):
    """
    Generate a compassionate, personalised support response.

    The response is built from a mood-specific template and incorporates a
    short excerpt from the user's own message so that each reply reflects
    what they actually shared, not a generic canned phrase.

    Args:
        mood (str): The detected mood label (e.g. "Lonely", "Sad").
        user_message (str): The user's original message text.

    Returns:
        str: A warm, non-medical support response personalised to the user.
    """
    template = _RESPONSE_TEMPLATES.get(mood, _RESPONSE_TEMPLATES["Okay"])
    opening, closing = template

    # Trim the user's message for use inside the response.
    # Keep it short — we are echoing, not quoting at length.
    trimmed = user_message.strip()
    if len(trimmed) > 80:
        trimmed = trimmed[:77].rstrip() + "..."

    if trimmed:
        middle = f'You mentioned: "{trimmed}" — that takes courage to share. '
    else:
        middle = ""

    return opening + middle + closing
