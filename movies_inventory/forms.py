from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators= [DataRequired()])
    submit_button = SubmitField()


class MovieSearchForm(FlaskForm):
    search = StringField('search', [DataRequired()])
    submit_search = SubmitField('Search',
                        render_kw={'class': 'btn btn-success btn-block'})
    
class MovieFavoriteForm(FlaskForm):
    title = StringField('Title')
    tmdb_id = StringField('tmdb_id')