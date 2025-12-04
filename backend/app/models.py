from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy import CheckConstraint, Enum as PgEnum, Table, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class UserRole(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    STAFF = "staff"
    CLIENT = "client"


service_professional = Table(
    "service_professional",
    db.Model.metadata,
    db.Column("service_id", db.Integer, db.ForeignKey("services.id"), primary_key=True),
    db.Column(
        "professional_id", db.Integer, db.ForeignKey("professionals.id"), primary_key=True
    ),
    UniqueConstraint("service_id", "professional_id"),
)


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(PgEnum(UserRole), nullable=False, default=UserRole.CLIENT)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=True)

    business = db.relationship("Business", back_populates="users")
    appointments = db.relationship("Appointment", back_populates="client")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
            "business_id": self.business_id,
        }


class Business(db.Model, TimestampMixin):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    users = db.relationship("User", back_populates="business")
    professionals = db.relationship("Professional", back_populates="business")
    services = db.relationship("Service", back_populates="business")
    appointments = db.relationship("Appointment", back_populates="business")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Professional(db.Model, TimestampMixin):
    __tablename__ = "professionals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)

    business = db.relationship("Business", back_populates="professionals")
    services = db.relationship("Service", secondary=service_professional, back_populates="professionals")
    schedules = db.relationship("Schedule", back_populates="professional")
    time_off = db.relationship("TimeOff", back_populates="professional")
    appointments = db.relationship("Appointment", back_populates="professional")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "business_id": self.business_id}


class Service(db.Model, TimestampMixin):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)

    business = db.relationship("Business", back_populates="services")
    professionals = db.relationship("Professional", secondary=service_professional, back_populates="services")
    appointments = db.relationship("Appointment", back_populates="service")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration_minutes": self.duration_minutes,
            "price": float(self.price),
            "business_id": self.business_id,
        }


class Schedule(db.Model, TimestampMixin):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professionals.id"), nullable=False)
    weekday = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    professional = db.relationship("Professional", back_populates="schedules")

    __table_args__ = (
        UniqueConstraint("professional_id", "weekday", name="uq_professional_weekday"),
        CheckConstraint("start_time < end_time", name="check_schedule_time"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "professional_id": self.professional_id,
            "weekday": self.weekday,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }


class TimeOff(db.Model, TimestampMixin):
    __tablename__ = "time_off"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professionals.id"), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    professional = db.relationship("Professional", back_populates="time_off")

    __table_args__ = (
        CheckConstraint("start_datetime < end_datetime", name="check_time_off_window"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "professional_id": self.professional_id,
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
            "reason": self.reason,
        }


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Appointment(db.Model, TimestampMixin):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professionals.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(PgEnum(AppointmentStatus), nullable=False, default=AppointmentStatus.SCHEDULED)
    notes = db.Column(db.Text, nullable=True)

    business = db.relationship("Business", back_populates="appointments")
    professional = db.relationship("Professional", back_populates="appointments")
    service = db.relationship("Service", back_populates="appointments")
    client = db.relationship("User", back_populates="appointments")

    __table_args__ = (
        CheckConstraint("start_datetime < end_datetime", name="check_appointment_window"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "business_id": self.business_id,
            "professional_id": self.professional_id,
            "service_id": self.service_id,
            "client_id": self.client_id,
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
            "status": self.status.value,
            "notes": self.notes,
        }



def calculate_slots(schedule: Schedule, duration_minutes: int):
    slots = []
    start_dt = datetime.combine(datetime.utcnow().date(), schedule.start_time)
    end_dt = datetime.combine(datetime.utcnow().date(), schedule.end_time)
    delta = timedelta(minutes=duration_minutes)
    cursor = start_dt
    while cursor + delta <= end_dt:
        slots.append((cursor.time(), (cursor + delta).time()))
        cursor += delta
    return slots
