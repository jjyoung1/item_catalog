from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, \
    HiddenField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    category_name = StringField("Category Name", validators=[DataRequired()])
    next = HiddenField('next')
    submit = SubmitField('Submit')


class ItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    category = SelectField("Category Name", coerce=int)
    next = HiddenField('next')
    submit = SubmitField('Submit')
