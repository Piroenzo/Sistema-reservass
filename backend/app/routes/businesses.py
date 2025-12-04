from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Business, User, UserRole
from ..utils import require_role

business_bp = Blueprint("businesses", __name__)


def current_user():
    user_id = get_jwt_identity()
    return User.query.get_or_404(user_id)


@business_bp.get("")
@jwt_required()
def list_businesses():
    user = current_user()
    if user.role not in (UserRole.ADMIN, UserRole.OWNER):
        abort(403)
    businesses = Business.query.all()
    return jsonify([b.to_dict() for b in businesses])


@business_bp.post("")
@jwt_required()
def create_business():
    user = current_user()
    require_role(user, [UserRole.ADMIN.value])
    data = request.get_json() or {}
    business = Business(name=data.get("name"), description=data.get("description"))
    db.session.add(business)
    db.session.commit()
    return jsonify(business.to_dict()), 201


@business_bp.put("/<int:business_id>")
@jwt_required()
def update_business(business_id):
    user = current_user()
    require_role(user, [UserRole.ADMIN.value])
    business = Business.query.get_or_404(business_id)
    data = request.get_json() or {}
    business.name = data.get("name", business.name)
    business.description = data.get("description", business.description)
    db.session.commit()
    return jsonify(business.to_dict())


@business_bp.delete("/<int:business_id>")
@jwt_required()
def delete_business(business_id):
    user = current_user()
    require_role(user, [UserRole.ADMIN.value])
    business = Business.query.get_or_404(business_id)
    db.session.delete(business)
    db.session.commit()
    return "", 204
