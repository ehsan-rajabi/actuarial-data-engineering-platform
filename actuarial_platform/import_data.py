import pandas as pd
from actuarial_platform.database import engine

import pandas as pd
from actuarial_platform.database import engine
from actuarial_platform.models import CurrentEmployee,Retired,Survivor


def import_current_employees(file):
    df = pd.read_excel(file)

    # Create the table according to the SQLAlchemy model
    CurrentEmployee.__table__.drop(engine, checkfirst=True)
    CurrentEmployee.__table__.create(engine)

    # Insert the Excel data into the existing table
    df.to_sql(
        "current_employees",
        con=engine,
        if_exists="append",
        index=False
    )

    return len(df)

def import_retired(file):
    df = pd.read_excel(file)

    Retired.__table__.drop(engine, checkfirst=True)
    Retired.__table__.create(engine)

    df.to_sql(
        "retired",
        con=engine,
        if_exists="append",
        index=False
    )

    return len(df)

def import_survivor(file):
    df = pd.read_excel(file)

    Survivor.__table__.drop(engine, checkfirst=True)
    Survivor.__table__.create(engine)

    df.to_sql(
        "survivor",
        con=engine,
        if_exists="append",
        index=False
    )

    return len(df)



from pathlib import Path


ASSUMPTIONS_DIR = Path("../assumptions")


ASSUMPTION_FILES = {
    "assumptions_actual": ["assumptions_actual.txt"],

    "assumptions_expected": ["assumptions_expected.txt"],

    "assumptions_discount_real": [
        "assumptions_discount_real.txt",
        "assumptions_actual.txt"
    ],

    "assumptions_wage_real": [
        "assumptions_wage_real.txt",
        "assumptions_actual.txt"
    ],

    "assumptions_annuity_real": [
        "assumptions_annuity_real.txt",
        "assumptions_actual.txt"
    ]
}

def update_assumptions(
    assumption_set,
    discount_rate,
    rate_wage_increase,
    rate_annuity_increase,
    productivity_rate,
    male_retirement_age,
    female_retirement_age,
    male_retiement_service,
    female_retirement_service,
    max_service_years,
    permium_rate_employer,
    permium_rate_employee,
    interst_rate,
    current_investment,
    borrowing_rate
):

    assumptions = {
        "discount_rate": discount_rate,
        "rate_wage_increase": rate_wage_increase,
        "rate_annuity_increase": rate_annuity_increase,
        "productivity_rate": productivity_rate,
        "male_retirement_age": male_retirement_age,
        "female_retirement_age": female_retirement_age,
        "male_retiement_service": male_retiement_service,
        "female_retirement_service": female_retirement_service,
        "max_service_years": max_service_years,
        "permium_rate_employer": permium_rate_employer,
        "permium_rate_employee": permium_rate_employee,
        "interst_rate": interst_rate,
        "current_investment": current_investment,
        "borrowing_rate": borrowing_rate
    }

    if assumption_set not in ASSUMPTION_FILES:
        raise ValueError(
            f"Invalid assumption set: {assumption_set}. "
            f"Allowed values: {list(ASSUMPTION_FILES.keys())}"
        )

    filenames = ASSUMPTION_FILES[assumption_set]

    for filename in filenames:

        file_path = ASSUMPTIONS_DIR / filename

        with open(file_path, "w") as file:

            for name, value in assumptions.items():
                file.write(f"{name}={value}\n")

    return filenames