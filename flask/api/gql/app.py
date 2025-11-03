from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from gql import schema
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL

from gql.db import db
from gql.blocklist import BLOCKLIST
from gql.models.user import UserModel


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "secret_key"

    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    Limiter(get_remote_address, app=app)

    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = UserModel.query.get(identity)
        if user:
            return {"role": user.role.value}
        return {"role": "user"}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # --------- GraphQL Routes ---------
    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return ExplorerGraphiQL().html(None), 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

    return app
