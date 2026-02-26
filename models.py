from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    insurance_type = Column(String(50))
    claim_amount = Column(Float)
    status = Column(String(50))
    request_date = Column(Date)
    approval_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")


class ClaimDocument(Base):
    __tablename__ = "claim_documents"

    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    document_type = Column(String(100))
    s3_url = Column(String)
    ocr_data = Column(JSON)
    validation_status = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())