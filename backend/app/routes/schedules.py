from datetime import datetime, time

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Professional, Schedule, TimeOff, User, UserRole

schedule_bp = Blueprint("scheduling", __name__)


def current_user():
    return User.query.get_or_404(get_jwt_identity())


def check_owner_or_admin(user: User, business_id: int):
    if user.role == UserRole.ADMIN:
        return
    if user.role == UserRole.OWNER and user.business_id == business_id:
        return
    abort(403, description="Solo propietarios o administradores")


def parse_time(value: str) -> time:
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        abort(400, description="Formato de hora inválido, use HH:MM")


@schedule_bp.get("/professionals/<int:professional_id>/schedules")
@jwt_required()
def list_schedules(professional_id):
    user = current_user()
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, professional.business_id)
    schedules = Schedule.query.filter_by(professional_id=professional_id).all()
    return jsonify([s.to_dict() for s in schedules])


@schedule_bp.post("/professionals/<int:professional_id>/schedules")
@jwt_required()
def create_schedule(professional_id):
    user = current_user()
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, professional.business_id)
    data = request.get_json() or {}
    schedule = Schedule(
        professional_id=professional_id,
        weekday=data.get("weekday"),
        start_time=parse_time(data.get("start_time", "09:00")),
        end_time=parse_time(data.get("end_time", "17:00")),
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify(schedule.to_dict()), 201


@schedule_bp.put("/schedules/<int:schedule_id>")
@jwt_required()
def update_schedule(schedule_id):
    user = current_user()
    schedule = Schedule.query.get_or_404(schedule_id)
    professional = Professional.query.get_or_404(schedule.professional_id)
    check_owner_or_admin(user, professional.business_id)
    data = request.get_json() or {}
    if "weekday" in data:
        schedule.weekday = data["weekday"]
    if "start_time" in data:
        schedule.start_time = parse_time(data["start_time"])
    if "end_time" in data:
        schedule.end_time = parse_time(data["end_time"])
    db.session.commit()
    return jsonify(schedule.to_dict())


@schedule_bp.delete("/schedules/<int:schedule_id>")
@jwt_required()
def delete_schedule(schedule_id):
    user = current_user()
    schedule = Schedule.query.get_or_404(schedule_id)
    professional = Professional.query.get_or_404(schedule.professional_id)
    check_owner_or_admin(user, professional.business_id)
    db.session.delete(schedule)
    db.session.commit()
    return "", 204


@schedule_bp.get("/professionals/<int:professional_id>/time-off")
@jwt_required()
def list_time_off(professional_id):
    user = current_user()
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, professional.business_id)
    blocks = TimeOff.query.filter_by(professional_id=professional_id).all()
    return jsonify([b.to_dict() for b in blocks])


@schedule_bp.post("/professionals/<int:professional_id>/time-off")
@jwt_required()
def create_time_off(professional_id):
    user = current_user()
    professional = Professional.query.get_or_404(professional_id)
    check_owner_or_admin(user, professional.business_id)
    data = request.get_json() or {}
    start = datetime.fromisoformat(data.get("start_datetime"))
    end = datetime.fromisoformat(data.get("end_datetime"))
    block = TimeOff(
        professional_id=professional_id,
        start_datetime=start,
        end_datetime=end,
        reason=data.get("reason"),
    )
    db.session.add(block)
    db.session.commit()
    return jsonify(block.to_dict()), 201


@schedule_bp.delete("/time-off/<int:block_id>")
@jwt_required()
def delete_time_off(block_id):
    user = current_user()
    block = TimeOff.query.get_or_404(block_id)
    professional = Professional.query.get_or_404(block.professional_id)
    check_owner_or_admin(user, professional.business_id)
    db.session.delete(block)
    db.session.commit()
    return "", 204
