from flask_login import UserMixin
from extensions import db
from datetime import datetime
 
 
class User(UserMixin, db.Model):
    """Matches existing `user` table in antoine_data MySQL database."""
    __tablename__ = 'user'
 
    id            = db.Column(db.Integer,     primary_key=True)
    fname         = db.Column(db.String(50),  nullable=False)
    lname         = db.Column(db.String(50),  nullable=False)
    username      = db.Column(db.String(30),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified   = db.Column(db.Boolean,     default=False)
    verification_code = db.Column(db.String(6))
    reset_code    = db.Column(db.String(6))    # For password reset
    reset_expiration = db.Column(db.DateTime)  # Reset code expiration
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


class UserLog(db.Model):
    """User activity logging table for security auditing"""
    __tablename__ = 'user_log'
    
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # nullable for failed attempts
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 compatible
    mac_address = db.Column(db.String(17), nullable=True)  # MAC address format: XX:XX:XX:XX:XX:XX
    action     = db.Column(db.String(100), nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref='logs')
    
    def __repr__(self):
        return f'<UserLog {self.action} by {self.user_id if self.user_id else "Unknown"}>'