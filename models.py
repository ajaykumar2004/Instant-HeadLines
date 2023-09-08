# models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Headline(Base):
    __tablename__ = 'headlines'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    timestamp = Column(DateTime)
