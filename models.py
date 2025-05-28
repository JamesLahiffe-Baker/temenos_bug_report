from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default="regular")  # roles: admin, regular
    created_at = Column(DateTime, default=datetime.utcnow)

class Website(Base):
    __tablename__ = "websites"
    website_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

class BugReport(Base):
    __tablename__ = "bug_reports"
    bug_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="Open")
    priority = Column(String, default="Medium")
    reported_at = Column(DateTime, default=datetime.utcnow)
    website_id = Column(Integer, ForeignKey("websites.website_id"))
    reported_by_user_id = Column(Integer, ForeignKey("users.user_id"))
    assigned_admin_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)

    website = relationship("Website")
    reporter = relationship("User", foreign_keys=[reported_by_user_id])
    admin = relationship("User", foreign_keys=[assigned_admin_id])
    comments = relationship("BugComment", back_populates="bug", cascade="all, delete")

class BugComment(Base):
    __tablename__ = "bug_comments"
    comment_id = Column(Integer, primary_key=True)
    bug_id = Column(Integer, ForeignKey("bug_reports.bug_id"))
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey("users.user_id"))

    bug = relationship("BugReport", back_populates="comments")
    user = relationship("User")
