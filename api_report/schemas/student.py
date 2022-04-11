from api_report.ma import ma
from api_report.models.student import StudentModel
from .course import CourseSchema
from .group import GroupSchema


class ShortStudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StudentModel
        ordered = True

    student_id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    group_name = ma.Function(lambda obj: None if obj.group is None else obj.group.name)
    course_names = ma.Function(lambda obj: ", ".join(list(map(lambda course: course.name, obj.courses))))


class FullStudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
        fields = ('student_id', 'first_name', 'last_name', 'group', 'courses')
        include_fk = True
        include_relationships = True
        ordered = True

    # field which contain list of courses
    courses = ma.Nested(CourseSchema(only=('course_id', 'name', 'description')), many=True)
    # field which contain group fields as dictionary
    group = ma.Nested(GroupSchema(only=('group_id', 'name',)))




