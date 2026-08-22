from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# Environment variables
# --------------------------------------------------

password = os.getenv("MSSQL_SA_PASSWORD")
server = os.getenv("MSSQL_SERVER", "localhost")


# --------------------------------------------------
# Create database if it does not exist
# --------------------------------------------------

def create_database_if_not_exists():

    master_connection_string = (
        f"mssql+pyodbc://sa:{password}@{server}:1433/master"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
    )

    master_engine = create_engine(
        master_connection_string,
        isolation_level="AUTOCOMMIT"
    )

    with master_engine.connect() as connection:

        result = connection.execute(
            text("SELECT DB_ID('actuarial')")
        )

        database_id = result.scalar()

        if database_id is None:

            connection.execute(
                text("CREATE DATABASE actuarial")
            )

            print("Database 'actuarial' created.")

        else:

            print("Database 'actuarial' already exists.")

    master_engine.dispose()


# --------------------------------------------------
# Make sure actuarial database exists
# --------------------------------------------------

create_database_if_not_exists()


# --------------------------------------------------
# Connection to actuarial database
# --------------------------------------------------

connection_string = (
    f"mssql+pyodbc://sa:{password}@{server}:1433/actuarial"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True
)


# --------------------------------------------------
# SQLAlchemy session
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# --------------------------------------------------
# Database dependency for FastAPI
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()