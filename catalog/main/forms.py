from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class CategoryForm(Form):
    category_name = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

class ItemForm(Form):
    name = StringField("Item Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    category = SelectField("Category Name")
    submit = SubmitField('Submit')
