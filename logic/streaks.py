from datetime import datetime, timedelta

def calculate_streak(streak_data):
    streak = 0
    day = datetime.now().date()

    while str(day) in streak_data:
        streak += 1
        day -= timedelta(days=1)

    return streak
