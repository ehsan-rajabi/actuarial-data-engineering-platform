from sqlalchemy import Column, Integer, BigInteger, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CurrentEmployee(Base):
    __tablename__ = "current_employees"

    PersonKey = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(BigInteger)
    StatusTitle = Column(String)
    DegreeCode = Column(BigInteger)
    GenderCode = Column(BigInteger)
    birth_date = Column("birth date", String)
    married_status = Column("married status", String)
    history = Column(BigInteger)
    wage = Column(Float)


class Retired(Base):
    __tablename__ = "retired"

    PersonKey = Column(Integer, primary_key=True, autoincrement=True)
    GenderCode = Column(BigInteger)
    Id = Column(String)
    birthDate = Column(String)
    anniuity = Column(String)


class Survivor(Base):
    __tablename__ = "survivor"

    PersonKey = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String)
    birthDate = Column(String)
    GenderCode = Column(String)
    anniuity = Column(BigInteger)