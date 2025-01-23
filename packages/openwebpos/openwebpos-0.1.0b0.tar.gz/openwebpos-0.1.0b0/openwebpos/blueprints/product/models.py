from openwebpos.extensions import db
from openwebpos.utils.helpers import CRUDMixin


class OrderType(db.Model, CRUDMixin):

    def __init__(self, name, **kwargs):
        super(OrderType, self).__init__(**kwargs)
        self.name = name.lower()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(30), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_visible = db.Column(db.Boolean, default=True)
    show_table_selection = db.Column(db.Boolean, default=False)
    show_pager_selection = db.Column(db.Boolean, default=False)

    @classmethod
    def list_active_and_visible(cls):
        return cls.query.filter_by(is_active=True, is_visible=True).all()
