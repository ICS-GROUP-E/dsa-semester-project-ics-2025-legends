import tkinter as tk
from tkinter import ttk
from model.student import Student
from src.linkedlist import LinkedList
from datastucture.stack import Stack
from student_heap import StudentHeap
from graph_branch import CourseGraph
from database import save_to_db, fetch_all_students


class StudentApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Student Record System")
        self.window.geometry("750x500")

        # Data structures
        self.student_list = LinkedList()
        self.undo_stack = Stack()
        self.heap = StudentHeap()
        self.graph = CourseGraph()

        self.create_widgets()
        self.load_from_db()

    def create_widgets(self):
        title = tk.Label(self.window, text="Student Record System", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        input_frame = tk.Frame(self.window)
        input_frame.pack()

        labels = ["ID", "Name", "Course", "GPA"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(input_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label.lower()] = entry

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Student", command=self.add_student, bg="#99ffcc").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Student", command=self.delete_student, bg="#ff9999").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Undo Delete", command=self.undo_delete, bg="#ffff99").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Search Student", command=self.search_student, bg="#ccffcc").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show All", command=self.show_students, bg="#cce6ff").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Top Students", command=self.show_top_students, bg="#b3b3ff").pack(side=tk.LEFT, padx=5)

        self.display_area = tk.Text(self.window, height=15, width=85)
        self.display_area.pack(pady=10)

    def add_student(self):
        try:
            student_id = self.entries["id"].get().strip()
            name = self.entries["name"].get().strip()
            course = self.entries["course"].get().strip()
            gpa = float(self.entries["gpa"].get().strip())

            if not (student_id and name and course):
                self.display_area.insert(tk.END, "⚠️ Fill in all fields!\n")
                return

            student = Student(student_id, name, course, 0, gpa)
            self.student_list.add_student(student)
            self.heap.insert_by_gpa(student)
            save_to_db(self.student_list)

            self.display_area.insert(tk.END, f"✅ Added: {name} ({student_id})\n")
            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except ValueError:
            self.display_area.insert(tk.END, "❌ GPA must be a number.\n")

    def delete_student(self):
        student_id = self.entries["id"].get().strip()
        if not student_id:
            self.display_area.insert(tk.END, "⚠️ Enter student ID to delete.\n")
            return

        student = self.student_list.delete_student(student_id)
        if student:
            self.undo_stack.push(student)
            save_to_db(self.student_list)
            self.display_area.insert(tk.END, f"🗑️ Deleted student {student_id}\n")
        else:
            self.display_area.insert(tk.END, f"❌ Student {student_id} not found.\n")

    def undo_delete(self):
        student = self.undo_stack.pop()
        if student:
            self.student_list.add_student(student)
            save_to_db(self.student_list)
            self.display_area.insert(tk.END, f"🔁 Restored: {student.name} ({student.student_id})\n")
        else:
            self.display_area.insert(tk.END, "⚠️ Nothing to undo.\n")

    def search_student(self):
        student_id = self.entries["id"].get().strip()
        if not student_id:
            self.display_area.insert(tk.END, "⚠️ Enter student ID to search.\n")
            return

        student = self.student_list.search_student(student_id)
        self.display_area.delete(1.0, tk.END)

        if student:
            self.display_area.insert(tk.END,
                f"🔎 Found:\nID: {student.student_id}\nName: {student.name}\nCourse: {student.course}\nGPA: {student.gpa}\n")
        else:
            self.display_area.insert(tk.END, f"❌ No student found with ID {student_id}\n")

    def show_students(self):
        self.display_area.delete(1.0, tk.END)
        current = self.student_list.head

        if not current:
            self.display_area.insert(tk.END, "No students to show.\n")
            return

        while current:
            s = current
            self.display_area.insert(tk.END,
                f"ID: {s.student_id} | Name: {s.name} | Course: {s.course} | GPA: {s.gpa}\n")
            current = current.next

    def show_top_students(self):
        self.display_area.delete(1.0, tk.END)
        top = self.heap.get_top_students(5)

        if not top:
            self.display_area.insert(tk.END, "No top students yet.\n")
            return

        self.display_area.insert(tk.END, "🏆 Top Performers:\n")
        for s in top:
            self.display_area.insert(tk.END, f"{s.name} ({s.student_id}) - GPA: {s.gpa}\n")

    def load_from_db(self):
        rows = fetch_all_students()
        for row in rows:
            student = Student(*row)
            self.student_list.add_student(student)
            self.heap.insert_by_gpa(student)


if __name__ == "__main__":
    app = StudentApp()
    app.window.mainloop()
