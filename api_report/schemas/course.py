from api_report.ma import ma
from api_report.models.course import CourseModel


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CourseModel
        fields = ('course_id', 'name', 'description', 'students')
        include_relationships = True
        ordered = True
