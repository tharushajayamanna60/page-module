from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy function to simulate auth
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.username == token).first()  # Simplified for now
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user

def is_admin(user: User = Depends(get_current_user)) -> bool:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return True
