from datetime import datetime

from app.extensions import db


class TimestampMixin:
    """Generates timestamps for  created_at / updated_at columns"""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
