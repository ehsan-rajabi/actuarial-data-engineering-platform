from pydantic import BaseModel


class ImportResponse(BaseModel):
    status: str
    table: str
    rows_imported: int
from pydantic import BaseModel
from enum import Enum


class ImportResponse(BaseModel):
    status: str
    table: str
    rows_imported: int


class AssumptionSet(str, Enum):
    actual = "assumptions_actual"
    expected = "assumptions_expected"
    discount_real = "assumptions_discount_real"
    wage_real = "assumptions_wage_real"
    annuity_real = "assumptions_annuity_real"

class AssumptionsRequest(BaseModel):
    assumption_set: AssumptionSet

    discount_rate: float
    rate_wage_increase: float
    rate_annuity_increase: float
    productivity_rate: float

    male_retirement_age: float
    female_retirement_age: float

    male_retiement_service: float
    female_retirement_service: float

    max_service_years: float

    permium_rate_employer: float
    permium_rate_employee: float

    interst_rate: float
    current_investment: float
    borrowing_rate: float

class ValuationResponse(BaseModel):
    status: str
    total_normal_cost: float
    total_accrued_liability: float