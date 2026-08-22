import pandas as pd
from sqlalchemy import create_engine
from actuarial_platform.database import engine

current_employees = pd.read_sql(
    "SELECT * FROM current_employees",
    engine
)

retired = pd.read_sql(
    "SELECT * FROM retired",
    engine
)

survivor = pd.read_sql(
    "SELECT * FROM survivor",
    engine
)

print(current_employees.head())
print(retired.head())
print(survivor.head())