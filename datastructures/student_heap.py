import heapq
from app.student import Student  # Adjust import if needed

class StudentHeap:
    def __init__(self):
        self.heap = []

    def insert_by_gpa(self, student):
        # Use negative GPA so higher GPA = higher priority
        heapq.heappush(self.heap, (-student.gpa, student))

    def get_top_students(self, n=5):
        # Sort by actual GPA descending, then return top n students
        sorted_students = sorted(self.heap)  # Lower negative GPA = higher actual GPA
        top_n = sorted_students[:n]
        return [student for _, student in top_n]
