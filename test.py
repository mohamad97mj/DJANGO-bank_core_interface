class Student:
    def __init__(self, name):
        self.name = name


def create_student(cls):
    return cls("mohamad")


x = create_student(Student)
print(x.name)
