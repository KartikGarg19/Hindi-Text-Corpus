from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length

class MovieInputForm(FlaskForm):
    moviename = TextField('Movie Name', validators=[DataRequired()])
    moviereview = TextAreaField('Movie Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    moviename = TextField('Movie Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
