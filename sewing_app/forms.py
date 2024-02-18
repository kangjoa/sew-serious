from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL
from sewing_app.models import PatternCategory, Fabric, Pattern


class FabricForm(FlaskForm):
    """Form for adding/updating a Fabric."""

    name = StringField('Fabric Name', validators=[DataRequired(),
                                                  Length(min=2, max=80,
                                                         message="Your name needs to be between 2 and 80 chars")])
    color = StringField('Fabric Color', validators=[DataRequired(),
                                                    Length(min=2, max=80,
                                                           message="Your name needs to be between 2 and 80 chars")])
    quantity = FloatField('Fabric Quantity', validators=[
        DataRequired(message="Quantity is required (no letters)")
    ])
    photo_url = StringField('Fabric photo url', validators=[DataRequired(), Length(
        min=5, max=1000, message="Your message needs to be between 5 and 1000 characters")])
    submit = SubmitField('Submit')


class PatternForm(FlaskForm):
    """Form for adding/updating a Pattern."""

    name = StringField('Pattern Name', validators=[DataRequired(), Length(
        min=2, max=100, message="Your message needs to be between 2 and 100 characters")])

    category = SelectField('Pattern Category',
                           choices=PatternCategory.choices())
    photo_url = StringField('Sewing Pattern photo url', validators=[DataRequired(), Length(
        min=5, max=1000, message="Your message needs to be between 5 and 1000 characters")])

    def fabric_query():
        """Retrieve all fabrics from the database."""
        return Fabric.query.all()

    # Assign the fabric_query function to the query_factory param of the QuerySelectField
    fabric = QuerySelectField('Fabrics for patterns',
                              query_factory=fabric_query, get_label='name')
    submit = SubmitField('Submit')
