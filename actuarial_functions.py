def annuity_at_retirement_time(wage,service_years,assumptions):
    b=1/(1+assumptions["rate_wage_increase"]+assumptions["productivity_rate"])
    average_wage_at_retiremrnt=(wage+(wage*b))/2
    benefit=average_wage_at_retiremrnt*(service_years/30)
    return benefit


def calculate_survival_probability(age, age_at_retirement, gender, life_table):

    if gender == 1:
        return life_table.iloc[age_at_retirement, 1]/life_table.iloc[age,1]
    else:
        return life_table.iloc[age_at_retirement, 2]/life_table.iloc[age, 2]


def retiment_age_services_wage (
                               age, 
                               gender, 
                               service_years, 
                               wage,
                               rate_wage_increase,
                               productivity_rate,
                               male_retirement_age,
                               female_retirement_age,
                               male_retiement_service,
                               female_retirement_service,
                               max_service_years
                               ):
      if gender==1:
                  while(service_years < male_retiement_service and age < male_retirement_age) and (service_years< max_service_years):
                   age=age+1
                   service_years=service_years+1
                   wage=wage*(1+rate_wage_increase+productivity_rate)
      else:
            while(service_years < female_retirement_service and age < female_retirement_age) and (service_years< max_service_years-5):
                 age=age+1
                 service_years=service_years+1
                 wage=wage*(1+rate_wage_increase+productivity_rate)
      return(age,service_years,wage)


def age_service_wage_legibility(service_years,distance_to_retirement,wage_at_retirement,rate_wage_increase,productivity_rate):
            if (service_years>=28):
             increase_eligibility=0
             wage_increase_eligibility=wage_at_retirement
             return(increase_eligibility,wage_increase_eligibility)
            elif (22<=service_years<=27):
              increase_eligibility=int(distance_to_retirement*3/12)
              wage_increase_eligibility=wage_at_retirement*(1+rate_wage_increase+productivity_rate)**increase_eligibility
              return(increase_eligibility,wage_increase_eligibility)
            elif(17 <=service_years<=21):
                 increase_eligibility=int(distance_to_retirement*4/12)
                 wage_increase_eligibility=wage_at_retirement*(1+rate_wage_increase+productivity_rate)**increase_eligibility
                 return(increase_eligibility,wage_increase_eligibility)
            elif(10<=service_years<=16):
                increase_eligibility=int(distance_to_retirement*5/12)
                wage_increase_eligibility=wage_at_retirement*(1+rate_wage_increase+productivity_rate)**increase_eligibility
                return(increase_eligibility,wage_increase_eligibility)
            else:
                 increase_eligibility=int(distance_to_retirement*5/12)
                 wage_increase_eligibility=wage_at_retirement*(1+rate_wage_increase+productivity_rate)**increase_eligibility
                 return(increase_eligibility,wage_increase_eligibility)

def age_service_limitation(
        retirement_age,
        service_at_retirement,
        increase_service_eligibility,
        wage_increase_eligibility,
        rate_wage_increase,
        productivity_rate
):

    k = min(
        max(0, 62 - retirement_age),
        max(0, 35 - service_at_retirement)
    )

    if increase_service_eligibility > k:

        removed_years = increase_service_eligibility - k

        new_retirement_age = retirement_age + k
        new_service_at_retirement = service_at_retirement + k

        wage_increase_eligibility = (
            wage_increase_eligibility /
            (1 + rate_wage_increase+productivity_rate) ** removed_years
        )

    else:
        new_retirement_age = retirement_age + increase_service_eligibility
        new_service_at_retirement = service_at_retirement + increase_service_eligibility

    return (
        new_retirement_age,
        new_service_at_retirement,
        wage_increase_eligibility
    )

def actuarial_liability_at_current_age(age,gender,limited_at_retirement_age,limited_wage_increase_eligibility,limited_service_at_retirement,life_table,assumptions):
    years_after_retirement=1
    liability=0
    benefit_at_retirement=annuity_at_retirement_time(limited_wage_increase_eligibility,limited_service_at_retirement,assumptions) 
    for  future_age in range(limited_at_retirement_age,106):
        survival=calculate_survival_probability(future_age,future_age+1, gender, life_table)
        v=survival*benefit_at_retirement*(1+assumptions["rate_annuity_increase"]) 
        liability=v*((1/(1+assumptions["discount_rate"]))**years_after_retirement)+liability
        years_after_retirement=years_after_retirement+1
    liability_at_current_age=liability*(1/(1+assumptions["discount_rate"]))**(limited_at_retirement_age-age)*calculate_survival_probability(age,limited_at_retirement_age, gender, life_table)
    return liability_at_current_age

################################################acuried liability and normal cost##############################################
###############################################################################################################################
##############################################################################################################################

class liability_calculator_employees:
    def __init__(self,row):
        self.row=row
    def normal_cost(self):
      normal_cost=self.row["actuarial_liability_at current_age"]*12/self.row["limited_service_at_retirement"]
      return normal_cost

    def accuired_liability(self,normal_cost):
      accurued_liability=normal_cost*self.row["service_years"]
      return accurued_liability

#####################################################death_benefit_before_retirement##############################################
##########################################################################################################
def death_benfit_before_retirement(gender,wage,service_years,age,limited_at_retirement_age,life_table,assumptions):
   n=1
   survival = 1
   q=1
   future_service=service_years
   death_benefit_liability_before_retirement=0
   for future_age in range(age,limited_at_retirement_age):
        survival_q=calculate_survival_probability(future_age,future_age+1, gender, life_table)
        q=1-survival_q
        probablity_death=survival*q
        survival*=survival_q
        future_wage=wage*(1+assumptions["rate_wage_increase"]+assumptions["productivity_rate"])**n
        future_service=future_service+1
        if(future_service<15):
            death_benefit_annuity=annuity_at_retirement_time(future_wage,15,assumptions)
        else:
            death_benefit_annuity=annuity_at_retirement_time(future_wage,future_service,assumptions)
        present_value_anniuity_death_each_year=0
        for j in range(1,30):
         anniuity_death_each_year=((1+assumptions["rate_annuity_increase"])**j)*death_benefit_annuity
         present_value_anniuity_death_each_year+=anniuity_death_each_year*(1/(1+assumptions["discount_rate"]))**j
        death_benefit_liability_before_retirement+=probablity_death*present_value_anniuity_death_each_year*(1/(1+assumptions["discount_rate"]))**n
        n=n+1
   return death_benefit_liability_before_retirement

def persent_value_future_permiums (gender,wage,age,limited_at_retirement_age,life_table,assumptions):
   n=1
   survival = 1
   persent_value_future_permiums_employer=0
   persent_value_future_permiums_employee=0
   for future_age in range(age,limited_at_retirement_age):
        survival*=calculate_survival_probability(future_age,future_age+1, gender, life_table)
        future_wage=wage*(1+assumptions["rate_wage_increase"]+assumptions["productivity_rate"])**n
        persent_value_future_permiums_employer+=future_wage*survival*assumptions["permium_rate_employer"]*12*(1/(1+assumptions["discount_rate"]))**n
        persent_value_future_permiums_employee+=future_wage*survival*assumptions["permium_rate_employee"]*12*(1/(1+assumptions["discount_rate"]))**n
        n=n+1
   return(persent_value_future_permiums_employer,persent_value_future_permiums_employee)


def liabilities_of_retired_employees(gender,age,anniuity,life_table,assumptions,):
    Persent_value_liabilities_retired_people=0
    n=1
    survival=1
    for future_age in range(age,106):
        survival*=calculate_survival_probability(future_age,future_age+1, gender, life_table)
        future_anniuty=anniuity*(1+assumptions["rate_annuity_increase"])**n
        Persent_value_liabilities_retired_people+=future_anniuty*12*survival*(1/(1+assumptions["discount_rate"]))**n
        n=n+1
    return(Persent_value_liabilities_retired_people)

def liabilities_of_survivors(gender,age,anniuity,life_table,assumptions,):
    Persent_value_liabilities_survivors=0
    n=1
    survival=1
    for future_age in range(age,106):
        survival*=calculate_survival_probability(future_age,future_age+1, gender, life_table)
        future_anniuty=anniuity*(1+assumptions["rate_annuity_increase"])**n
        Persent_value_liabilities_survivors+=future_anniuty*12*survival*(1/(1+assumptions["discount_rate"]))**n
        n=n+1
    return(Persent_value_liabilities_survivors)





def income_projection_new_retired(
        gender,
        age,
        wage,
        limited_at_retirement_age,
        limited_wage_increase_eligibility,
        limited_service_at_retirement,
        projection_years,
        life_table,
        assumptions
):

    future_income = [0] * projection_years
    future_expenses_new_retired = [0] * projection_years
    benefit_at_retirement = annuity_at_retirement_time(limited_wage_increase_eligibility,limited_service_at_retirement,assumptions)
    distance_to_retirement = limited_at_retirement_age - age

    for i in range(1, projection_years + 1):

        # cumulative survival probability until projection year i
        survival = 1

        for j in range(i):
            survival *= calculate_survival_probability(
                age + j,
                age + j + 1,
                gender,
                life_table
            )

        # Person is still active
        if distance_to_retirement >= i:

            future_salary = wage *(1+ assumptions["rate_wage_increase"]+ assumptions["productivity_rate"]) ** i

            employer_income = future_salary* 12* assumptions["permium_rate_employer"]

            employee_income = future_salary* 12 * assumptions["permium_rate_employee"]

            future_income[i-1] = (employer_income + employee_income) * survival


        # Person retired during projection
        else:

            

            years_after_retirement = (i - distance_to_retirement)

            future_annuity = benefit_at_retirement*(1 + assumptions["rate_annuity_increase"]) ** years_after_retirement
            

            future_expenses_new_retired[i-1] = (
                future_annuity * survival
            )


    return future_income, future_expenses_new_retired


def expense_projection_current_retired(gender,age,anniuity,projection_years,life_table,assumptions,):
    future_expense=[0]*projection_years
    max_age=len(life_table)-1
    for i in range(1,projection_years+1):
        survival=1
        if age +i > max_age:
            break
        survival=1
        for j in range(i):
         survival *=calculate_survival_probability(age+j,age+j+1, gender, life_table)
        future_anniuty=12*anniuity*(1+assumptions["rate_annuity_increase"])**i
        future_expense[i-1]=future_anniuty*survival
        
    return(future_expense)

def expense_projection_current_survivirs(gender,age,anniuity,projection_years,life_table,assumptions,):
    future_expense=[0]*projection_years
    max_age=len(life_table)-1
    for i in range(1,projection_years+1):
        survival=1
        if age +i > max_age:
            break
        survival=1
        for j in range(i):
         survival *=calculate_survival_probability(age+j,age+j+1, gender, life_table)
        future_anniuty=12*anniuity*(1+assumptions["rate_annuity_increase"])**i
        future_expense[i-1]=future_anniuty*survival
        
    return(future_expense)


def death_expense_active_employee(
    gender,
    age,
    wage,
    service_years,
    limited_at_retirement_age,
    projection_years,
    life_table,
    assumptions
):

    future_death_expense = [0.0] * projection_years

    distance_to_retirement = limited_at_retirement_age - age

    for death_year in range(1, projection_years + 1):

        # No new active-employee deaths after retirement
        if death_year > distance_to_retirement:
            break

        # Survival until the beginning of the death year
        survival = 1

        for j in range(death_year - 1):
            survival *= calculate_survival_probability(
                age + j,
                age + j + 1,
                gender,
                life_table
            )

        # Probability of dying during death year
        survival_next_year = calculate_survival_probability(
            age + death_year - 1,
            age + death_year,
            gender,
            life_table
        )

        death_probability = survival * (1 - survival_next_year)

        # Salary at time of death
        future_wage = (
            wage
            * (
                1
                + assumptions["rate_wage_increase"]
                + assumptions["productivity_rate"]
            ) ** death_year
        )

        # Service at time of death
        future_service = service_years + death_year

        # Minimum 15 years of service
        benefit_service = max(future_service, 15)

        # Annuity created by death
        death_benefit_annuity = annuity_at_retirement_time(
            future_wage,
            benefit_service,
            assumptions
        )
        # ------------------------------------------------
        # Survivor annuity continues for 30 years
        # ------------------------------------------------

        for years_after_death in range(30):

            payment_year = death_year + years_after_death

            # Outside our projection
            if payment_year > projection_years:
                break

            future_annuity = (
                death_benefit_annuity*12
                * (
                    1 + assumptions["rate_annuity_increase"]
                ) ** years_after_death
            )

            future_death_expense[payment_year - 1] += (
                death_probability * future_annuity
            )

    return future_death_expense




def investment_projection(
    premium_income,
    total_expense,
    projection_years,
    assumptions
):

    investment_income = [0.0] * projection_years
    borrowing_expense = [0.0] * projection_years
    investment_balance = [0.0] * projection_years
    net_cash_flow = [0.0] * projection_years

    beginning_balance = assumptions["current_investment"]

    for i in range(projection_years):

        # Investment income if fund has positive balance
        if beginning_balance > 0:

            investment_income[i] = (
                beginning_balance
                * assumptions["interst_rate"]
            )

        else:

            investment_income[i] = 0

        # Borrowing expense if fund has negative balance
        if beginning_balance < 0:

            borrowing_expense[i] = (
                abs(beginning_balance)
                * assumptions["borrowing_rate"]
            )

        else:

            borrowing_expense[i] = 0

        # Net cash flow
        net_cash_flow[i] = (
            premium_income.iloc[i]
            + investment_income[i]
            - total_expense.iloc[i]
            - borrowing_expense[i]
        )

        # Ending balance
        ending_balance = (
            beginning_balance
            + net_cash_flow[i]
        )

        investment_balance[i] = ending_balance

        beginning_balance = ending_balance

    return (
        investment_income,
        borrowing_expense,
        investment_balance,
        net_cash_flow
    )

#############################################################################################################################
#####################################################population_projection###################################################
###########################################################################################################################
def employee_number_projection(
    age,
    gender,
    distance_to_retirement,
    projection_years,
    life_table
):
    """
    Calculate expected active members, deaths and new retirees
    for one current active employee over the projection period.
    """

    expected_active = [0] * projection_years
    expected_deaths = [0] * projection_years
    expected_new_retirees = [0] * projection_years

    survival = 1

    for i in range(1, projection_years + 1):

        # Survival probability during the current year
        annual_survival = calculate_survival_probability(
            age + i - 1,
            age + i,
            gender,
            life_table
        )

        # Probability of being alive at the END of this year
        survival_next = survival * annual_survival

        # Death during this year
        death_probability = survival - survival_next

        # =====================================================
        # ACTIVE
        # =====================================================

        if distance_to_retirement >= i:

            expected_active[i - 1] = survival_next

        # =====================================================
        # RETIREMENT
        # =====================================================

        elif distance_to_retirement == i - 1:

            # Employee reaches retirement during this year
            expected_new_retirees[i - 1] = survival_next

        # =====================================================
        # UPDATE SURVIVAL
        # =====================================================

        expected_deaths[i - 1] = death_probability

        survival = survival_next

    return (
        expected_active,
        expected_deaths,
        expected_new_retirees
    )

def new_retired_population_projection(
    age,
    gender,
    distance_to_retirement,
    projection_years,
    life_table
):
    """
    Calculate:
    1. Expected retired population in each projection year
    2. Expected deaths among retired members in each projection year
    """

    # ---------------------------------------------------------
    # Get new retirees from the first function
    # ---------------------------------------------------------

    (
        expected_active,
        expected_deaths,
        new_retirees
    ) = employee_number_projection(
        age=age,
        gender=gender,
        distance_to_retirement=distance_to_retirement,
        projection_years=projection_years,
        life_table=life_table
    )

    # ---------------------------------------------------------
    # Output arrays
    # ---------------------------------------------------------

    retired_population = [0] * projection_years
    retired_deaths = [0] * projection_years

    # ---------------------------------------------------------
    # Follow each retirement cohort
    # ---------------------------------------------------------

    for retirement_year in range(1, projection_years + 1):

        new_retiree = new_retirees[retirement_year - 1]

        if new_retiree == 0:
            continue

        # Age at retirement
        retirement_age = age + retirement_year

        survival_after_retirement = 1

        # -----------------------------------------------------
        # Follow this cohort after retirement
        # -----------------------------------------------------

        for projection_year in range(
            retirement_year,
            projection_years + 1
        ):

            # ---------------------------------------------
            # Retirement year
            # ---------------------------------------------

            if projection_year == retirement_year:

                retired_population[projection_year - 1] += (
                    new_retiree
                )

            # ---------------------------------------------
            # After retirement
            # ---------------------------------------------

            else:

                age_at_previous_year = (
                    retirement_age
                    + projection_year
                    - retirement_year
                    - 1
                )

                annual_survival = calculate_survival_probability(
                    age_at_previous_year,
                    age_at_previous_year + 1,
                    gender,
                    life_table
                )

                death_probability = 1 - annual_survival

                # Expected deaths from this retirement cohort
                retired_deaths[projection_year - 1] += (
                    new_retiree
                    * survival_after_retirement
                    * death_probability
                )

                # Update survival
                survival_after_retirement *= annual_survival

                # Expected retired population
                retired_population[projection_year - 1] += (
                    new_retiree
                    * survival_after_retirement
                )

    return retired_population, retired_deaths


def current_retiree_projection(
    age,
    gender,
    projection_years,
    life_table
):

    survival_probabilities = [1.0]
    death_probabilities = [0.0]

    if gender == 1:
        valid_ages = life_table.loc[
            life_table["male"].notna(), "age"
        ]
    else:
        valid_ages = life_table.loc[
            life_table["female"].notna(), "age"
        ]

    max_age = int(valid_ages.max())

    for year in range(1, projection_years + 1):

        future_age = age + year

        if future_age > max_age:
            survival_probabilities.append(0.0)
            death_probabilities.append(
                survival_probabilities[-2]
            )
            continue

        survival_probability = calculate_survival_probability(
            age,
            future_age,
            gender,
            life_table
        )

        previous_survival = survival_probabilities[-1]

        one_year_survival = calculate_survival_probability(
            future_age - 1,
            future_age,
            gender,
            life_table
        )

        death_probability = (
            previous_survival * (1 - one_year_survival)
        )

        survival_probabilities.append(
            survival_probability
        )

        death_probabilities.append(
            death_probability
        )

    return survival_probabilities, death_probabilities

def current_survivor_projection(
    age,
    gender,
    projection_years,
    life_table
):

    survival_probabilities = [1.0]
    death_probabilities = [0.0]

    if gender == "مرد":
        valid_ages = life_table.loc[
            life_table["male"].notna(), "age"
        ]
    else:
        valid_ages = life_table.loc[
            life_table["female"].notna(), "age"
        ]

    max_age = int(valid_ages.max())

    for year in range(1, projection_years + 1):

        future_age = age + year

        if future_age > max_age:
            survival_probabilities.append(0.0)
            death_probabilities.append(
                survival_probabilities[-2]
            )
            continue

        survival_probability = calculate_survival_probability(
            age,
            future_age,
            gender,
            life_table
        )

        previous_survival = survival_probabilities[-1]

        one_year_survival = calculate_survival_probability(
            future_age - 1,
            future_age,
            gender,
            life_table
        )

        death_probability = (
            previous_survival * (1 - one_year_survival)
        )

        survival_probabilities.append(
            survival_probability
        )

        death_probabilities.append(
            death_probability
        )

    return survival_probabilities, death_probabilities