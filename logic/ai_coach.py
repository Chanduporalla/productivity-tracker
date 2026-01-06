import random

SUGGESTIONS = [
    "Focus on one hard task today",
    "Revise DSA fundamentals",
    "Avoid phone during deep work",
    "Track expenses today",
    "Work on one resume project"
]

def get_ai_suggestion():
    return random.choice(SUGGESTIONS)
