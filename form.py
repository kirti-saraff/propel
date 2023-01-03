from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class AddressForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name=StringField('last_name',validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired()])
    submit=SubmitField('Add address')

class SearchForm(FlaskForm):
    first_name = StringField('first_name', validators = [DataRequired()])
    submit=SubmitField('Search')

