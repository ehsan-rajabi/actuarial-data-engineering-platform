from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("MSSQL_SA_PASSWORD")

connection_string = (
    f"mssql+pyodbc://sa:{password}@localhost:1433/actuarial"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

