from datetime import datetime, timedelta
from typing import List

from flask import abort

from .models import Appointment, AppointmentStatus, Schedule, TimeOff
from .extensions import db


ROLE_LEVELS = {
    "admin": 3,
    "owner": 2,
    "staff": 1,
    "client": 0,
}


def require_role(user, allowed_roles):
    if user.role.value not in allowed_roles:
        abort(403, description="No autorizado para esta acción")


def overlaps(start_a, end_a, start_b, end_b):
    return max(start_a, start_b) < min(end_a, end_b)


def is_within_schedule(schedule: Schedule, start_dt: datetime, end_dt: datetime) -> bool:
    weekday = start_dt.weekday()
    if schedule.weekday != weekday:
        return False
    return schedule.start_time <= start_dt.time() and end_dt.time() <= schedule.end_time


def validate_appointment_window(schedule: Schedule, time_off: List[TimeOff], appointments: List[Appointment], start_dt: datetime, end_dt: datetime):
    if not is_within_schedule(schedule, start_dt, end_dt):
        abort(400, description="Fuera de horario disponible")

    for block in time_off:
        if overlaps(start_dt, end_dt, block.start_datetime, block.end_datetime):
            abort(400, description="Profesional no disponible por bloqueo")

    for appt in appointments:
        if appt.status != AppointmentStatus.CANCELLED and overlaps(start_dt, end_dt, appt.start_datetime, appt.end_datetime):
            abort(400, description="Conflicto con otro turno")


def create_appointment(business_id: int, professional_id: int, service_id: int, client_id: int, start_dt: datetime, duration_minutes: int, notes: str | None = None):
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    schedule = (
        Schedule.query.filter_by(professional_id=professional_id, weekday=start_dt.weekday())
        .order_by(Schedule.start_time)
        .first()
    )
    if not schedule:
        abort(400, description="No hay horario configurado para el profesional")

    time_off = TimeOff.query.filter(
        TimeOff.professional_id == professional_id,
        TimeOff.start_datetime <= end_dt,
        TimeOff.end_datetime >= start_dt,
    ).all()

    appointments = Appointment.query.filter(
        Appointment.professional_id == professional_id,
        Appointment.start_datetime < end_dt,
        Appointment.end_datetime > start_dt,
    ).all()

    validate_appointment_window(schedule, time_off, appointments, start_dt, end_dt)

    appointment = Appointment(
        business_id=business_id,
        professional_id=professional_id,
        service_id=service_id,
        client_id=client_id,
        start_datetime=start_dt,
        end_datetime=end_dt,
        status=AppointmentStatus.SCHEDULED,
        notes=notes,
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment
