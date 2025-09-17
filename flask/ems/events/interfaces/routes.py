from flask import Blueprint, request, jsonify
from infrastructure.repository import InMemoryEventRepository
from infrastructure.redis_pubsub import RedisPublisher
from application.services import RegisterUser
from domain.exceptions import EventFull, UserAlreadyRegistered

bp = Blueprint("routes", __name__)

publisher = RedisPublisher()
event_repo = InMemoryEventRepository()
register_use_case = RegisterUser(event_repo, publisher)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        register_use_case.execute(data["user_id"], data["event_id"])
        return jsonify({"message": "User registered successfully"}), 200
    except (EventFull, UserAlreadyRegistered) as e:
        return jsonify({"error": str(e)}), 400
