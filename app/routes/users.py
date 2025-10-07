from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# READ ALL
@router.get("/", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# READ ONE
@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id)

# UPDATE
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user)

# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)
