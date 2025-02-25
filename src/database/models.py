from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy.sql import text


class Statistics(Base):
    __tablename__ = 'statistics'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(server_default=text("TIMEZONE('utc', current_date)"))
    organization: Mapped[str]
    object_: Mapped[str]
    spent: Mapped[float]
    impressions: Mapped[int]
    clicks: Mapped[int]
    goals: Mapped[int]
    ctr: Mapped[float] = mapped_column(
        comment="Click-Through Rate - Коэффициент кликабельности (clicks / impressions)"
    )
    cpm: Mapped[float] = mapped_column(
        comment="Cost Per Mille - Стоимость за 1000 показов (spent / impressions * 1000)"
    )
    cpc: Mapped[float] = mapped_column(
        comment="Cost Per Click - Стоимость за клик (spent / clicks)"
    )
    cps: Mapped[float] = mapped_column(
        comment="Cost Per Subscription - Стоимость за подписку (spent / goals)"
    )
