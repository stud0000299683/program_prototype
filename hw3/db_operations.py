import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Faculty, Course, Person, Student, Employee, Grade


class UniversityDataHandler:
    def __init__(self, db_url='sqlite:///university.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_faculty(self, name):
        faculty = Faculty(name=name)
        self.session.add(faculty)
        self.session.commit()

    def insert_course(self, name):
        course = Course(name=name)
        self.session.add(course)
        self.session.commit()

    def insert_person(self, surname, name, type='студент'):
        person = Person(surname=surname, name=name, type=type)
        self.session.add(person)
        self.session.commit()
        return person.id

    def insert_student(self, person_id, faculty_id, course_id):
        student = Student(id=person_id, faculty_id=faculty_id, course_id=course_id)
        self.session.add(student)
        self.session.commit()

    def insert_grade(self, subject, score, student_id):
        grade = Grade(subject=subject, score=score, student_id=student_id)
        self.session.add(grade)
        self.session.commit()

    def select_all_faculties(self):
        return self.session.query(Faculty).all()

    def select_all_courses(self):
        return self.session.query(Course).all()

    def select_all_students(self):
        return self.session.query(Student).all()

    def select_all_grades(self):
        return self.session.query(Grade).all()

    def load_data_from_csv(self, filename):
        try:
            df = pd.read_csv(filename)

            for index, row in df.iterrows():
                # Проверка существования факультета
                faculty = self.session.query(Faculty).filter_by(name=row['Факультет']).first()
                if not faculty:
                    faculty = Faculty(name=row['Факультет'])
                    self.session.add(faculty)
                    self.session.commit()
                faculty_id = faculty.id

                # Проверка существования курса
                course = self.session.query(Course).filter_by(name=row['Курс']).first()
                if not course:
                    course = Course(name=row['Курс'])
                    self.session.add(course)
                    self.session.commit()
                course_id = course.id

                # Создание персоны (студента)
                person_id = self.insert_person(row['Фамилия'], row['Имя'])

                # Создание студента
                self.insert_student(person_id, faculty_id, course_id)

                # Создание оценки
                self.insert_grade(row['Курс'], row['Оценка'], person_id)

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

    def update_faculty(self, faculty_id, new_name):
        faculty = self.session.query(Faculty).get(faculty_id)
        if faculty:
            faculty.name = new_name
            self.session.commit()
        else:
            print("Факультет не найден.")

    def update_course(self, course_id, new_name):
        course = self.session.query(Course).get(course_id)
        if course:
            course.name = new_name
            self.session.commit()
        else:
            print("Курс не найден.")

    def update_person(self, person_id, surname, name, type):
        person = self.session.query(Person).get(person_id)
        if person:
            person.surname = surname
            person.name = name
            person.type = type
            self.session.commit()
        else:
            print("Персона не найдена.")

    def update_student(self, student_id, faculty_id, course_id):
        student = self.session.query(Student).get(student_id)
        if student:
            student.faculty_id = faculty_id
            student.course_id = course_id
            self.session.commit()
        else:
            print("Студент не найден.")

    def update_grade(self, grade_id, subject, score):
        grade = self.session.query(Grade).get(grade_id)
        if grade:
            grade.subject = subject
            grade.score = score
            self.session.commit()
        else:
            print("Оценка не найдена.")

    def delete_faculty(self, faculty_id):
        faculty = self.session.query(Faculty).get(faculty_id)
        if faculty:
            self.session.delete(faculty)
            self.session.commit()
        else:
            print("Факультет не найден.")

    def delete_course(self, course_id):
        course = self.session.query(Course).get(course_id)
        if course:
            self.session.delete(course)
            self.session.commit()
        else:
            print("Курс не найден.")

    def delete_person(self, person_id):
        person = self.session.query(Person).get(person_id)
        if person:
            self.session.delete(person)
            self.session.commit()
        else:
            print("Персона не найдена.")

    def delete_student(self, student_id):
        student = self.session.query(Student).get(student_id)
        if student:
            self.session.delete(student)
            self.session.commit()
        else:
            print("Студент не найден.")

    def delete_grade(self, grade_id):
        grade = self.session.query(Grade).get(grade_id)
        if grade:
            self.session.delete(grade)
            self.session.commit()
        else:
            print("Оценка не найдена.")


# Пример использования
if __name__ == "__main__":
    handler = UniversityDataHandler()
    handler.load_data_from_csv('students.csv')

    # Проверка данных
    faculties = handler.select_all_faculties()
    for faculty in faculties:
        print(faculty)
