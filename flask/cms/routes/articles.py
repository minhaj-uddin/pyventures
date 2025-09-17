from flask import Blueprint, request, jsonify
from models import db, Article

bp = Blueprint('articles', __name__)


@bp.route('/', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([{"id": a.id, "title": a.title} for a in articles])


@bp.route('/', methods=['POST'])
def create_article():
    data = request.json
    article = Article(
        title=data['title'], content=data['content'], category_id=data['category_id'])
    db.session.add(article)
    db.session.commit()
    return jsonify({"id": article.id}), 201
