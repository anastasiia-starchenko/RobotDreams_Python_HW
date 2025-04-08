from sqlalchemy.orm import Session
from fastapi_project import models, schemas


def create_user(db: Session, username: str, email: str, hashed_password: str):
    db_user = models.User(
        username=username, email=email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_course(db: Session, name: str, description: str, user_id: int):
    db_course = models.Course(name=name, description=description, user_id=user_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()