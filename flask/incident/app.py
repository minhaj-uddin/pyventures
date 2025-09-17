from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from store import IncidentStore
from auth import auth_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register blueprint for auth
app.register_blueprint(auth_bp)

store = IncidentStore()


@app.route("/incidents", methods=["GET"])
@jwt_required()
def get_all_incidents():
    status = request.args.get("status")
    severity = request.args.get("severity")
    return jsonify(store.list_all(status, severity)), 200


@app.route("/incidents/<int:incident_id>", methods=["GET"])
@jwt_required()
def get_incident(incident_id):
    incident = store.get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident), 200


@app.route("/incidents", methods=["POST"])
@jwt_required()
def create_incident():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    incident = store.create(data)
    return jsonify(incident), 201


@app.route("/incidents/<int:incident_id>/status", methods=["PUT"])
@jwt_required()
def update_status(incident_id):
    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "Status is required"}), 400
    incident = store.update_status(incident_id, data["status"])
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident), 200


@app.route("/incidents/<int:incident_id>/assign", methods=["PUT"])
@jwt_required()
def assign_responder(incident_id):
    data = request.get_json()
    if not data or "responder" not in data:
        return jsonify({"error": "Responder is required"}), 400
    incident = store.assign_responder(incident_id, data["responder"])
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident), 200


@app.route("/incidents/<int:incident_id>/timeline", methods=["POST"])
@jwt_required()
def add_timeline(incident_id):
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    event = store.add_timeline_event(incident_id, data["message"])
    if not event:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(event), 201


@app.route("/incidents/<int:incident_id>", methods=["DELETE"])
@jwt_required()
def delete_incident(incident_id):
    incident = store.delete(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify({"message": "Incident deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
