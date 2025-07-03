import tkinter as tk
from tkinter import messagebox, simpledialog
from src.linkedlist import StudentLinkedList
from datastructure.stack import ActionStack
from model.student import Student
from student_heap import StudentHeap
from graph_branch import CourseGraph
from database import StudentDatabase


class StudentApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Student Record System")
        self.window.geometry("800x600")

        # Core systems
        self.linked_list = StudentLinkedList()
        self.undo_stack = ActionStack()
        self.heap = StudentHeap()
        self.graph = CourseGraph()
        self.db = StudentDatabase()

        # Load DB students into linked list and heap
        self._load_students()

        self._create_widgets()

    def _load_students(self):
        for s in self.db.list_all():
            student = Student(*s)
            self.linked_list.add_student(student.student_id, student.name, student.course, student.gpa)
            self.heap.insert_by_gpa(student)

    def _create_widgets(self):
        title = tk.Label(self.window, text="Student Record System", font=("Helvetica", 20))
        title.pack(pady=10)

        # Inputs
        form = tk.Frame(self.window)
        form.pack()

        tk.Label(form, text="ID:").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Name:").grid(row=1, column=0)
        self.name_entry = tk.Entry(form)
        self.name_entry.grid(row=1, column=1)

        tk.Label(form, text="Course:").grid(row=2, column=0)
        self.course_entry = tk.Entry(form)
        self.course_entry.grid(row=2, column=1)

        tk.Label(form, text="Year:").grid(row=3, column=0)
        self.year_entry = tk.Entry(form)
        self.year_entry.grid(row=3, column=1)

        tk.Label(form, text="GPA:").grid(row=4, column=0)
        self.gpa_entry = tk.Entry(form)
        self.gpa_entry.grid(row=4, column=1)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add", command=self.add_student).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Search", command=self.search_student).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_student).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Show All", command=self.show_all_students).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Undo Delete", command=self.undo_delete).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Top Performers", command=self.show_top_students).grid(row=0, column=5, padx=5)
        tk.Button(button_frame, text="Course Path", command=self.recommend_path).grid(row=0, column=6, padx=5)

        # Output display
        self.display = tk.Text(self.window, height=20, width=90)
        self.display.pack()

    def add_student(self):
        try:
            student_id = self.id_entry.get().strip()
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            year = int(self.year_entry.get().strip())
            gpa = float(self.gpa_entry.get().strip())

            student = Student(student_id, name, course, year, gpa)
            self.linked_list.add_student(student_id, name, course, gpa)
            self.db.add(student)
            self.heap.insert_by_gpa(student)

            self.display.insert(tk.END, f"✅ Added student {student_id}\n")
            self._clear_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_student(self):
        student_id = self.id_entry.get().strip()
        student = self.linked_list.search_student(student_id)
        self.display.delete(1.0, tk.END)
        if student:
            self.display.insert(tk.END, f"🔍 Found:\n{student}\n")
        else:
            self.display.insert(tk.END, "❌ Student not found\n")

    def delete_student(self):
        student_id = self.id_entry.get().strip()
        student_data = self.linked_list.search_student(student_id)
        if student_data:
            student = self.db.get(student_id)
            self.undo_stack.push("delete", student)
            self.linked_list.delete_student(student_id)
            self.db.remove(student_id)
            self.display.insert(tk.END, f"🗑️ Deleted student {student_id}\n")
        else:
            self.display.insert(tk.END, f"❌ Student {student_id} not found\n")

    def show_all_students(self):
        self.display.delete(1.0, tk.END)
        current = self.linked_list.head
        if not current:
            self.display.insert(tk.END, "No students found\n")
            return
        while current:
            self.display.insert(tk.END,
                f"ID: {current.student_id}, Name: {current.name}, "
                f"Course: {current.course}, GPA: {current.gpa}\n")
            current = current.next

    def undo_delete(self):
        action = self.undo_stack.pop()
        if not action:
            self.display.insert(tk.END, "⚠️ Nothing to undo\n")
            return

        action_type, student = action
        if action_type == "delete":
            self.linked_list.add_student(student.student_id, student.name, student.course, student.gpa)
            self.db.add(student)
            self.display.insert(tk.END, f"↩️ Restored student {student.student_id}\n")

    def show_top_students(self):
        top = self.heap.get_top_students(5)
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "🎓 Top 5 Students by GPA:\n")
        for s in top:
            self.display.insert(tk.END, f"{s.name} ({s.student_id}) - GPA: {s.gpa}\n")

    def recommend_path(self):
        course = simpledialog.askstring("Course Path", "Enter course name:")
        if course:
            path = self.graph.get_course_path(course)
            self.display.delete(1.0, tk.END)
            if path:
                self.display.insert(tk.END, f"📘 Recommended path for {course}:\n")
                self.display.insert(tk.END, " → ".join(path) + "\n")
            else:
                self.display.insert(tk.END, f"⚠️ No path found for '{course}'\n")

    def _clear_inputs(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.gpa_entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = StudentApp()
    app.run()

