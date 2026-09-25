import random


ACTIVITIES = {

    "Lonely": [
        "Call or message a family member or friend for a short conversation.",
        "Look through a few favourite family photographs.",
        "Listen to a song that brings back a happy memory."
    ],

    "Sad": [
        "Sit somewhere comfortable and listen to a favourite song.",
        "Write down one small thing you are grateful for today.",
        "Spend a few minutes looking at photographs that make you smile."
    ],

    "Anxious": [
        "Take five slow breaths: breathe in gently and breathe out slowly.",
        "Sit quietly with a cup of tea or water for five minutes.",
        "Focus on one simple task instead of thinking about everything at once."
    ],

    "Tired": [
        "Take a short rest in a comfortable place.",
        "Drink a glass of water and relax for a few minutes.",
        "Listen to soft music while resting."
    ],

    "Happy": [
        "Share your good mood with someone you care about.",
        "Listen to one of your favourite songs.",
        "Spend a few minutes doing something you enjoy."
    ],

    "Okay": [
        "Take a short walk if you feel comfortable doing so.",
        "Listen to your favourite song.",
        "Call someone you enjoy speaking with.",
        "Enjoy a cup of tea while relaxing."
    ]
}


def get_activity(mood):

    activities = ACTIVITIES.get(
        mood,
        ACTIVITIES["Okay"]
    )

    return random.choice(activities)