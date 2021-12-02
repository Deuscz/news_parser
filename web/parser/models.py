import datetime
from parser.config import db
from typing import Dict


class Source(db.Model):
    """Model with resources urls."""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    source_link = db.Column(db.String, nullable=False)


class Article(db.Model):
    """Model with article information."""

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey("source.id"))
    source = db.relationship(
        "Source", backref=db.backref("artcle_current", uselist=False)
    )
    category = db.Column(db.String, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    created_date = db.Column(
        db.DateTime, default=datetime.datetime.now(), nullable=False
    )

    def as_dict(self) -> Dict:
        return {
            "id": self.id,
            "url_id": self.url_id,
            "category": self.category,
            "title": self.title,
            "published_date": self.published_date.strftime("%Y-%m-%d"),
        }
