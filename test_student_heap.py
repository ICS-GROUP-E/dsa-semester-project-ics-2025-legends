import unittest
from student_heap import StudentHeap
from student import Student
class TestStudentHeap(unittest.TestCase):
    def setUp(self):
        self.students = [
            Student("P12345", "Allan", "Computer Science", 2, 3.85),
            Student("P12346", "John", "CPA", 3, 3.92),
            Student("P12347", "Mike", "Mechanical Engineering", 4, 3.67),
            Student("P12348", "Eve", "Acturial Science", 2, 3.99),
            Student("P12349", "Bob", "Civil Engineering", 3, 3.75),
            Student("P12340", "Alice", "Computer Science", 1, 3.80),
           


        ]
        self.heap = StudentHeap()
        for s in self.students:
            self.heap.insert_by_gpa(s)

    def test_insert_and_get_top_students(self):
        top_students = self.heap.get_top_students(3)

        expected_names = ["Eve", "John", "Allan"]
        result_names = [s.name for s in top_students]
        self.assertEqual(result_names, expected_names)

    def test_get_top_students_default(self):
        top_students = self.heap.get_top_students()
        self.assertEqual(len(top_students), 5)

        self.assertEqual(top_students[0].name, "Eve")

if __name__ == "__main__":
    unittest.main()
       