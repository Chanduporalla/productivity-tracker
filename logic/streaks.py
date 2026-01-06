from datetime import datetime, timedelta

def mark(data):
    today = str(datetime.now().date())
    data["streak"][today] = 1

def count(data):
    streak = 0
    today = datetime.now().date()
    for i in range(365):
        if str(today - timedelta(days=i)) in data["streak"]:
            streak += 1
        else:
            break
    return streak
