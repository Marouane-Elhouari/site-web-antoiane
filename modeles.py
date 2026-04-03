from flask_login import UserMixin
from extensions import db
 
 
class User(UserMixin, db.Model):
    """Matches existing `user` table in antoine_data MySQL database."""
    __tablename__ = 'user'
 
    id            = db.Column(db.Integer,     primary_key=True)
    fname         = db.Column(db.String(50),  nullable=False)
    lname         = db.Column(db.String(50),  nullable=False)
    username      = db.Column(db.String(30),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created  = db.Column(db.DateTime,    server_default=db.func.current_timestamp())
 
    def __repr__(self):
        return f'<User {self.username}>'
 
 
class Liquid(db.Model):
    """Matches existing `liquids` table in antoine_data MySQL database."""
    __tablename__ = 'liquids'
 
    id               = db.Column(db.Integer,     primary_key=True)
    name             = db.Column(db.String(100), nullable=False)
    chemical_formula = db.Column(db.String(50))
    cas_number       = db.Column(db.String(20))
    molecular_weight = db.Column(db.Float)
    boiling_point    = db.Column(db.Float)
    antoine_a        = db.Column(db.Float)
    antoine_b        = db.Column(db.Float)
    antoine_c        = db.Column(db.Float)
    temperature_min  = db.Column(db.Float)
    temperature_max  = db.Column(db.Float)
    description      = db.Column(db.Text)
 
    def __repr__(self):
        return f'<Liquid {self.name}>'