
import pandas as pd
import numpy as np
pd.set_option("display.max_rows",None)
assumptions = {}

with open("assumptions.txt", "r") as file:
   for line in file:
         key, value = line.strip().split("=")
         assumptions[key] = float(value)
from actuarial_functions import annuity_at_retirement_time
from actuarial_functions import calculate_survival_probability
from actuarial_functions import retiment_age_services_wage
from actuarial_functions import age_service_wage_legibility
from actuarial_functions import age_service_limitation
from actuarial_functions import actuarial_liability_at_current_age
from actuarial_functions import liability_calculator_employees
from actuarial_functions import death_benfit_before_retirement
from actuarial_functions import persent_value_future_permiums
from data_cleaning import data
from data_cleaning import life_table
# benefit=annuity_at_retirement_time(5000,15,assumptions)
# print(benefit)
#print(life_table.head(10))


results=data.apply(
     lambda row:retiment_age_services_wage(
          age=row["age"],
          gender=row["GenderCode"],
          service_years=row["service_years"],
          wage=row["wage"],
          rate_wage_increase=assumptions["rate_wage_increase"],
          productivity_rate=assumptions["productivity_rate"],
          male_retirement_age=assumptions["male_retirement_age"],
          female_retirement_age=assumptions["female_retirement_age"],
          male_retiement_service=assumptions["male_retiement_service"],
          female_retirement_service=assumptions["female_retirement_service"],
          max_service_years=assumptions["max_service_years"],
        ), axis=1)


data[
     ["retirement_age",
     "service_at_retirement",
     "wage_at_retirement"
     ]
    ]=pd.DataFrame(results.tolist(),index=data.index)

data["distance_to_retirment"]=data["retirement_age"]-data["age"]

results=data.apply(
        lambda row:age_service_wage_legibility(
                 service_years=row["service_years"],
                 distance_to_retirement=row["distance_to_retirment"],
                 wage_at_retirement=row["wage_at_retirement"],
                 rate_wage_increase=assumptions["rate_wage_increase"],
                 productivity_rate=assumptions["productivity_rate"]
                                                   ),axis=1       
)

data[
     ["increase_service_eligibility",
      "wage_increase_eligibility"
     ]
    ]=pd.DataFrame(results.tolist(),index=data.index)

data["new_service_years"]=data["service_at_retirement"]+data["increase_service_eligibility"]

results = data.apply(
    lambda row: age_service_limitation(
        retirement_age=row["retirement_age"],
        service_at_retirement=row["service_at_retirement"],
        increase_service_eligibility=row["increase_service_eligibility"],
        wage_increase_eligibility=row["wage_increase_eligibility"],
        rate_wage_increase=assumptions["rate_wage_increase"],
        productivity_rate=assumptions["productivity_rate"]
    ),
    axis=1
)

data[
    [
        "limited_retirement_age",
        "limited_service_at_retirement",
        "limited_wage_increase_eligibility"
    ]
] = pd.DataFrame(
    results.tolist(),
    index=data.index
)


results=data.apply(
                 lambda row: actuarial_liability_at_current_age(
                      age=row["age"],
                      gender= row["GenderCode"],
                      limited_at_retirement_age=row["limited_retirement_age"],
                      limited_service_at_retirement=row["limited_service_at_retirement"],
                      limited_wage_increase_eligibility=row["limited_wage_increase_eligibility"],
                      life_table=life_table,
                      assumptions=assumptions

                 ),axis=1
)

data["actuarial_liability_at current_age"]=results
normal_costs=[]
accrued_liabilities=[]
for index, row in data.iterrows():

    valuation = liability_calculator_employees(row)

    nc = valuation.normal_cost()
    al = valuation.accuired_liability(nc)
    normal_costs.append(nc)
    accrued_liabilities.append(al)


data["normal_costs"]=normal_costs
data["accrued_liabilities"]=accrued_liabilities

#################################################total_normal_costs#######################################################################
#################################################total_accured_liability#################################################################
########################################################################################################################################
total_normal_costs = data["normal_costs"].sum()

total_accrued_liability = data["accrued_liabilities"].sum()

print(f"Total Normal Cost: {total_normal_costs/1_000_000:.2f} million")
print(f"Total Accrued Liability: {total_accrued_liability/1_000_000:.2f} million")

##################################################################################################################################
##################################################liability before retirement####################################################
################################################################################################################################
data["death_liability_before_retirement"]=data.apply(
                  lambda row :death_benfit_before_retirement(
                               gender=row["GenderCode"],
                               wage=row["wage"],
                               service_years=row["service_years"],
                               age=row["age"],
                               limited_at_retirement_age=row["limited_retirement_age"],
                               life_table=life_table,
                               assumptions=assumptions
                       ),axis=1
                  ) 

total_death_liability_before_retirement=data["death_liability_before_retirement"].sum()
print(f"Total death Liability before retirement: {total_death_liability_before_retirement/1_000_000:.2f} million")
###################################################################################################################################
########################################################persent value of future permiums##########################################
################################################################################################################################
results=data.apply(
                lambda row: persent_value_future_permiums (
                    gender=row["GenderCode"],
                    wage=row["wage"],
                    age=row["age"],
                    limited_at_retirement_age=row["limited_retirement_age"],
                    life_table=life_table,
                    assumptions=assumptions
                ),axis=1
)
data[["future_permiums_employer",
    "future_permiums_employee"]
    ]=pd.DataFrame(results.to_list(),index=data.index)

total_future_permiums_employer=data["future_permiums_employer"].sum()
total_future_permiums_employee=data["future_permiums_employee"].sum()
print(f"total_future_permiums_employer:{total_future_permiums_employer/1_000_000:.2f} million")
print(f"total_future_permiums_employee:{total_future_permiums_employee/1_000_000:.2f} million")

###################################################################################################################################
########################################################liabilites of retired people##########################################
################################################################################################################################
from data_cleaning import data_retirement
from actuarial_functions import liabilities_of_retired_employees
data_retirement["liabilies"]=data_retirement.apply(
                                                   lambda row :liabilities_of_retired_employees(
                                                       gender=row["GenderCode"],
                                                       age=row["age"],
                                                       anniuity= row["anniuity"],
                                                       life_table=life_table,
                                                       assumptions=assumptions
                                                   ),axis=1
)
total_liabilites_retired_people=data_retirement["liabilies"].sum()
print(f"total_liabilities_retired_people:{total_liabilites_retired_people/1_000_000:.2f} million")
###################################################################################################################################
########################################################liabilites of survivors##########################################
################################################################################################################################
from data_cleaning import data_survivor
from actuarial_functions import liabilities_of_survivors
data_survivor["liabilies"]=data_survivor.apply(
                                                   lambda row :liabilities_of_retired_employees(
                                                       gender=row["GenderCode"],
                                                       age=row["age"],
                                                       anniuity= row["anniuity"],
                                                       life_table=life_table,
                                                       assumptions=assumptions
                                                   ),axis=1
)
total_liabilites_survivors=data_survivor["liabilies"].sum()
print(f"total_liabilities_survivors:{total_liabilites_survivors/1_000_000:.2f} million")

new_retirees = (
    data["distance_to_retirment"].value_counts().sort_index()
)
print(new_retirees)