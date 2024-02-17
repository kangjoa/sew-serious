from sqlalchemy_utils import URLType

from sewing_app.extensions import db
from sewing_app.utils import FormEnum


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
    patterns = db.relationship('Pattern', back_populates='fabric')


class Pattern(db.Model):
    """Pattern model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.Enum(PatternCategory),
                         default=PatternCategory.OTHER)
    fabric_id = db.Column(
        db.Integer, db.ForeignKey('fabric.id'), nullable=False)
    fabric = db.relationship('Fabric', back_populates='patterns')
