from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    booking_number = StringField('Booking nummer', validators=[DataRequired()])
    last_name = StringField('Efternavn', validators=[DataRequired()])
    submit = SubmitField('Log ind')
    
    def validate_booking_number(self, booking_number):
        # Booking nummer valideres ikke her, da det sker i routes.py
        # sammen med efternavn mod booking-databasen
        pass

class AdminLoginForm(FlaskForm):
    username = StringField('Brugernavn', validators=[DataRequired()])
    password = PasswordField('Adgangskode', validators=[DataRequired()])
    submit = SubmitField('Log ind')
