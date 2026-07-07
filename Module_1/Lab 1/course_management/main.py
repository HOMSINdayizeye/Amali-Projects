from student import UndergraduateStudent, GraduateStudent
from course import Course
from enrollment import EnrollmentManager


def main():
    manager = EnrollmentManager()
    
    while True:
        print("\n=== Student Course Management System ===")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student in Course")
        print("4. View Student Summary")
        print("5. View Course Roster")
        print("6. View All Students")
        print("7. View All Courses")
        print("8. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            student_id = input("Student ID: ").strip()
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            student_type = input("Type (U for Undergraduate, G for Graduate): ").strip().upper()
            
            if student_type == 'U':
                year = int(input("Year (1-4): ").strip())
                student = UndergraduateStudent(student_id, name, email, year)
            elif student_type == 'G':
                program = input("Program (Masters/PhD): ").strip()
                student = GraduateStudent(student_id, name, email, program)
            else:
                print("Invalid type!")
                continue
            
            if manager.add_student(student):
                print(f"Added: {repr(student)}")
            else:
                print("Student ID already exists!")
                
        elif choice == '2':
            course_id = input("Course ID: ").strip()
            name = input("Course Name: ").strip()
            instructor = input("Instructor: ").strip()
            
            course = Course(course_id, name, instructor)
            if manager.add_course(course):
                print(f"Added: {repr(course)}")
            else:
                print("Course ID already exists!")
                
        elif choice == '3':
            student_id = input("Student ID: ").strip()
            course_id = input("Course ID: ").strip()
            if manager.enroll_student_in_course(student_id, course_id):
                print("Enrollment successful!")
            else:
                print("Enrollment failed! Check student/course IDs.")
                
        elif choice == '4':
            student_id = input("Student ID: ").strip()
            student = manager.get_student(student_id)
            if student:
                print(f"\n{repr(student)}")
                print(f"Enrolled courses: {student.enrolled_courses}")
            else:
                print("Student not found!")
                
        elif choice == '5':
            course_id = input("Course ID: ").strip()
            course = manager.get_course(course_id)
            if course:
                students = manager.get_enrolled_students_in_course(course_id)
                print(f"\nRoster for {course.name}:")
                for s in students:
                    print(f"  - {s.name} ({s.student_id}) ({s.email}) - {s.get_student_type()}")
                print(f"Average enrollments: {manager.calculate_average_enrollments():.2f}")
            else:
                print("Course not found!")
                
        elif choice == '6':
            students = manager.get_all_students()
            print(f"\nTotal Students: {len(students)}")
            for s in students:
                print(f"  {repr(s)}")
                
        elif choice == '7':
            courses = manager.get_all_courses()
            print(f"\nTotal Courses: {len(courses)}")
            for c in courses:
                print(f"  {repr(c)}")
                
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()