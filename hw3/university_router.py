from fastapi import APIRouter, Depends
from pydantic import BaseModel


from db_operations import UniversityDataHandler
from models import Person
from dependencies import get_current_user, check_read_only_access


router = APIRouter(prefix="/university", tags=["University"])

# Инициализация обработчика данных
handler = UniversityDataHandler()


# Модели для запросов
class FacultyModel(BaseModel):
    id: int
    name: str


class CourseModel(BaseModel):
    id: int
    name: str


class PersonModel(BaseModel):
    id: int
    surname: str
    name: str
    type: str


class StudentModel(BaseModel):
    id: int
    faculty_id: int
    course_id: int


class GradeModel(BaseModel):
    id: int
    subject: str
    score: int


# Эндпойнты для CRUD-операций
# Создание


# Для всех эндпоинтов добавить зависимости
@router.post("/faculties/")
def create_faculty(faculty: FacultyModel, user: Person = Depends(get_current_user)):
    handler.insert_faculty(faculty.name)
    return {"message": "Факультет создан"}

@router.get("/faculties/")
def read_faculties(user: Person = Depends(get_current_user)):
    return handler.select_all_faculties()

# Для read-only пользователей
@router.delete("/faculties/{faculty_id}")
def delete_faculty(faculty_id: int, user: Person = Depends(check_read_only_access)):
    handler.delete_faculty(faculty_id)
    return {"message": "Факультет удален"}



@router.post("/courses/")
def create_course(course: CourseModel, user: Person = Depends(get_current_user)):
    handler.insert_course(course.name)
    return {"message": "Курс создан"}


@router.post("/persons/")
def create_person(person: PersonModel, user: Person = Depends(get_current_user)):
    handler.insert_person(person.surname, person.name, person.type)
    return {"message": "Персона создана"}


@router.post("/students/")
def create_student(student: StudentModel, user: Person = Depends(get_current_user)):
    handler.insert_student(student.id, student.faculty_id, student.course_id)
    return {"message": "Студент создан"}


@router.post("/grades/")
def create_grade(grade: GradeModel, user: Person = Depends(get_current_user)):
    handler.insert_grade(grade.subject, grade.score, grade.id)
    return {"message": "Оценка создана"}


# Чтение

@router.get("/courses/")
def read_courses(user: Person = Depends(get_current_user)):
    return handler.select_all_courses()


@router.get("/persons/")
def read_persons(user: Person = Depends(get_current_user)):
    return handler.session.query(Person).all()


@router.get("/students/")
def read_students(user: Person = Depends(get_current_user)):
    return handler.select_all_students()


@router.get("/grades/")
def read_grades(user: Person = Depends(get_current_user)):
    return handler.select_all_grades()


# Обновление

@router.put("/courses/{course_id}")
def update_course(course_id: int, course: CourseModel, user: Person = Depends(get_current_user)):
    handler.update_course(course_id, course.name)
    return {"message": "Курс обновлен"}


@router.put("/persons/{person_id}")
def update_person(person_id: int, person: PersonModel, user: Person = Depends(get_current_user)):
    handler.update_person(person_id, person.surname, person.name, person.type)
    return {"message": "Персона обновлена"}


@router.put("/students/{student_id}")
def update_student(student_id: int, student: StudentModel, user: Person = Depends(get_current_user)):
    handler.update_student(student_id, student.faculty_id, student.course_id)
    return {"message": "Студент обновлен"}


@router.put("/grades/{grade_id}")
def update_grade(grade_id: int, grade: GradeModel, user: Person = Depends(get_current_user)):
    handler.update_grade(grade_id, grade.subject, grade.score)
    return {"message": "Оценка обновлена"}


# Удаление
@router.delete("/faculties/{faculty_id}")
def delete_faculty(faculty_id: int, user: Person = Depends(get_current_user)):
    handler.delete_faculty(faculty_id)
    return {"message": "Факультет удален"}


@router.delete("/courses/{course_id}")
def delete_course(course_id: int, user: Person = Depends(get_current_user)):
    handler.delete_course(course_id)
    return {"message": "Курс удален"}


@router.delete("/persons/{person_id}")
def delete_person(person_id: int, user: Person = Depends(get_current_user)):
    handler.delete_person(person_id)
    return {"message": "Персона удалена"}


@router.delete("/students/{student_id}")
def delete_student(student_id: int, user: Person = Depends(get_current_user)):
    handler.delete_student(student_id)
    return {"message": "Студент удален"}


@router.delete("/grades/{grade_id}")
def delete_grade(grade_id: int, user: Person = Depends(get_current_user)):
    handler.delete_grade(grade_id)
    return {"message": "Оценка удалена"}
