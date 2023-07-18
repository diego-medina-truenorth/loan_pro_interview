from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    status = Column(String)

    # Relationship with records
    records = relationship("Record", back_populates="user")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    cost = Column(Float)

    # Relationship with records
    records = relationship("Record", back_populates="operation")


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    operation_id = Column(Integer, ForeignKey("operations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    user_balance = Column(Float)
    operation_response = Column(String)
    date = Column(String)

    # Relationship with user
    user = relationship("User", back_populates="records")
    # Relationship with operation
    operation = relationship("Operation", back_populates="records")
