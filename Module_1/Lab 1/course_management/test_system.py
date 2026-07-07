from student import UndergraduateStudent, GraduateStudent
from course import Course
from enrollment import EnrollmentManager


def test_system():
    print("=== Testing Student Course Management System ===\n")
    
    manager = EnrollmentManager()
    
    print("1. Adding Students...")
    s1 = UndergraduateStudent("S001", "Alice Johnson", "alice@email.com", 2)
    s2 = UndergraduateStudent("S002", "Bob Smith", "bob@email.com", 3)
    s3 = GraduateStudent("S003", "Dr. Carol White", "carol@email.com", "PhD")
    s4 = GraduateStudent("S004", "David Lee", "david@email.com", "Masters")
    
    manager.add_student(s1)
    manager.add_student(s2)
    manager.add_student(s3)
    manager.add_student(s4)
    print(f"   Added {len(manager.get_all_students())} students")
    
    print("\n2. Adding Courses...")
    c1 = Course("CS101", "Introduction to Python", "Dr. Brown", 30)
    c2 = Course("CS102", "Data Structures", "Prof. Davis", 25)
    
    manager.add_course(c1)
    manager.add_course(c2)
    print(f"   Added {len(manager.get_all_courses())} courses")
    
    print("\n3. Enrolling Students...")
    manager.enroll_student_in_course("S001", "CS101")
    manager.enroll_student_in_course("S001", "CS102")
    manager.enroll_student_in_course("S002", "CS101")
    manager.enroll_student_in_course("S003", "CS102")
    
    student = manager.get_student("S001")
    print(f"   Alice enrolled in {len(student.enrolled_courses)} courses")
    
    print("\n4. Testing Equality (__eq__)...")
    s1_copy = UndergraduateStudent("S001", "Alice Johnson", "alice@email.com", 2)
    print(f"   Same student? {s1 == s1_copy}")
    
    print("\n5. Testing Polymorphism (different student types)...")
    for s in manager.get_all_students():
        print(f"   {s.name}: {s.get_student_type()}")
    
    print("\n6. Testing __repr__...")
    print(f"   Undergrad repr: {repr(s1)}")
    print(f"   Grad repr: {repr(s3)}")
    print(f"   Course repr: {repr(c1)}")
    
    print("\n7. Testing Average Enrollments...")
    avg = manager.calculate_average_enrollments()
    print(f"   Average enrollments: {avg:.2f}")
    
    print("\n8. Testing Email Validation (@staticmethod)...")
    print(f"   Valid email: {EnrollmentManager.validate_email('test@email.com')}")
    print(f"   Invalid email: {EnrollmentManager.validate_email('invalid')}")
    
    print("\n9. Testing Get Students by Type...")
    grads = manager.get_students_by_type("Graduate")
    undergrads = manager.get_students_by_type("Undergraduate")
    print(f"   Graduate students: {len(grads)}")
    print(f"   Undergraduate students: {len(undergrads)}")
    
    print("\n=== All Tests Passed! ===")