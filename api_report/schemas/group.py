from api_report.ma import ma
from api_report.models.group import GroupModel


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupModel
        fields = ('group_id', 'name', 'students')
        include_relationships = True
        ordered = True
