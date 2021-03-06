from flask import jsonify
from flask_jwt_extended import JWTManager

from src.account import Account

jwt = JWTManager()


@jwt.user_identity_loader
def loader_identity(user):
    return user.id


@jwt.user_lookup_loader
def user_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return Account.query.filter_by(id=identity).one_or_none()


@jwt.user_lookup_error_loader
def user_error(_jwt_header, _jwt_data):
    return jsonify({
        "message": "Unable load account please contact support or try again"
    }), 401


@jwt.unauthorized_loader
def user_unauthorized(error):
    return jsonify(message=error), 403


@jwt.expired_token_loader
def user_token_expired(_jwt_header, _jwt_data):
    return jsonify(message="token is expired"), 401


