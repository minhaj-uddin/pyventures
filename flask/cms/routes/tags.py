from flask import Blueprint, request, jsonify
from models import db, Tag

bp = Blueprint('tags', __name__)


@bp.route('/', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in tags])


@bp.route('/', methods=['POST'])
def create_tag():
    data = request.json
    comment = Tag(name=data['name'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id}), 201
