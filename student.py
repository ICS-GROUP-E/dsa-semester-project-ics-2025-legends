class Student:
    def __init__(self, id,name,course,year,gpa):
        self.id = id
        self.name = name
        self.course = course
        self.year = year
        self.gpa = gpa


    def __repr__(self):
        return (f"Student(id-{self.id}, name='{self.name}', course='{self.course}', "
                f"year={self.year}, gpa={self.gpa})")
