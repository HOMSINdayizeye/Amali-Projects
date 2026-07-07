from typing import List, Dict, Set


class Course:
    def __init__(self, course_id: str, name: str, instructor: str, max_capacity: int = 30):
        self._course_id = course_id
        self._name = name
        self._instructor = instructor
        self._max_capacity = max_capacity
        self._enrolled_students: Set[str] = set()

    @property
    def course_id(self) -> str:
        return self._course_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def instructor(self) -> str:
        return self._instructor

    @property
    def max_capacity(self) -> int:
        return self._max_capacity

    @property
    def enrolled_students(self) -> Set[str]:
        return self._enrolled_students.copy()

    @property
    def available_spots(self) -> int:
        return self._max_capacity - len(self._enrolled_students)

    def enroll_student(self, student_id: str) -> bool:
        if student_id in self._enrolled_students:
            return False
        if len(self._enrolled_students) >= self._max_capacity:
            return False
        self._enrolled_students.add(student_id)
        return True

    def drop_student(self, student_id: str) -> bool:
        if student_id in self._enrolled_students:
            self._enrolled_students.remove(student_id)
            return True
        return False

    def get_roster_count(self) -> int:
        return len(self._enrolled_students)

    def __repr__(self) -> str:
        return f"Course(id={self._course_id}, name={self._name}, instructor={self._instructor}, enrolled={len(self._enrolled_students)})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Course):
            return False
        return self._course_id == other._course_id