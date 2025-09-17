from sqlalchemy import Column, INTEGER, String, TEXT, DATETIME, Date, Time, SMALLINT, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    pid = Column(INTEGER, primary_key=True, index=True)
    board = Column(String(50), nullable=True)
    author = Column(String(50), nullable=True)
    author_ip = Column(String(50), nullable=True)
    title = Column(String(50), nullable=True)
    content = Column(TEXT, nullable=True)
    location = Column(String(30), nullable=True)
    url = Column(String(80), nullable=False, unique=True)
    created_date = Column(Date, nullable=True)
    created_time = Column(Time, nullable=True)
    crawled_at = Column(DATETIME, nullable=True)


class Comment(Base):
    __tablename__ = "comments"
    cid = Column(INTEGER, primary_key=True, index=True)
    content = Column(TEXT, nullable=True)
    author = Column(String(100), nullable=True)
    author_ip = Column(String(50), nullable=True)
    created_date = Column(Date, nullable=True)
    created_time = Column(Time, nullable=True)
    is_push = Column(SMALLINT, nullable=True)
    is_boo = Column(SMALLINT, nullable=True)
    url = Column(String(255), nullable=True, unique=True)
    crawled_at = Column(DATETIME, nullable=True)


class PC(Base):
    __tablename__ = "pc"
    pid = Column(INTEGER, ForeignKey('posts.pid'), index=True, nullable=False)
    cid = Column(INTEGER, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("pid", "cid"),
    )
