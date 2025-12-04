from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Appointment, AppointmentStatus, Professional, Service, User, UserRole
from ..utils import create_appointment

appointment_bp = Blueprint("appointments", __name__)


def current_user():
    return User.query.get_or_404(get_jwt_identity())


def check_owner_or_admin(user: User, business_id: int):
    if user.role == UserRole.ADMIN:
        return
    if user.role == UserRole.OWNER and user.business_id == business_id:
        return
    abort(403, description="Solo propietarios o administradores")


@appointment_bp.get("")
@jwt_required()
def list_appointments():
    user = current_user()
    query = Appointment.query
    if user.role == UserRole.CLIENT:
        query = query.filter_by(client_id=user.id)
    elif user.role == UserRole.OWNER:
        query = query.filter_by(business_id=user.business_id)
    appointments = query.order_by(Appointment.start_datetime.desc()).all()
    return jsonify([a.to_dict() for a in appointments])


@appointment_bp.post("")
@jwt_required()
def create():
    user = current_user()
    data = request.get_json() or {}

    service = Service.query.get_or_404(data.get("service_id"))
    professional = Professional.query.get_or_404(data.get("professional_id"))
    business_id = service.business_id
    if business_id != professional.business_id:
        abort(400, description="Servicio y profesional deben coincidir en negocio")

    client_id = data.get("client_id") or user.id
    if user.role == UserRole.CLIENT and client_id != user.id:
        abort(403)

    start_dt = datetime.fromisoformat(data.get("start_datetime"))
    appointment = create_appointment(
        business_id=business_id,
        professional_id=professional.id,
        service_id=service.id,
        client_id=client_id,
        start_dt=start_dt,
        duration_minutes=service.duration_minutes,
        notes=data.get("notes"),
    )
    return jsonify(appointment.to_dict()), 201


@appointment_bp.put("/<int:appointment_id>")
@jwt_required()
def update(appointment_id):
    user = current_user()
    appointment = Appointment.query.get_or_404(appointment_id)
    if user.role == UserRole.CLIENT and appointment.client_id != user.id:
        abort(403)
    if user.role == UserRole.OWNER:
        check_owner_or_admin(user, appointment.business_id)

    data = request.get_json() or {}
    if "status" in data and data["status"] in [status.value for status in AppointmentStatus]:
        appointment.status = AppointmentStatus(data["status"])
    if "notes" in data:
        appointment.notes = data["notes"]
    db.session.commit()
    return jsonify(appointment.to_dict())


@appointment_bp.delete("/<int:appointment_id>")
@jwt_required()
def cancel(appointment_id):
    user = current_user()
    appointment = Appointment.query.get_or_404(appointment_id)
    if user.role == UserRole.CLIENT and appointment.client_id != user.id:
        abort(403)
    if user.role == UserRole.OWNER:
        check_owner_or_admin(user, appointment.business_id)

    appointment.status = AppointmentStatus.CANCELLED
    db.session.commit()
    return jsonify(appointment.to_dict())


@appointment_bp.post("/availability")
@jwt_required()
def availability():
    data = request.get_json() or {}
    professional = Professional.query.get_or_404(data.get("professional_id"))
    service = Service.query.get_or_404(data.get("service_id"))
    date = datetime.fromisoformat(data.get("date")).date()

    schedule = (
        professional.schedules and [s for s in professional.schedules if s.weekday == date.weekday()]
    )
    if not schedule:
        return jsonify([])
    schedule = schedule[0]

    start_dt = datetime.combine(date, schedule.start_time)
    end_dt = datetime.combine(date, schedule.end_time)
    delta = timedelta(minutes=service.duration_minutes)

    appointments = Appointment.query.filter(
        Appointment.professional_id == professional.id,
        Appointment.start_datetime >= start_dt,
        Appointment.start_datetime < end_dt,
        Appointment.status != AppointmentStatus.CANCELLED,
    ).all()

    blocks = {(a.start_datetime, a.end_datetime) for a in appointments}

    available = []
    cursor = start_dt
    while cursor + delta <= end_dt:
        slot_end = cursor + delta
        if all(not (start <= cursor < end or start < slot_end <= end) for start, end in blocks):
            available.append({"start": cursor.isoformat(), "end": slot_end.isoformat()})
        cursor += delta

    return jsonify(available)
