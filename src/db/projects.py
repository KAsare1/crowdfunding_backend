import uuid
from sqlalchemy import TIMESTAMP, Column, DateTime, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.expression import text
from .db import Base




class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    goal_amount = Column(Integer, nullable=False)
    deadline = Column(DateTime, nullable=False)
    number_of_contributions = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="projects") 
    contributions = relationship("Contribution", back_populates="project")
