from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class CategoryForm(FlaskForm):
    category_name = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

class ItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    category = SelectField("Category Name", coerce=int)
    submit = SubmitField('Submit')
