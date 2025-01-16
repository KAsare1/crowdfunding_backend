import datetime
from sqlalchemy import TIMESTAMP, Column, DateTime, Numeric, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.expression import text
from .db import Base 




class Contribution(Base):
    __tablename__ = "contributions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    contributed_at = Column(DateTime, default=datetime.timezone.utc)

    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="contributions")

    contributor_id = Column(String, ForeignKey("users.id"), nullable=False)
    contributor = relationship("User", back_populates="contributions_made")