from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_project import crud, models, schemas
from fastapi_project.database import SessionLocal, engine
from typing import List

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(
    username: str, email: str, hashed_password: str, db: Session = Depends(get_db)
):
    db_user = crud.create_user(
        db=db, username=username, email=email, hashed_password=hashed_password
    )
    return db_user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User is not found")
    return db_user


@app.post("/courses/", response_model=schemas.Course)
def create_course(
    name: str, description: str, user_id: int, db: Session = Depends(get_db)
):
    db_course = crud.create_course(
        db=db, name=name, description=description, user_id=user_id
    )
    return db_course


@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db=db, skip=skip, limit=limit)
    return courses


@app.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course is not found")
    return db_course