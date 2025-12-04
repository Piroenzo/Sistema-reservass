from datetime import timedelta

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

from ..extensions import db
from ..models import User, UserRole

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    required_fields = ["name", "email", "password", "role"]
    if not all(field in data for field in required_fields):
        abort(400, description="Faltan campos obligatorios")

    if data["role"] not in [role.value for role in UserRole]:
        abort(400, description="Rol inválido")

    if User.query.filter_by(email=data["email"]).first():
        abort(400, description="Email ya registrado")

    user = User(name=data["name"], email=data["email"], role=UserRole(data["role"]))
    user.set_password(data["password"])
    user.business_id = data.get("business_id")
    db.session.add(user)
    db.session.commit()

    return jsonify({"user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        abort(401, description="Credenciales inválidas")

    additional_claims = {"role": user.role.value, "business_id": user.business_id}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "user": user.to_dict()})


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    additional_claims = {"role": user.role.value, "business_id": user.business_id}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify({"access_token": access_token})


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
