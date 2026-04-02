from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
from collections import defaultdict
import csv


app = FastAPI(title="AI Auto Cart System")


class RecommendRequest(BaseModel):
    user_id: str
    today: str  # format: YYYY-MM-DD
    threshold_days: int = 7


def load_purchase_data(file_path="data/sample_purchase_data.csv"):
    records = []

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "user": row["user"],
                "item": row["item"],
                "date": datetime.strptime(row["date"], "%Y-%m-%d")
            })

    return records


def get_user_history(records, user_id):
    grouped = defaultdict(list)

    for record in records:
        if record["user"] == user_id:
            grouped[record["item"]].append(record["date"])

    for item in grouped:
        grouped[item].sort()

    return grouped


def calculate_average_cycle(dates):
    if len(dates) < 2:
        return 60

    intervals = []
    for i in range(1, len(dates)):
        intervals.append((dates[i] - dates[i - 1]).days)

    return sum(intervals) / len(intervals)


def generate_message(item_name, days_left):
    if days_left < 0:
        return f"{item_name} repurchase timing has already passed."
    elif days_left == 0:
        return f"Today is the expected repurchase date for {item_name}."
    return f"{item_name} is expected to be repurchased in {days_left} days."


def recommend_items(user_id, today_str, threshold_days=7):
    records = load_purchase_data()
    today = datetime.strptime(today_str, "%Y-%m-%d")
    history = get_user_history(records, user_id)

    recommendations = []

    for item_name, dates in history.items():
        avg_cycle = calculate_average_cycle(dates)
        last_purchase = dates[-1]
        predicted_next_date = last_purchase + timedelta(days=avg_cycle)
        days_left = (predicted_next_date - today).days

        if days_left <= threshold_days:
            recommendations.append({
                "item_name": item_name,
                "last_purchase_date": last_purchase.strftime("%Y-%m-%d"),
                "average_cycle_days": round(avg_cycle, 1),
                "predicted_next_date": predicted_next_date.strftime("%Y-%m-%d"),
                "days_left": days_left,
                "message": generate_message(item_name, days_left)
            })

    recommendations.sort(key=lambda x: x["days_left"])
    return recommendations


@app.get("/")
def root():
    return {
        "message": "AI Auto Cart System is running."
    }


@app.post("/recommend")
def recommend(request: RecommendRequest):
    recommendations = recommend_items(
        user_id=request.user_id,
        today_str=request.today,
        threshold_days=request.threshold_days
    )

    return {
        "user_id": request.user_id,
        "recommended_cart": [item["item_name"] for item in recommendations],
        "details": recommendations
    }
