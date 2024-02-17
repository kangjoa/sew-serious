from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL
from sewing_app.models import ItemCategory, GroceryStore, GroceryItem


class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField('Grocery Store Title', validators=[DataRequired(),
                                                           Length(min=2, max=80,
                                                                  message="Your title needs to be between 2 and 80 chars")])
    address = StringField('Grocery Store Address', validators=[DataRequired(), Length(
        min=5, max=100, message="Your address needs to be between 5 and 100 chars")])
    submit = SubmitField('Submit')


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    name = StringField('Grocery Item name', validators=[DataRequired(), Length(
        min=2, max=100, message="Your message needs to be between 2 and 100 characters")])
    price = FloatField('Grocery Item price', validators=[
        DataRequired(message="Price is required (no letters)")
    ])
    category = SelectField('Grocery Item category',
                           choices=ItemCategory.choices())
    photo_url = StringField('Grocery Item photo url', validators=[DataRequired(), Length(
        min=5, max=1000, message="Your message needs to be between 5 and 1000 characters")])

    def grocery_store_query():
        """Retrieve all grocery stores from the database."""
        return GroceryStore.query.all()

    # Assign the grocery_store_query function to the query_factory param of the QuerySelectField
    store = QuerySelectField('Grocery Item store',
                             query_factory=grocery_store_query, get_label='title')
    submit = SubmitField('Submit')

    # Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button

    # Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button
