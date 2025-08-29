from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer,primary_key=True,index=True)
    nombre = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255))
    is_active = Column(Boolean,default=False)

class TokenTable(Base):
    __tablename__ = "tokens"
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    access_token = Column(String(450), primary_key=True, index=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
