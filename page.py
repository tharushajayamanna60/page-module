from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from models import Page, User
from database import get_db
from auth import get_current_user, is_admin

router = APIRouter()


# =============================
# Pydantic Schemas
# =============================

class PageCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    mentions: Optional[List[str]] = []
    status: Optional[str] = "draft"  # or 'published'


class PageEdit(PageCreate):
    pass


# =============================
# Routes
# =============================

@router.post("/page/create")
def create_page(data: PageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.verified:
        raise HTTPException(status_code=403, detail="Account verification required")

    new_page = Page(
        title=data.title,
        content=data.content,
        tags=",".join(data.tags),
        mentions=",".join(data.mentions),
        status=data.status,
        owner_id=user.id
    )
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return {"message": "Page created", "page_id": new_page.id}


@router.put("/page/edit/{page_id}")
def edit_page(page_id: int, data: PageEdit, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    page = db.query(Page).filter(Page.id == page_id, Page.owner_id == user.id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found or unauthorized")

    page.title = data.title
    page.content = data.content
    page.tags = ",".join(data.tags)
    page.mentions = ",".join(data.mentions)
    page.status = data.status
    db.commit()
    return {"message": "Page updated"}


@router.get("/page/{page_id}")
def view_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


# =============================
# Admin Functionality
# =============================

@router.post("/admin/login")
def admin_login(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": "Welcome admin!"}


@router.get("/admin/pages")
def get_all_pages(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return db.query(Page).all()
