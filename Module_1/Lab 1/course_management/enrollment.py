from typing import Dict, List, Optional
from student import Student
from course import Course


class EnrollmentManager:
    def __init__(self):
        self._students: Dict[str, Student] = {}
        self._courses: Dict[str, Course] = {}

    def add_student(self, student: Student) -> bool:
        if student.student_id in self._students:
            return False
        self._students[student.student_id] = student 
        return True

    def get_student(self, student_id: str) -> Optional[Student]:
        return self._students.get(student_id)

    def add_course(self, course: Course) -> bool:
        if course.course_id in self._courses:
            return False
        self._courses[course.course_id] = course
        return True

    def get_course(self, course_id: str) -> Optional[Course]:
        return self._courses.get(course_id)

    def enroll_student_in_course(self, student_id: str, course_id: str) -> bool:
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        if not student or not course:
            return False
        if course.enroll_student(student_id):
            student.enroll(course_id)
            return True
        return False

    def drop_student_from_course(self, student_id: str, course_id: str) -> bool:
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        if not student or not course:
            return False
        if course.drop_student(student_id):
            student.drop(course_id)
            return True
        return False

    def get_all_students(self) -> List[Student]:
        return list(self._students.values())

    def get_all_courses(self) -> List[Course]:
        return list(self._courses.values())

    def get_students_by_type(self, student_type: str) -> List[Student]:
        type_filter = student_type.lower()
        return [s for s in self._students.values() 
                if type_filter in s.get_student_type().lower()]

    def get_enrolled_students_in_course(self, course_id: str) -> List[Student]:
        if course_id not in self._courses:
            return []
        return [s for s in self._students.values() if course_id in s.enrolled_courses]

    def calculate_average_enrollments(self) -> float:
        if not self._students:
            return 0.0
        total = sum(s.get_enrollment_count() for s in self._students.values())
        return total / len(self._students)

    @classmethod
    def create_sample_data(cls) -> 'EnrollmentManager':
        manager = cls()
        return manager

    @staticmethod
    def validate_email(email: str) -> bool:
        return '@' in email and '.' in email.split('@')[1] if '@' in email else False