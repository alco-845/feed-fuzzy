from fastapi import FastAPI, HTTPException

from fishDetail import FishDetail, fishDetail
from feedFuzzy import InputData, OutputData, feedFuzzy

app = FastAPI()

@app.get("/")
async def index() -> dict[str, FishDetail]:
    return fishDetail


@app.put("/update")
async def updateAll(
    fishDetailed: FishDetail
):
    if "data" not in fishDetail:
        raise HTTPException(status_code=404, detail=f"Item not found")

    fishDetail["data"] = {
        "id": fishDetailed.id,
        "fish_age_days": fishDetailed.fish_age_days,
        "fish_amount": fishDetailed.fish_amount,
        "date_start_automation": fishDetailed.date_start_automation,
        "feed_duration_seconds": fishDetailed.feed_duration_seconds}

    return {"detail": "success", "data": fishDetail["data"]}

@app.put("/update/duration")
async def update_feed_duration(feed_duration_seconds: int):
    if "data" not in fishDetail:
        raise HTTPException(status_code=404, detail="Item not found")

    fishDetail["data"].feed_duration_seconds = feed_duration_seconds
    return {"detail": "success", "data": {"feed_duration_seconds": feed_duration_seconds}}

@app.post("/predict", response_model=OutputData)
async def predict(input_data: InputData):
    return {"feed_duration_seconds": feedFuzzy(input_data)}