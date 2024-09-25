from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1 import schemas, services
from app.db.session import get_db
from app.core.security import create_access_token, authenticate_user, get_current_user

from datetime import timedelta
router = APIRouter()

@router.post("/upload", response_model=schemas.FileResponse)
def upload_file(
    file: schemas.FileUpload, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)  # Agregar protección aquí
):
    return services.upload_file(db, file)

@router.get("/files/{file_id}", response_model=schemas.FileResponse)
def get_file(
    file_id: int, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)  # Agregar protección aquí
):
    db_file = services.get_file(db, file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return services.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}