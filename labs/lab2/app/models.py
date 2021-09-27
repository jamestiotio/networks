from typing import Optional
from pydantic import BaseModel
from fastapi import File, UploadFile


class Student(BaseModel):
    name: str
    id: str
    gpa: Optional[float] = None
    phone_number: Optional[int] = None
    photo_file: Optional[UploadFile] = File(None, media_type="image/png")