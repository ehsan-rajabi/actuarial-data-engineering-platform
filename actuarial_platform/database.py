from sqlalchemy import create_engine, text
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("MSSQL_SA_PASSWORD")

connection_string = (
    f"mssql+pyodbc://sa:{password}@10.211.55.2:1433/actuarial"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(connection_string)






with engine.begin() as connection:

    # 1. Current employees
    connection.execute(text("""
        IF OBJECT_ID('current_employees', 'U') IS NULL
        CREATE TABLE current_employees (
            Code INT,
            StatusTitle NVARCHAR(50),
            DegreeCode INT,
            GenderCode INT,
            [birth date] VARCHAR(10),
            [married status] NVARCHAR(30),
            history INT,
            wage BIGINT
        )
    """))

    # 2. Retired
    connection.execute(text("""
        IF OBJECT_ID('retired', 'U') IS NULL
        CREATE TABLE retired (
            Id INT,
            GenderCode INT,
            birthDate VARCHAR(10),
            anniuity BIGINT
        )
    """))

    # 3. Survivor
    connection.execute(text("""
        IF OBJECT_ID('survivor', 'U') IS NULL
        CREATE TABLE survivor (
            id INT,
            birthDate VARCHAR(10),
            GenderCode NVARCHAR(10),
            anniuity BIGINT
        )
    """))

print("All three tables created successfully.")


df = pd.read_excel("data/current_employees.xlsx")
df.to_sql("current_employees", con=engine,if_exists="replace",index=False)

print("Current employees imported successfully.")
df = pd.read_excel("data/retired.xlsx")

df.to_sql("retired", con=engine,if_exists="replace",index=False)
print("retired imported successfully.")
df = pd.read_excel("data/survivor.xlsx")
df.to_sql("survivor", con=engine,if_exists="replace",index=False)
print("survivor imported successfully.")



with engine.begin() as connection:

    connection.execute(text("""
        IF COL_LENGTH('current_employees', 'PersonKey') IS NULL
        ALTER TABLE current_employees
        ADD PersonKey INT IDENTITY(1,1)
    """))

    connection.execute(text("""
        IF COL_LENGTH('retired', 'PersonKey') IS NULL
        ALTER TABLE retired
        ADD PersonKey INT IDENTITY(1,1)
    """))

    connection.execute(text("""
        IF COL_LENGTH('survivor', 'PersonKey') IS NULL
        ALTER TABLE survivor
        ADD PersonKey INT IDENTITY(1,1)
    """))

print("PersonKey added successfully.")