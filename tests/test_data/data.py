from api_university.models.group import GroupModel
from api_university.models.course import CourseModel
from api_university.models.student import StudentModel

# DON'T CHANGE THESE DATA
group_list = [
    GroupModel(group_id=1,
               name="AA-11"),
    GroupModel(group_id=2,
               name="BB-22"),
    GroupModel(group_id=3,
               name="CC-33")
]
course_list = [
    CourseModel(course_id=1,
                name="Math",
                description="Mathematics is the science and study of quality, structure, space, and change."),
    CourseModel(course_id=2,
                name="Chemistry",
                description="Walter H. White : Chemistry is the study of change."),
    CourseModel(course_id=3,
                name="English",
                description="You really need to learn English, lazy ass")
]

student_list = [
    StudentModel(student_id=1,
                 first_name="Joseph",
                 last_name="Anderson",
                 group_id=2,
                 courses=[course_list[0]]),
    StudentModel(student_id=2,
                 first_name="Maria",
                 last_name="Johnson",
                 group_id=1,
                 courses=[course_list[1], course_list[2]]),
    StudentModel(student_id=3,
                 first_name="Joseph",
                 last_name="Johnson",
                 group_id=2,
                 courses=[course_list[0]]),
    StudentModel(student_id=4,
                 first_name="Patricia",
                 last_name="Williams",
                 courses=[course_list[0], course_list[1], course_list[2]]),
    StudentModel(student_id=5,
                 first_name="William",
                 last_name="Miller"),
    StudentModel(student_id=6,
                 first_name="Dorothy",
                 last_name="Miller",
                 group_id=1,
                 courses=[course_list[1]]),
    StudentModel(student_id=7,
                 first_name="Elizabeth",
                 last_name="Brown",
                 group_id=2,
                 courses=[course_list[0], course_list[2]]),
    StudentModel(student_id=8,
                 first_name="Richard",
                 last_name="Clark",
                 group_id=3),
    StudentModel(student_id=9,
                 first_name="Margaret",
                 last_name="Clark",
                 group_id=1,
                 courses=[course_list[2], course_list[1], course_list[0]]),
    StudentModel(student_id=10,
                 first_name="Susan",
                 last_name="Smith",
                 group_id=3,
                 courses=[course_list[0], course_list[1]])
]

student_count = len(student_list)
group_count = len(group_list)
course_count = len(course_list)
