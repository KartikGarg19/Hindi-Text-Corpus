from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length

class MovieInputForm(FlaskForm):
    moviename = StringField('Movie Name', validators=[DataRequired()])
    moviereview = TextAreaField('Movie Review', validators=[DataRequired()])
    submit = SubmitField('Submit')
