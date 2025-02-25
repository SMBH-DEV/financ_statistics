from pydantic import BaseModel
from datetime import date


class Statistic(BaseModel):
    created_at: date
    organization: str
    object_: str
    spent: float
    impressions: int
    clicks: int
    goals: int
    ctr: float  # Click-Through Rate - Коэффициент кликабельности (clicks / impressions)
    cpm: float  # Cost Per Mille - Стоимость за 1000 показов (spent / impressions * 1000)
    cpc: float  # Cost Per Click - Стоимость за клик (spent / clicks)
    cps: float  # Cost Per Subscription - Стоимость за подписку (spent / goals)