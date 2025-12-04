from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from ..models import Appointment, AppointmentStatus, Service, User, UserRole

stats_bp = Blueprint("stats", __name__)


def current_user():
    return User.query.get_or_404(get_jwt_identity())


@stats_bp.get("")
@jwt_required()
def overview():
    user = current_user()
    start = request.args.get("start")
    end = request.args.get("end")
    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None

    query = Appointment.query
    if user.role == UserRole.OWNER:
        query = query.filter_by(business_id=user.business_id)
    if start_dt:
        query = query.filter(Appointment.start_datetime >= start_dt)
    if end_dt:
        query = query.filter(Appointment.start_datetime <= end_dt)

    total = query.count()
    cancelled = query.filter_by(status=AppointmentStatus.CANCELLED).count()
    no_show = query.filter_by(status=AppointmentStatus.NO_SHOW).count()

    top_services = (
        query.join(Service)
        .with_entities(Service.name, func.count(Appointment.id))
        .group_by(Service.name)
        .order_by(func.count(Appointment.id).desc())
        .limit(5)
        .all()
    )

    return jsonify(
        {
            "total": total,
            "cancelled": cancelled,
            "no_show": no_show,
            "top_services": [{"name": name, "count": count} for name, count in top_services],
        }
    )
