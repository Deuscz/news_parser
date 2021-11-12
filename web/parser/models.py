from parser.config import db
import datetime


class Source(db.Model):
    """Model that stores urls to resources"""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    category = db.Column(db.String)
    name = db.Column(db.String)


class Article(db.Model):
    """Model that stores articles information"""

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey("source.id"))
    source = db.relationship('Source', backref=db.backref('artcle_current', uselist=False))
    category = db.Column(db.String)
    title = db.Column(db.String, unique=True)
    published_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def as_dict(self):
        return {
            "id": self.id,
            "url_id": self.url_id,
            "category": self.category,
            "title": self.title,
            "published_date": self.published_date.strftime("%Y-%m-%d"),
        }
