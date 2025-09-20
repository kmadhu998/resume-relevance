
# Simple SQLAlchemy models scaffold (not used in MVP Streamlit-only but included for future)
from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    raw_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    raw_text = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Evaluation(Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    job_id = Column(Integer)
    score = Column(Integer)
    verdict = Column(String)
    missing = Column(JSON)
