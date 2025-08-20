from typing import Optional
from ..extensions import db
from ..models import Student

class StudentService:
    """Service for Student entity CRUD."""
    def get(self, id_: int) -> Optional[Student]:
        return db.session.get(Student, id_)

    def create(self, **data) -> Student:
        student = Student(**data)
        db.session.add(student)
        db.session.commit()
        return student

    def update(self, student: Student, **data) -> Student:
        for k, v in data.items():
            setattr(student, k, v)
        db.session.commit()
        return student

    def delete(self, student: Student) -> None:
        db.session.delete(student)
        db.session.commit()
