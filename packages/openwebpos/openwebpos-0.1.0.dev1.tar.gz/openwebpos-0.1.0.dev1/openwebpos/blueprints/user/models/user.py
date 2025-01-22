from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from openwebpos.extensions import db
from openwebpos.utils.helpers import CRUDMixin, generate_uuid


class User(UserMixin, CRUDMixin, db.Model):

    def __init__(self, username, email, password, **kwargs):
        super(User, self).__init__(**kwargs)

        self.username = username
        self.email = email
        self.public_id = generate_uuid()

        self.set_password(password)

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    hourly_rate = db.Column(db.Integer, nullable=False, default=0)

    # Authentication
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmation_token = db.Column(db.String(128), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    role = db.relationship("Role", back_populates="users")

    @classmethod
    def get_by_identity(cls, identity: str):
        """Get a user by username or email."""
        return cls.query.filter((cls.username == identity) | (cls.email == identity))

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(
            password, salt_length=32, method="pbkdf2:sha256:80000"
        )

    def check_password(self, password):
        """Check if the user's password is correct."""
        return check_password_hash(self.password_hash, password)

    def in_role(self, role_name):
        """Check if the user is in the given role."""
        return self.role.name == role_name.lower()
