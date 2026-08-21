from fastapi import FastAPI, UploadFile, File, HTTPException

from import_data import (import_current_employees, import_retired, import_survivor, update_assumptions)
from schemas import ImportResponse, AssumptionsRequest


app = FastAPI(
    title="Actuarial Data API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Actuarial Data API is running"
    }


@app.post(
    "/import/employees",
    response_model=ImportResponse
)
def import_employees(
    file: UploadFile = File(...)
):

    try:
        rows = import_current_employees(file.file)

        return {
            "status": "success",
            "table": "current_employees",
            "rows_imported": rows
        }

    except Exception as e:
        print("IMPORT ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post(
        "/import/retired",
    response_model=ImportResponse
)
def import_retired_data(
    file: UploadFile = File(...)
):

    try:
        rows = import_retired(file.file)

        return {
            "status": "success",
            "table": "retired",
            "rows_imported": rows
        }

    except Exception as e:
        print("IMPORT ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post(
    "/import/survivor",
    response_model=ImportResponse
)
def import_survivor_data(
    file: UploadFile = File(...)
):

    try:
        rows = import_survivor(file.file)

        return {
            "status": "success",
            "table": "survivor",
            "rows_imported": rows
        }

    except Exception as e:
        print("IMPORT ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@app.post("/assumptions")
def update_assumption_file(
    data: AssumptionsRequest
):

    try:
        print("ASSUMPTION SET:", data.assumption_set)
        print("ASSUMPTION VALUE:", data.assumption_set.value)
        files = update_assumptions(
            assumption_set=data.assumption_set.value,
            discount_rate=data.discount_rate,
            rate_wage_increase=data.rate_wage_increase,
            rate_annuity_increase=data.rate_annuity_increase,
            productivity_rate=data.productivity_rate,
            male_retirement_age=data.male_retirement_age,
            female_retirement_age=data.female_retirement_age,
            male_retiement_service=data.male_retiement_service,
            female_retirement_service=data.female_retirement_service,
            max_service_years=data.max_service_years,
            permium_rate_employer=data.permium_rate_employer,
            permium_rate_employee=data.permium_rate_employee,
            interst_rate=data.interst_rate,
            current_investment=data.current_investment,
            borrowing_rate=data.borrowing_rate
        )

        return {
            "status": "success",
            "updated_files": files
        }

    except Exception as e:
        print("ASSUMPTION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )