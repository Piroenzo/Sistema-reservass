from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Professional, Service, User, UserRole

service_bp = Blueprint("services", __name__)


def current_user():
    user_id = get_jwt_identity()
    return User.query.get_or_404(user_id)


def check_owner_or_admin(user: User, business_id: int):
    if user.role == UserRole.ADMIN:
        return
    if user.role == UserRole.OWNER and user.business_id == business_id:
        return
    abort(403, description="Solo propietarios o administradores")


@service_bp.get("/businesses/<int:business_id>/services")
@jwt_required()
def list_services(business_id):
    user = current_user()
    check_owner_or_admin(user, business_id)
    services = Service.query.filter_by(business_id=business_id).all()
    return jsonify([s.to_dict() for s in services])


@service_bp.post("/businesses/<int:business_id>/services")
@jwt_required()
def create_service(business_id):
    user = current_user()
    check_owner_or_admin(user, business_id)
    data = request.get_json() or {}
    service = Service(
        name=data.get("name"),
        duration_minutes=data.get("duration_minutes", 30),
        price=data.get("price", 0),
        business_id=business_id,
    )
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201


@service_bp.put("/services/<int:service_id>")
@jwt_required()
def update_service(service_id):
    user = current_user()
    service = Service.query.get_or_404(service_id)
    check_owner_or_admin(user, service.business_id)
    data = request.get_json() or {}
    service.name = data.get("name", service.name)
    service.duration_minutes = data.get("duration_minutes", service.duration_minutes)
    service.price = data.get("price", service.price)
    db.session.commit()
    return jsonify(service.to_dict())


@service_bp.delete("/services/<int:service_id>")
@jwt_required()
def delete_service(service_id):
    user = current_user()
    service = Service.query.get_or_404(service_id)
    check_owner_or_admin(user, service.business_id)
    db.session.delete(service)
    db.session.commit()
    return "", 204


@service_bp.get("/businesses/<int:business_id>/professionals")
@jwt_required()
def list_professionals(business_id):
    user = current_user()
    check_owner_or_admin(user, business_id)
    professionals = Professional.query.filter_by(business_id=business_id).all()
    return jsonify([p.to_dict() for p in professionals])


@service_bp.post("/businesses/<int:business_id>/professionals")
@jwt_required()
def create_professional(business_id):
    user = current_user()
    check_owner_or_admin(user, business_id)
    data = request.get_json() or {}
    professional = Professional(name=data.get("name"), business_id=business_id)
    db.session.add(professional)
    db.session.commit()
    return jsonify(professional.to_dict()), 201


@service_bp.put("/professionals/<int:professional_id>")
@jwt_required()
def update_professional(professional_id):
    user = current_user()
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, professional.business_id)
    data = request.get_json() or {}
    professional.name = data.get("name", professional.name)
    db.session.commit()
    return jsonify(professional.to_dict())


@service_bp.delete("/professionals/<int:professional_id>")
@jwt_required()
def delete_professional(professional_id):
    user = current_user()
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, professional.business_id)
    db.session.delete(professional)
    db.session.commit()
    return "", 204


@service_bp.post("/services/<int:service_id>/professionals/<int:professional_id>")
@jwt_required()
def assign_service(service_id, professional_id):
    user = current_user()
    service = Service.query.get_or_404(service_id)
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, service.business_id)
    if service.business_id != professional.business_id:
        abort(400, description="Servicio y profesional deben pertenecer al mismo negocio")

    if professional not in service.professionals:
        service.professionals.append(professional)
        db.session.commit()
    return jsonify({"service": service.to_dict(), "professional": professional.to_dict()})
