from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Calculate(Base):
    __tablename__ = 'calculations'
    category = Column(String, primary_key=True)
    goal = Column(Integer)
    years = Column(Float)