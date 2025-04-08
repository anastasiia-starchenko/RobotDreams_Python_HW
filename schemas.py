from pydantic import BaseModel
from typing import List, Optional

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    owner: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    courses: List[CourseResponse]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class AssignmentCreate(BaseModel):
    course_id: int
    student_id: int
    grade: Optional[int] = None


class AssignmentResponse(BaseModel):
    id: int
    course_id: int
    student_id: int
    grade: Optional[int] = None

    class Config:
        orm_mode = True