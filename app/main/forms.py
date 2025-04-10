from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, BooleanField, FloatField
from wtforms.validators import DataRequired, Email, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed

class BakeryOrderForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Bestil')

class PromotionOrderForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    quantity = IntegerField('Antal', validators=[DataRequired(), NumberRange(min=1)], default=1)
    comment = TextAreaField('Kommentar', validators=[Optional()])
    submit = SubmitField('Bestil')

class EventRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    num_participants = IntegerField('Antal deltagere', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Tilmeld')
