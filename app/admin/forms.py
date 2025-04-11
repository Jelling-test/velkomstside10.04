from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, BooleanField, FloatField, TimeField, DateTimeField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime, time

class AdminLoginForm(FlaskForm):
    username = StringField('Brugernavn', validators=[DataRequired()])
    password = PasswordField('Adgangskode', validators=[DataRequired()])
    submit = SubmitField('Log ind')

class MenuItemForm(FlaskForm):
    name_da = StringField('Navn (Dansk)', validators=[DataRequired()])
    name_en = StringField('Navn (Engelsk)', validators=[DataRequired()])
    name_de = StringField('Navn (Tysk)', validators=[DataRequired()])
    name_nl = StringField('Navn (Hollandsk)', validators=[DataRequired()])
    
    description_da = TextAreaField('Beskrivelse (Dansk)', validators=[DataRequired()])
    description_en = TextAreaField('Beskrivelse (Engelsk)', validators=[DataRequired()])
    description_de = TextAreaField('Beskrivelse (Tysk)', validators=[DataRequired()])
    description_nl = TextAreaField('Beskrivelse (Hollandsk)', validators=[DataRequired()])
    
    price = FloatField('Pris', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Billede', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Kun billeder tilladt')])
    is_active = BooleanField('Aktiv', default=True)
    
    submit = SubmitField('Gem')

class BakeryItemForm(FlaskForm):
    name_da = StringField('Navn (Dansk)', validators=[DataRequired()])
    name_en = StringField('Navn (Engelsk)', validators=[DataRequired()])
    name_de = StringField('Navn (Tysk)', validators=[DataRequired()])
    name_nl = StringField('Navn (Hollandsk)', validators=[DataRequired()])
    
    allergene_da = StringField('Allergener (Dansk)', validators=[Optional()])
    allergene_en = StringField('Allergener (Engelsk)', validators=[Optional()])
    allergene_de = StringField('Allergener (Tysk)', validators=[Optional()])
    allergene_nl = StringField('Allergener (Hollandsk)', validators=[Optional()])
    
    price = FloatField('Pris', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Billede', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Kun billeder tilladt')])
    is_active = BooleanField('Aktiv', default=True)
    
    submit = SubmitField('Gem')

class OpeningHoursForm(FlaskForm):
    monday_is_closed = BooleanField('Lukket')
    monday_open_time = TimeField('Åbningstid', default=time(10, 0))
    monday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    tuesday_is_closed = BooleanField('Lukket')
    tuesday_open_time = TimeField('Åbningstid', default=time(10, 0))
    tuesday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    wednesday_is_closed = BooleanField('Lukket')
    wednesday_open_time = TimeField('Åbningstid', default=time(10, 0))
    wednesday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    thursday_is_closed = BooleanField('Lukket')
    thursday_open_time = TimeField('Åbningstid', default=time(10, 0))
    thursday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    friday_is_closed = BooleanField('Lukket')
    friday_open_time = TimeField('Åbningstid', default=time(10, 0))
    friday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    saturday_is_closed = BooleanField('Lukket')
    saturday_open_time = TimeField('Åbningstid', default=time(10, 0))
    saturday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    sunday_is_closed = BooleanField('Lukket')
    sunday_open_time = TimeField('Åbningstid', default=time(10, 0))
    sunday_close_time = TimeField('Lukketid', default=time(21, 0))
    
    submit = SubmitField('Gem')

class EventForm(FlaskForm):
    title_da = StringField('Titel (Dansk)', validators=[DataRequired()])
    title_en = StringField('Titel (Engelsk)', validators=[DataRequired()])
    title_de = StringField('Titel (Tysk)', validators=[DataRequired()])
    title_nl = StringField('Titel (Hollandsk)', validators=[DataRequired()])
    title_fi = StringField('Titel (Finsk)', validators=[Optional()])
    title_no = StringField('Titel (Norsk)', validators=[Optional()])
    title_sv = StringField('Titel (Svensk)', validators=[Optional()])
    
    description_da = TextAreaField('Beskrivelse (Dansk)', validators=[DataRequired()])
    description_en = TextAreaField('Beskrivelse (Engelsk)', validators=[DataRequired()])
    description_de = TextAreaField('Beskrivelse (Tysk)', validators=[DataRequired()])
    description_nl = TextAreaField('Beskrivelse (Hollandsk)', validators=[DataRequired()])
    description_fi = TextAreaField('Beskrivelse (Finsk)', validators=[Optional()])
    description_no = TextAreaField('Beskrivelse (Norsk)', validators=[Optional()])
    description_sv = TextAreaField('Beskrivelse (Svensk)', validators=[Optional()])
    
    start_date = DateTimeField('Startdato og -tid', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_date = DateTimeField('Slutdato og -tid', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    location = StringField('Sted', validators=[DataRequired()])
    image = FileField('Billede', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Kun billeder tilladt')])
    is_active = BooleanField('Aktiv', default=True)
    
    submit = SubmitField('Gem')

class PromotionForm(FlaskForm):
    title_da = StringField('Titel (Dansk)', validators=[DataRequired()])
    title_en = StringField('Titel (Engelsk)', validators=[DataRequired()])
    title_de = StringField('Titel (Tysk)', validators=[DataRequired()])
    title_nl = StringField('Titel (Hollandsk)', validators=[DataRequired()])
    title_fi = StringField('Titel (Finsk)', validators=[Optional()])
    title_no = StringField('Titel (Norsk)', validators=[Optional()])
    title_sv = StringField('Titel (Svensk)', validators=[Optional()])
    
    description_da = TextAreaField('Beskrivelse (Dansk)', validators=[DataRequired()])
    description_en = TextAreaField('Beskrivelse (Engelsk)', validators=[DataRequired()])
    description_de = TextAreaField('Beskrivelse (Tysk)', validators=[DataRequired()])
    description_nl = TextAreaField('Beskrivelse (Hollandsk)', validators=[DataRequired()])
    description_fi = TextAreaField('Beskrivelse (Finsk)', validators=[Optional()])
    description_no = TextAreaField('Beskrivelse (Norsk)', validators=[Optional()])
    description_sv = TextAreaField('Beskrivelse (Svensk)', validators=[Optional()])
    
    price = FloatField('Tilbudspris', validators=[DataRequired(), NumberRange(min=0)])
    original_price = FloatField('Normalpris', validators=[DataRequired(), NumberRange(min=0)])
    start_date = DateTimeField('Startdato og -tid', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_date = DateTimeField('Slutdato og -tid', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    image = FileField('Billede', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Kun billeder tilladt')])
    is_active = BooleanField('Aktiv', default=True)
    
    submit = SubmitField('Gem')

class PoolHoursForm(FlaskForm):
    name_da = StringField('Navn (Dansk)', validators=[DataRequired()])
    name_en = StringField('Navn (Engelsk)', validators=[DataRequired()])
    name_de = StringField('Navn (Tysk)', validators=[DataRequired()])
    name_nl = StringField('Navn (Hollandsk)', validators=[DataRequired()])
    
    description_da = TextAreaField('Beskrivelse (Dansk)', validators=[Optional()])
    description_en = TextAreaField('Beskrivelse (Engelsk)', validators=[Optional()])
    description_de = TextAreaField('Beskrivelse (Tysk)', validators=[Optional()])
    description_nl = TextAreaField('Beskrivelse (Hollandsk)', validators=[Optional()])
    
    start_date = DateField('Startdato', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Slutdato', format='%Y-%m-%d', validators=[DataRequired()])
    
    weekday_open_time = TimeField('Åbningstid (hverdage)', validators=[Optional()])
    weekday_close_time = TimeField('Lukketid (hverdage)', validators=[Optional()])
    weekend_open_time = TimeField('Åbningstid (weekend)', validators=[Optional()])
    weekend_close_time = TimeField('Lukketid (weekend)', validators=[Optional()])
    
    special_note_da = TextAreaField('Særlig bemærkning (Dansk)', validators=[Optional()])
    special_note_en = TextAreaField('Særlig bemærkning (Engelsk)', validators=[Optional()])
    special_note_de = TextAreaField('Særlig bemærkning (Tysk)', validators=[Optional()])
    special_note_nl = TextAreaField('Særlig bemærkning (Hollandsk)', validators=[Optional()])
    
    order_index = IntegerField('Rækkefølge', default=0, validators=[NumberRange(min=0)])
    is_active = BooleanField('Aktiv', default=True)
    
    submit = SubmitField('Gem')
