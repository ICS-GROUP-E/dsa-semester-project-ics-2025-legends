import sqlite3
from collections import deque

class CourseGraph:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.graph = {}  # In-memory graph

        self._load_courses_from_db()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _load_courses_from_db(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS courses (course_name TEXT PRIMARY KEY, prerequisites TEXT)")
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        for course, prereqs in rows:
            prereq_list = prereqs.split(',') if prereqs else []
            self.graph[course] = prereq_list
            for prereq in prereq_list:
                if prereq not in self.graph:
                    self.graph[prereq] = []
        conn.close()

    def add_course(self, course_name, prerequisites):
        prerequisites_str = ','.join(prerequisites)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO courses (course_name, prerequisites)
            VALUES (?, ?)
        ''', (course_name, prerequisites_str))
        conn.commit()
        conn.close()

        # Update in-memory graph
        self.graph[course_name] = prerequisites
        for prereq in prerequisites:
            if prereq not in self.graph:
                self.graph[prereq] = []

    def get_course_path(self, target_course):
        visited = set()
        path = []

        def dfs(course):
            if course in visited:
                return
            visited.add(course)
            for prereq in self.graph.get(course, []):
                dfs(prereq)
            path.append(course)

        if target_course not in self.graph:
            return []
        dfs(target_course)
        return path[::-1]

    def display_graph(self):
        for course, prereqs in self.graph.items():
            print(f"{course} <- {prereqs}")
