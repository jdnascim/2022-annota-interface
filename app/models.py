from datetime import datetime
from config import db, ma


class Image(db.Model):
    __tablename__ = "image"
    imagepath = db.Column(db.String(255), primary_key=True)
    related = db.Column(db.Boolean, nullable=False)
    annotated = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
        nullable=False
    )
    

class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Image
        sqla_session = db.session
        load_instance = True