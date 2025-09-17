from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

article_tags = db.Table('article_tags',
                        db.Column('article_id', db.Integer,
                                  db.ForeignKey('article.id')),
                        db.Column('tag_id', db.Integer,
                                  db.ForeignKey('tag.id'))
                        )


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='article', lazy=True)
    tags = db.relationship('Tag', secondary=article_tags, backref='articles')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey(
        'article.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
