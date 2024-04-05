from pydantic import BaseModel

class FishDetail(BaseModel):
    id: int
    fish_age_days: int
    fish_amount: int
    date_start_automation: str
    feed_duration_seconds: int

fishDetail = {
    "data": 
        FishDetail(
            id = 1,
            fish_age_days = 0,
            fish_amount = 0,
            date_start_automation = "2000-02-02",
            feed_duration_seconds = 3
        )
}