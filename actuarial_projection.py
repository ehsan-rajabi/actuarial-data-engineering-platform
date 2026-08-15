import pandas as pd
from current_employees import data
from actuarial_functions import income_projection_new_retired
from actuarial_functions import expense_projection_current_retired
from actuarial_functions import expense_projection_current_survivirs
from actuarial_functions import death_expense_active_employee
from actuarial_functions import investment_projection
from actuarial_functions import employee_number_projection
from actuarial_functions import new_retired_population_projection
from actuarial_functions import current_retiree_projection
from actuarial_functions import current_survivor_projection
from data_cleaning import life_table
from current_employees import assumptions
from current_employees import data_retirement
from current_employees import data_survivor
pd.set_option("display.float_format", lambda x: f"{x:,.0f}")
projection_years = 30
########################################################################################################################################
###################################################income_projection_expense_projection_current_employees#####################################################
#######################################################################################################################################
projection_columns = [ f"Year_{i}" for i in range(1, projection_years + 1)]

future_income_df = pd.DataFrame(
    0.0,
    index=data.index,
    columns=projection_columns
)

future_new_retired_expense_df = pd.DataFrame(
    0.0,
    index=data.index,
    columns=projection_columns
)

for index, employee in data.iterrows():

    income, expense = income_projection_new_retired(
        gender=employee["GenderCode"],
        age=employee["age"],
        wage=employee["wage"],
        limited_at_retirement_age=employee["limited_retirement_age"],
        limited_wage_increase_eligibility=employee["limited_wage_increase_eligibility"],
        limited_service_at_retirement=employee["limited_service_at_retirement"],
        projection_years=projection_years,
        life_table=life_table,
        assumptions=assumptions
    )

    future_income_df.loc[index] = income
    future_new_retired_expense_df.loc[index] = expense

total_income_projection = future_income_df.sum(axis=0)
total_expense_projection_employee=future_new_retired_expense_df.sum(axis=0)
########################################################################################################################################
###################################################expense_projection_retire_dpeople#####################################################
#######################################################################################################################################
projection_columns = [
    f"Year_{i}" for i in range(1, projection_years+1)
]


future_retired_expense_df = pd.DataFrame(
    0.0,
    index=data_retirement.index,
    columns=projection_columns
)

for index, retired in data_retirement.iterrows():

    expense =expense_projection_current_retired (
        gender=retired["GenderCode"],
        age=retired["age"],
        anniuity=retired ["anniuity"],
        projection_years=projection_years,
        life_table=life_table,
        assumptions=assumptions
    )

    future_retired_expense_df.loc[index] = expense

    total_expense_projection_current_retired=future_retired_expense_df.sum(axis=0)




    projection_columns = [
    f"Year_{i}" for i in range(1, projection_years+1)
]
########################################################################################################################################
###################################################expense_projection_survivorse#####################################################
#######################################################################################################################################

future_survivors_expense_df = pd.DataFrame(
    0.0,
    index=data_survivor.index,
    columns=projection_columns
)
for index, survivor in data_survivor.iterrows():

    expense =expense_projection_current_survivirs (
        gender=survivor["GenderCode"],
        age=survivor["age"],
        anniuity=survivor ["anniuity"],
        projection_years=projection_years,
        life_table=life_table,
        assumptions=assumptions
    )

    future_survivors_expense_df.loc[index] = expense

    total_expense_projection_current_survivors=future_survivors_expense_df.sum(axis=0)

#########################################################################################################################################
###############################################death_expense_active_employee##########################################################
#######################################################################################################################################
projection_columns = [ f"Year_{i}" for i in range(1, projection_years + 1)]

future_expense_death_active_employee = pd.DataFrame(
    0.0,
    index=data.index,
    columns=projection_columns
)
for index, employee in data.iterrows():

     expense = death_expense_active_employee(
        gender=employee["GenderCode"],
        age=employee["age"],
        wage=employee["wage"],
        service_years=employee["service_years"],
        limited_at_retirement_age=employee["limited_retirement_age"],
        projection_years=projection_years,
        life_table=life_table,
        assumptions=assumptions
    )
     future_expense_death_active_employee.loc[index] = expense

total_expense_projection_death_active_employee=future_expense_death_active_employee.sum(axis=0)

#########################################################################################################################################
###############################################invest_income_projection##########################################################
#######################################################################################################################################

investment_income,borrowing_expense, investment_balance,net_cash_flow = investment_projection(premium_income=total_income_projection,
                                                              total_expense=(total_expense_projection_employee+
                                                                            total_expense_projection_current_retired+
                                                                            total_expense_projection_current_survivors +
                                                                            total_expense_projection_death_active_employee),
                                                                            projection_years=projection_years,assumptions=assumptions)

#######################################################################################################################################
#########################################################cash_flow_projection#########################################################
#####################################################################################################################################
cash_flow_df=pd.DataFrame ({ "permium_income":total_income_projection,
                             "investment_income":investment_income,
                             "investment_balance":investment_balance,
                             "total_income":(total_income_projection+investment_income),
                             "new_retired_expense":total_expense_projection_employee,
                             "current_retired_expense":total_expense_projection_current_retired,
                             "current_retired_survivos":total_expense_projection_current_survivors,
                             "expences_disability":total_expense_projection_death_active_employee,
                             "total_expense":(total_expense_projection_employee+
                                            total_expense_projection_current_retired+
                                            total_expense_projection_current_survivors +
                                            total_expense_projection_death_active_employee),
                             "borrowing_expense": borrowing_expense,
                             "cash_flow":net_cash_flow
                            })

cash_flow_with_investment = cash_flow_df.copy()

cash_flow_with_investment = cash_flow_with_investment / 1_000_000

#print(cash_flow_with_investment.head(30))

cash_flow_df_withoutinvestment=pd.DataFrame ({ "permium_income":total_income_projection,
                             "new_retired_expense":total_expense_projection_employee,
                             "current_retired_expense":total_expense_projection_current_retired,
                             "current_retired_survivos":total_expense_projection_current_survivors,
                             "expences_disability":total_expense_projection_death_active_employee,
                             "total_expense":(total_expense_projection_employee+
                                            total_expense_projection_current_retired+
                                            total_expense_projection_current_survivors +
                                            total_expense_projection_death_active_employee),
                             "cash_flow":total_income_projection-(total_expense_projection_employee+
                                            total_expense_projection_current_retired+
                                            total_expense_projection_current_survivors +
                                            total_expense_projection_death_active_employee)
                            })
cash_flow_final_without_investment = cash_flow_df_withoutinvestment.copy()
cash_flow_final_without_investment = cash_flow_final_without_investment / 1_000_000
#print(cash_flow_final_without_investment.head(30))

########################################################################################################################################
##########################################################population projection#########################################################
#######################################################################################################################################
projection_years = 20

total_active = [0] * projection_years
total_deaths = [0] * projection_years
total_new_retirees = [0] * projection_years

for _, employee in data.iterrows():

    active, deaths, new_retirees = employee_number_projection(
        age=employee["age"],
        gender=employee["GenderCode"],
        distance_to_retirement=employee["distance_to_retirment"],
        projection_years=projection_years,
        life_table=life_table
    )

    for i in range(projection_years):

        total_active[i] += active[i]
        total_deaths[i] += deaths[i]
        total_new_retirees[i] += new_retirees[i]

employee_number_projection_df = pd.DataFrame({
    "Projection_Year": range(1, projection_years + 1),
    "Expected_Active": [round(x) for x in total_active],
    "Expected_Deaths": [round(x) for x in total_deaths],
    "Expected_New_Retirees": [round(x) for x in total_new_retirees]
})
#print(employee_number_projection_df.head(20))

projection_years = 20

total_retired = [0] * projection_years
total_retired_deaths = [0] * projection_years

for _, employee in data.iterrows():

   
    retired_population, retired_deaths = new_retired_population_projection(
        age=employee["age"],
        gender=employee["GenderCode"],
        distance_to_retirement=employee["distance_to_retirment"],
        projection_years=projection_years,
        life_table=life_table
    )

    # -----------------------------------------
    # Aggregate results
    # -----------------------------------------

    for i in range(projection_years):

        total_retired[i] += retired_population[i]

        total_retired_deaths[i] += retired_deaths[i]

employee_number_projection_df["Retired_Members"] = [
    round(x) for x in total_retired
]

employee_number_projection_df["Deaths_Retired"] = [
    round(x) for x in total_retired_deaths
]



retiree_projections = []

for _, retiree in data_retirement.iterrows():

    survival, death = current_retiree_projection(
        age=int(retiree["age"]),
        gender=int(retiree["GenderCode"]),
        projection_years=projection_years,
        life_table=life_table
    )

    retiree_projections.append({
        "age": retiree["age"],
        "gender": retiree["GenderCode"],
        "survival": survival,
        "death": death
    })


    retired_population = [len(data_retirement)]
new_survivors_from_retirees = [0]

for year in range(1, projection_years + 1):

    total_retired = 0
    total_new_survivors = 0

    for _, retiree in data_retirement.iterrows():

        survival, death = current_retiree_projection(
            age=int(retiree["age"]),
            gender=int(retiree["GenderCode"]),
            projection_years=projection_years,
            life_table=life_table
        )

        total_retired += survival[year]
        total_new_survivors += death[year]

    retired_population.append(round(total_retired, 2))
    new_survivors_from_retirees.append(round(total_new_survivors, 2))


employee_number_projection_df["retired_population_alive"] = [int(round(x)) for x in retired_population[1:]]

employee_number_projection_df["new_survivors_from_retirees"] = [int(round(x)) for x in new_survivors_from_retirees[1:]]

#print(employee_number_projection_df.head(20))

survivor_projections = []

for _, retiree in data_retirement.iterrows():

    survival, death = current_retiree_projection(
        age=int(retiree["age"]),
        gender=int(retiree["GenderCode"]),
        projection_years=projection_years,
        life_table=life_table
    )

    survivor_projections.append({
        "age": retiree["age"],
        "gender": retiree["GenderCode"],
        "survival": survival,
        "death": death
    })


    survivor_population = [len(data_survivor)]
new_death_from_survior = [0]

for year in range(1, projection_years + 1):

    total_survivor = 0
    total_new_death_survivors = 0

    for _, survivor in data_survivor.iterrows():

        survival, death = current_survivor_projection(
            age=int(survivor["age"]),
            gender=survivor["GenderCode"],
            projection_years=projection_years,
            life_table=life_table
        )

        total_survivor+= survival[year]
        total_new_death_survivors += death[year]

    survivor_population.append(round(total_survivor, 2))
    new_death_from_survior.append(round(total_new_death_survivors, 2))


employee_number_projection_df["survivor_population_alive"] = [int(round(x)) for x in survivor_population[1:]]

employee_number_projection_df["new_death_from_survivor"] = [int(round(x)) for x in new_death_from_survior[1:]]

#print(employee_number_projection_df.head(20))
employee_number_projection_df["total_new survivor"]=employee_number_projection_df["new_survivors_from_retirees"]+employee_number_projection_df["Expected_Deaths"]+employee_number_projection_df["Deaths_Retired"]
survivor_population = []

current_survivors = len(data_survivor)

for _, row in employee_number_projection_df.iterrows():

    current_survivors = (
        current_survivors
        + row["total_new survivor"]
        - row["new_death_from_survivor"]
    )

    survivor_population.append(current_survivors)

employee_number_projection_df["Survivors_total"] = [
    int(round(x)) for x in survivor_population
]



final_population_projection = pd.DataFrame({
    "Projection_Year": employee_number_projection_df["Projection_Year"],
    "Active": employee_number_projection_df["Expected_Active"],
    "Retired": employee_number_projection_df["retired_population_alive"]+employee_number_projection_df["Retired_Members"],
    "Survivors": employee_number_projection_df["Survivors_total"],
    "support ratio":employee_number_projection_df["Expected_Active"]/(employee_number_projection_df["retired_population_alive"]+employee_number_projection_df["Retired_Members"]+employee_number_projection_df["Survivors_total"])
})
#print(final_population_projection.head(20))


with pd.ExcelWriter("output/projection_results.xlsx", engine="openpyxl") as writer:

    final_population_projection.to_excel(
        writer,
        sheet_name="Population Details",
        index=False
    )

    cash_flow_with_investment.to_excel(
        writer,
        sheet_name="cash_flow_with_investment",
        index=False
    )

    cash_flow_final_without_investment.to_excel(
        writer,
        sheet_name="cash_flow_without_onvestment",
        index=False
    )

print("Projection results saved successfully.")