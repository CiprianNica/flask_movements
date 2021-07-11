from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

# creamos nuestro formulario 
# (clase que hereda de FlaskForm)
class MovementsForm(FlaskForm):
    #los campos
    id = IntegerField('id')
    fecha = DateField('fecha', validators=[DataRequired()])
    concepto = StringField('concepto', validators=[DataRequired(), Length(min=10, message='El concepto debe tener min 10')])
    cantidad = FloatField('cantidad', validators=[DataRequired()])

    submit = SubmitField('GO')