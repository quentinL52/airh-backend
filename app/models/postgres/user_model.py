from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"  

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    google_id = Column(String, unique=True, nullable=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)
    candidate_mongo_id = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    auth_providers = Column(JSON, default=list)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)