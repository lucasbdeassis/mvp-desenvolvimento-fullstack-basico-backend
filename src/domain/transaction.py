from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class Transaction(BaseModel):
    id: UUID
    amount: float
    description: str
    date: date
    category: str
    tags: list[str] | None = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def add_tags(self, tags: list[str]):
        for tag in tags:
            if not tag in self.tags:
                self.tags.append(tag)

    def remove_tags(self, tags: list[str]):
        for tag in tags:
            if tag in self.tags:
                self.tags.remove(tag)
