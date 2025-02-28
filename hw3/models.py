from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from sqlalchemy import create_engine

Base = declarative_base()


class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Идентификатор факультета
    name = Column(String(100), nullable=False, unique=True)      # Название факультета

    def __repr__(self):
        return f"<Faculty(id={self.id}, name={self.name})>"


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Идентификатор курса
    name = Column(String(100), nullable=False, unique=True)      # Название курса

    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name})>"


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Идентификатор персоны
    surname = Column(String(50), nullable=False)                 # Фамилия
    name = Column(String(50), nullable=False)                    # Имя
    type = Column(String(10), nullable=False)                    # Тип (студент или сотрудник)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)  # ID студента (внешний ключ на Person)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=False)  # Внешний ключ на факультет
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)      # Внешний ключ на курс

    person = relationship("Person")  # Связь с таблицей Person
    faculty = relationship("Faculty")  # Связь с таблицей Faculty
    course = relationship("Course")     # Связь с таблицей Course


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)  # ID сотрудника (внешний ключ на Person)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=False)  # Внешний ключ на факультет
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)  # Внешний ключ на курс

    person = relationship("Person")  # Связь с таблицей Person
    faculty = relationship("Faculty")  # Связь с таблицей Faculty
    course = relationship("Course")     # Связь с таблицей Course


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Идентификатор оценки
    subject = Column(String(100), nullable=False)                # Название предмета
    score = Column(Integer, nullable=False)                      # Оценка
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # Внешний ключ на студента

    student = relationship("Student")  # Связь с таблицей студентов


if __name__ == "__main__":
    engine = create_engine('sqlite:///university.db')
    Base.metadata.create_all(engine)
