from sqlalchemy import Column, Integer, Float, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    retirement_age = Column(Integer, nullable=False)

    pension = Column(Float, nullable=False)

    monthly_contribution = Column(Float, nullable=False)

    annual_return = Column(Float, nullable=False)