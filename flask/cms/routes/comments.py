from flask import Blueprint, request, jsonify
from models import db, Comment

bp = Blueprint('comments', __name__)


@bp.route('/', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([{"id": c.id, "content": c.content} for c in comments])


@bp.route('/', methods=['POST'])
def create_comment():
    data = request.json
    comment = Comment(article_id=data['article_id'], content=data['content'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id}), 201
