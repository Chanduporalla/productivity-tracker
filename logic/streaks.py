from datetime import datetime, timedelta

def update_streak(data, completed_today):
    today = str(datetime.now().date())
    if completed_today:
        data["streak"][today] = True
    else:
        data["streak"].pop(today, None)

def get_streak_count(data):
    count = 0
    d = datetime.now().date()
    while str(d) in data["streak"]:
        count += 1
        d -= timedelta(days=1)
    return count
