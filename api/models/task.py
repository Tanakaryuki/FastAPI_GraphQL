import strawberry
from sqlalchemy import func, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.db import Base


@strawberry.type
class Task(Base):
    __tablename__ = "Tasks"

    id = Column(String(48), primary_key=True, index=True)
    administrator_username = Column(
        String(48), ForeignKey("Users.username"), nullable=False, index=True
    )
    title = Column(String(48), nullable=False)
    detail = Column(String(96), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    administrator = relationship("User", back_populates="tasks_administered")
