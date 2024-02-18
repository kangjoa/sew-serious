from sqlalchemy_utils import URLType
from flask_login import UserMixin

from sewing_app.extensions import db
from sewing_app.utils import FormEnum

# Create a many-to-many relationship between fabrics and patterns
fabrics_patterns = db.Table('fabrics_patterns',
                            db.Column('fabric_id', db.Integer,
                                      db.ForeignKey('fabric.id')),
                            db.Column('pattern_id', db.Integer,
                                      db.ForeignKey('pattern.id'))
                            )

# Bridge table between users and patterns, users-patterns many-to-many relationship
patterns_list = db.Table('patterns_list',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('user.id')),
                         db.Column('pattern_id', db.Integer,
                                   db.ForeignKey('pattern.id'))
                         )

# Bridge table between users and fabrics, users-fabrics many-to-many relationship
fabrics_list = db.Table('fabrics_list', db.Column('user_id', db.Integer, db.ForeignKey(
    'user.id')), db.Column('fabric_id', db.Integer, db.ForeignKey('fabric.id')))


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
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users = db.relationship('User', secondary=fabrics_list,
                            back_populates='fabrics_list_items')


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
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users = db.relationship('User', secondary=patterns_list,
                            back_populates='patterns_list_items')


class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    patterns_list_items = db.relationship(
        'Pattern', secondary=patterns_list, back_populates='users')
    fabrics_list_items = db.relationship(
        'Fabric', secondary=fabrics_list, back_populates='users')
