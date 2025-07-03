import heapq
from student import Student

class StudentHeap:
    def __init__(self):
        self.heap = []

    def insert_by_gpa(self, student):
        heapq.heappush(self.heap, (-student.gpa, student))

    def get_top_students(self, n=5):
        return [student for _, student in sorted(self.heap, reverse=True)[:n]]
    

if __name__ == "__main__":
    students =[
        Student("P12345", "Allan", "Computer Science", 2, 3.85),
        Student("P12346", "John", "CPA", 3, 3.92),
        Student("P12347", "Mike", "Mechanical Engineering", 4, 3.67),
        Student("P12348", "Eve", "Acturial Science", 2, 3.99),
        Student("P12349", "Bob", "Civil Engineering", 3, 3.75),
        Student("P12340", "Alice", "Computer Science", 1, 3.80),
        
    ]

    heap = StudentHeap()

    for s in students:
        heap.insert_by_gpa(s)

    print("Top 5 students by GPA:")
    for student in heap.get_top_students(5):
        print(student)