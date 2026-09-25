def detect_mood(text):

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


def generate_support_response(mood, user_message):

    responses = {

        "Lonely":
            "It sounds like you're feeling a little alone today. "
            "Having someone to connect with can sometimes make the day feel warmer. "
            "Even a short conversation with someone you care about may help.",

        "Sad":
            "I'm sorry that today feels difficult. "
            "You don't have to solve everything at once. "
            "A small comforting activity or speaking with someone you trust may help.",

        "Anxious":
            "It sounds like there is a lot on your mind. "
            "Try giving yourself a quiet moment and taking a few slow breaths. "
            "You can focus on one small thing at a time.",

        "Tired":
            "It sounds like you may need a little rest today. "
            "A quiet break, some water, or a few minutes of relaxation might help you feel refreshed.",

        "Happy":
            "That's lovely to hear. "
            "Enjoy this moment and consider sharing your happiness with someone you care about.",

        "Okay":
            "Thank you for sharing how you feel. "
            "Sometimes an ordinary day can become better with one small enjoyable activity."
    }

    return responses.get(
        mood,
        responses["Okay"]
    )