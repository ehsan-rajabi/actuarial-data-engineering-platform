import pandas as pd
from sqlalchemy import create_engine
from database import engine
from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
from current_employees import data
####################################################################################################################################
################################################################current_employee####################################################
###################################################################################################################################
# -----------------------------
# Prepared data
# -----------------------------

prepared_columns = [
    "PersonKey",
    "age",
    "service_years",
    "retirement_age",
    "service_at_retirement",
    "wage_at_retirement",
    "distance_to_retirment",
    "increase_service_eligibility",
    "wage_increase_eligibility",
    "new_service_years",
    "limited_retirement_age",
    "limited_service_at_retirement",
    "limited_wage_increase_eligibility"
]

prepared_data_employees = data[prepared_columns]

result_columns = [
    "PersonKey",
    "actuarial_liability_at current_age",
    "normal_costs",
    "accrued_liabilities",
    "death_liability_before_retirement",
    "future_permiums_employer",
    "future_permiums_employee"
]

results_data = data[result_columns]


# -----------------------------
# Save to SQL
# -----------------------------

prepared_data_employees.to_sql(
    "employees_prepared",
    con=engine,
    if_exists="replace",
    index=False
)

results_data.to_sql(
    "employee_results",
    con=engine,
    if_exists="replace",
    index=False
)

print("Prepared data saved successfully.")
print("Actuarial results saved successfully.")
########################################################################################################################################
##########################################################retired people##################################################################
########################################################################################################################################
from current_employees import data_retirement
from current_employees import data_survivor


data_retirement.to_sql(
    "retired_results",
    con=engine,
    if_exists="replace",
    index=False
)
data_survivor.to_sql(
    "survivor_results",
        con=engine,
        if_exists="replace",
        index=False
)

########################################################################################################################################
####################################################actuarial_balance_sheet#############################################################
########################################################################################################################################
from actuarial_balance_sheet import balance_sheet_df
from sqlalchemy import types

balance_sheet_df.index.name = "Measure"

balance_sheet_df.to_sql("balance_sheet_prepare",con=engine,if_exists="replace",index=True,index_label="Measure",dtype={"Measure": types.NVARCHAR(100)})


from actuarial_balance_sheet import final_balance_sheet
final_balance_sheet.index.name = "Measure"
final_balance_sheet.to_sql("balance_sheet_final",con=engine,if_exists="replace",index=True,index_label="Measure",dtype={"Measure": types.NVARCHAR(100)})

########################################################################################################################################
#########################################################actuarial_projection_results###################################################
########################################################################################################################################
from actuarial_projection import cash_flow_with_investment
cash_flow_with_investment.index.name="year"
cash_flow_with_investment.to_sql("cash_flow_with_investment",con=engine,if_exists="replace",index=True,index_label="year",dtype={"year": types.NVARCHAR(10)} )
from actuarial_projection import cash_flow_df_withoutinvestment
cash_flow_df_withoutinvestment.index.name="year"
cash_flow_df_withoutinvestment.to_sql("cash_flow_df_withoutinvestment",con=engine,if_exists="replace",index=True,index_label="year",dtype={"year": types.NVARCHAR(10)})
from actuarial_projection import final_population_projection
final_population_projection.to_sql("final_population_projection",con=engine,if_exists="replace",index=False)