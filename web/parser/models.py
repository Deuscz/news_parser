from parser.config import db
import datetime


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    category = db.Column(db.String)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey("source.id"))
    category = db.Column(db.String)
    title = db.Column(db.String)
    published_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    def as_dict(self):
        return {'id': self.id,
                'url_id': self.url_id,
                'category': self.category,
                'title': self.title,
                'published_date': self.published_date.strftime("%Y-%m-%d"),
                }
