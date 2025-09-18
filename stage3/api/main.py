import re
from datetime import datetime, date, time
from math import ceil
from fastapi import FastAPI, Depends, Query
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from database import SessionLocal
from models import Post


# -------- Pydantic Schema --------
class PostSchema(BaseModel):
    url: str

    # 選填欄位，預設 None
    board: Optional[str] = None
    author: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    author_ip: Optional[str] = None
    location: Optional[str] = None
    created_date: Optional[date] = None
    created_time: Optional[time] = None
    crawled_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # 對應舊版的 orm_mode
    }


class StatisticsSchema(BaseModel):
    board: Optional[str]
    author: Optional[str]
    time_range_start: Optional[datetime]
    time_range_end: Optional[datetime]
    total_count: int

    model_config = {
        "from_attributes": True
    }


# -------- FastAPI --------
app = FastAPI()

# 設定靜態檔案路徑
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定模板路徑
templates = Jinja2Templates(directory="templates")


def highlight(text: str, keyword: str):
    if not keyword:
        return text
    # 用正則忽略大小寫替換
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)


# 註冊 filter
templates.env.filters["highlight"] = highlight


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    all_posts = db.query(Post).all()
    return all_posts  # 可以直接回傳 ORM model


@app.get("/api/posts")
def get_posts_page(
        request: Request,
        db: Session = Depends(get_db),
        limit: int = Query(50, ge=1, le=100),
        page: int = Query(1, ge=1),
        author: Optional[str] = Query(None),
        board: Optional[str] = Query(None),
        created_date: Optional[str] = Query(None),
        created_time: Optional[str] = Query(None),
        keyword: Optional[str] = Query(None, description="搜尋關鍵字")
):
    query = db.query(Post)

    # 篩選條件
    if author:
        query = query.filter(Post.author.like(f"%{author}%"))
    if board:
        query = query.filter(Post.board == board)
    if created_date:
        query = query.filter(Post.created_date == created_date)
    if created_time:
        query = query.filter(Post.created_time <= created_time)
    if keyword:
        query = query.filter(
            or_(
                Post.title.like(f"%{keyword}%"),
                Post.content.like(f"%{keyword}%")
            )
        )

    # 總數 + 分頁
    total_count = query.count()
    offset = (page - 1) * limit
    posts = query.order_by(Post.created_date.desc(), Post.created_time.desc()).offset(offset).limit(limit).all()

    # 將 QueryParams 轉成 dict
    query_dict = dict(request.query_params)
    prev_query = query_dict.copy()
    next_query = query_dict.copy()
    prev_query["page"] = str(max(page - 1, 1))
    next_query["page"] = str(page + 1)

    total_pages = ceil(total_count / limit)

    return {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": total_pages,
        "prev_query": prev_query,
        "next_query": next_query,
        "keyword": keyword,
        "posts": [
            {
                "id": p.pid,
                "title": p.title,
                "author": p.author,
                "board": p.board,
                "created_date": p.created_date,
                "created_time": p.created_time,
                "content": p.content,
            } for p in posts
        ]
    }


@app.get("/posts")
def get_posts_page(
        request: Request,
        db: Session = Depends(get_db),
        limit: int = Query(50, ge=1, le=100),
        page: int = Query(1, ge=1),
        author: Optional[str] = Query(None),
        board: Optional[str] = Query(None),
        created_date: Optional[str] = Query(None),
        created_time: Optional[str] = Query(None),
        keyword: Optional[str] = Query(None, description="搜尋關鍵字")
):
    query = db.query(Post)

    # 篩選條件
    if author:
        query = query.filter(Post.author.like(f"%{author}%"))
    if board:
        query = query.filter(Post.board == board)
    if created_date:
        query = query.filter(Post.created_date == created_date)
    if created_time:
        query = query.filter(Post.created_time <= created_time)
    if keyword:
        query = query.filter(
            or_(
                Post.title.like(f"%{keyword}%"),
                Post.content.like(f"%{keyword}%")
            )
        )

    # 總數 + 分頁
    total_count = query.count()
    offset = (page - 1) * limit
    posts = query.order_by(Post.created_date.desc(), Post.created_time.desc()).offset(offset).limit(limit).all()

    # 將 QueryParams 轉成 dict
    query_dict = dict(request.query_params)
    prev_query = query_dict.copy()
    next_query = query_dict.copy()
    prev_query["page"] = str(max(page - 1, 1))
    next_query["page"] = str(page + 1)

    total_pages = ceil(total_count / limit)

    return templates.TemplateResponse("article_pages.html", {
        "request": request,
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": total_pages,
        "prev_query": prev_query,
        "next_query": next_query,
        "keyword": keyword,
        "posts": posts
    })


@app.get("/api/posts/{pid}")
def post_detail(pid: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.pid == pid).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    return {
        "id": post.pid,
        "title": post.title,
        "author": post.author,
        "board": post.board,
        "created_date": post.created_date,
        "created_time": post.created_time,
        "content": post.content
    }


@app.get("/posts/{pid}")
def post_detail(pid: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.pid == pid).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    return templates.TemplateResponse(
        "single_article.html",
        {
            "request": request,
            "post": post
        }
    )


@app.get("/api/statistics")
def statistics_page(
        request: Request,
        db: Session = Depends(get_db),
        time_range_start: Optional[str] = Query(None),
        time_range_end: Optional[str] = Query(None),
        board: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        keyword: Optional[str] = Query(None)
):
    query = db.query(Post)

    if board:
        query = query.filter(Post.board == board)
    if author:
        query = query.filter(Post.author.like(f"%{author}%"))
    if time_range_start:
        query = query.filter(Post.created_date >= time_range_start)
    if time_range_end:
        query = query.filter(Post.created_date <= time_range_end)
    if keyword:
        query = query.filter(
            or_(
                Post.title.like(f"%{keyword}%"),
                Post.content.like(f"%{keyword}%")
            )
        )

    total_count = query.count()

    return {
        "board": board,
        "author": author,
        "time_range_start": time_range_start,
        "time_range_end": time_range_end,
        "total_count": total_count
    }


@app.get("/statistics")
def statistics_page(
        request: Request,
        db: Session = Depends(get_db),
        time_range_start: Optional[str] = Query(None),
        time_range_end: Optional[str] = Query(None),
        board: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        keyword: Optional[str] = Query(None)
):
    query = db.query(Post)

    if board:
        query = query.filter(Post.board == board)
    if author:
        query = query.filter(Post.author.like(f"%{author}%"))
    if time_range_start:
        query = query.filter(Post.created_date >= time_range_start)
    if time_range_end:
        query = query.filter(Post.created_date <= time_range_end)
    if keyword:
        query = query.filter(
            or_(
                Post.title.like(f"%{keyword}%"),
                Post.content.like(f"%{keyword}%")
            )
        )

    total_count = query.count()

    return templates.TemplateResponse(
        "statistics.html",
        {
            "request": request,
            "board": board,
            "author": author,
            "time_range_start": time_range_start,
            "time_range_end": time_range_end,
            "total_count": total_count,
            "keyword": keyword
        }
    )


# 新增 POST
@app.post("/api/posts", response_model=PostSchema)
def create_post(post: PostSchema, db: Session = Depends(get_db)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# 修改 PUT
@app.put("/api/posts/{pid}", response_model=PostSchema)
def update_post(pid: int, post: PostSchema, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.pid == pid).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.model_dump().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


# 刪除 DELETE
@app.delete("/api/posts/{pid}")
def delete_post(pid: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.pid == pid).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": f"Post {pid} deleted"}
