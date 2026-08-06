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