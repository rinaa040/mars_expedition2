from flask_wtf import FlaskForm
from wtforms import EmailField, DateField, IntegerField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    team_leader = IntegerField('Id руководителя', validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])
    collaborations = StringField('Список id участников', validators=[DataRequired()])
    is_finished = BooleanField('Признак завершения')