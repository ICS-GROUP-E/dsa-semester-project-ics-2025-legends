from graph_branch import CourseGraph

graph = CourseGraph()

# Add a course and its prerequisites
graph.add_course("Algorithms", ["Data Structures"])
graph.add_course("Data Structures", ["Intro to Programming"])

# Display graph
graph.display_graph()

# Recommend path
print("Recommended path for Algorithms:")
print(graph.get_course_path("Algorithms"))
