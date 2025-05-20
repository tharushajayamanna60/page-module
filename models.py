from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    pages = relationship("Page", back_populates="owner")


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(String)       # comma-separated
    mentions = Column(String)   # comma-separated
    status = Column(String, default="draft")  # e.g., "draft", "published"

    owner = relationship("User", back_populates="pages")
  
