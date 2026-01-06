from datetime import datetime, timedelta

def weekly_productivity(data):
    score = 0
    for i in range(7):
        day = str(datetime.now().date() - timedelta(days=i))
        score += len(data["tasks"].get(day, []))
    return score
