from abc import ABC, abstractmethod
from typing import List, Optional


class Student(ABC):
    def __init__(self, student_id: str, name: str, email: str):
        self._student_id = student_id
        self._name = name
        self._email = email
        self._enrolled_courses: List[str] = []

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def enrolled_courses(self) -> List[str]:
        return self._enrolled_courses.copy()

    def enroll(self, course_id: str) -> None:
        self._enrolled_courses.append(course_id)

    def drop(self, course_id: str) -> bool:
        if course_id in self._enrolled_courses:
            self._enrolled_courses.remove(course_id)
            return True
        return False

    def get_enrollment_count(self) -> int:
        return len(self._enrolled_courses)

    @abstractmethod
    def get_student_type(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"Student(id={self._student_id}, name={self._name}, type={self.get_student_type()})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Student):
            return False
        return self._student_id == other._student_id


class UndergraduateStudent(Student):
    def __init__(self, student_id: str, name: str, email: str, year: int = 1):
        super().__init__(student_id, name, email)
        self._year = year

    @property
    def year(self) -> int:
        return self._year

    def get_student_type(self) -> str:
        return f"Undergraduate (Year {self._year})"


class GraduateStudent(Student):
    def __init__(self, student_id: str, name: str, email: str, program: str = "Masters"):
        super().__init__(student_id, name, email)
        self._program = program

    @property
    def program(self) -> str:
        return self._program

    def get_student_type(self) -> str:
        return f"Graduate ({self._program})"