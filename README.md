# AI Auto Cart System

A FastAPI-based recommendation system that predicts repurchase timing using user purchase history data.

## Features
- Predicts repurchase cycle per item
- Recommends items based on expected depletion timing
- Uses CSV-based structured purchase dataset
- Provides API endpoint for recommendation results

## Tech Stack
- Python
- FastAPI
- Pydantic

## API Endpoints

### GET /
Returns service status.

### POST /recommend
Returns repurchase recommendations for a given user.

Example request:
```json
{
  "user_id": "user1",
  "today": "2026-04-03",
  "threshold_days": 7
}
