from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, URL


class NewsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired(), URL()])
    source_link = StringField('source_link', validators=[DataRequired(), URL()])
    category = SelectField(choices=[
        ("sport", "sport"),
        ("health", "health"),
        ("politics", "politics")], validators=[DataRequired()])
