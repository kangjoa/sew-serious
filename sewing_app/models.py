from sqlalchemy_utils import URLType

from sewing_app.extensions import db
from sewing_app.utils import FormEnum

# Create a many-to-many relationship between fabrics and patterns
fabrics_patterns = db.Table('fabrics_patterns',
                            db.Column('fabric_id', db.Integer,
                                      db.ForeignKey('fabric.id')),
                            db.Column('pattern_id', db.Integer,
                                      db.ForeignKey('pattern.id'))
                            )


class PatternCategory(FormEnum):
    """Categories of sewing patterns."""
    PANTS = 'Pants'
    SHIRT = 'Shirt'
    ACCESSORY = 'Accessory'
    JACKET = 'Jacket'
    OTHER = 'Other'


class Fabric(db.Model):
    """Fabric model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    photo_url = db.Column(URLType)
    patterns = db.relationship(
        'Pattern', secondary=fabrics_patterns, back_populates='fabrics')


class Pattern(db.Model):
    """Pattern model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.Enum(PatternCategory),
                         default=PatternCategory.OTHER)
    photo_url = db.Column(URLType)
    # fabric_id = db.Column(
    #     db.Integer, db.ForeignKey('fabric.id'), nullable=False)
    fabrics = db.relationship(
        'Fabric', secondary=fabrics_patterns, back_populates='patterns')
