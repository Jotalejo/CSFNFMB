from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .base import Base

# Tabla de asociación para la relación many-to-many entre Usuario y Role
usuario_roles = Table(
    'usuario_roles',
    Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255))
    is_active = Column(Boolean, default=False)
    # Secret para Google Authenticator
    otp_secret = Column(String(32), nullable=True)
    otp_enabled = Column(Boolean, default=False)  # Si tiene 2FA activado
    roles = relationship("Role", secondary=usuario_roles,
                         back_populates="usuarios")


class TokenTable(Base):
    __tablename__ = "tokens"
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    access_token = Column(String(450), primary_key=True, index=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    usuarios = relationship(
        "Usuario", secondary=usuario_roles, back_populates="roles")
