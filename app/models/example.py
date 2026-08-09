"""This model is added for testing one vertical slice end-to-end.
The model will be removed when populating the database."""

# TODO: Remove when adding real models

from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db

class ExampleItem(db.Model):
    __tablename__ = "example_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ExampleItem {self.id} {self.title!r}>"