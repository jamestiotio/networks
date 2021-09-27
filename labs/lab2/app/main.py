#!/usr/bin/env python3
# SUTD 50.012 Networks Lab 2
# James Raphael Tiovalen (1004555)

from fastapi import FastAPI, Response, Depends
from typing import Optional
import redis
from models import Student

app = FastAPI()

students = [
    {"name": "Alice", "id": "1004803", "gpa": 4.0},
    {"name": "Bob", "id": "1004529", "gpa": 3.6},
    {"name": "Charlie", "id": "1004910", "gpa": 5.0},
]


def get_redis_client():
    return redis.Redis(host="redis")


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/students")
def get_students(sortBy: Optional[str] = None, limit: Optional[int] = None):
    if sortBy is not None and limit is not None:
        if sortBy == "name":
            return sorted(students, key=lambda x: x.name)[:limit]
        elif sortBy == "id":
            return sorted(students, key=lambda x: x.id)[:limit]
        elif sortBy == "gpa":
            return sorted(students, key=lambda x: x.gpa)[:limit]
    return students


@app.get("/students/{student_id}")
def find_student(student_id: str, response: Response):
    global students
    for student in students:
        if student["id"] == student_id:
            return student
    response.status_code = 404
    return None


@app.post("/students")
def create_student(
    student: Student, redis_client: redis.Redis = Depends(get_redis_client)
):
    global students
    students.append({"name": student.name, "id": student.id, "gpa": student.gpa})
    return "Student created!"


@app.delete("/students")
def delete_multiple_students_below_gpa(min_gpa: float):
    pass