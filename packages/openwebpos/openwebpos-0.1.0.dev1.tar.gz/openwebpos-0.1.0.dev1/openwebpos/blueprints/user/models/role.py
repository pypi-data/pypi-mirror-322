from openwebpos.extensions import db
from openwebpos.utils.helpers import CRUDMixin, generate_slug


class Role(CRUDMixin, db.Model):

    def __init__(self, name, **kwargs):
        super(Role, self).__init__(**kwargs)

        self.name = name.lower()
        self.slug = generate_slug(name)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_removable = db.Column(db.Boolean, default=True)

    # Relationships
    users = db.relationship("User", back_populates="role")
