import pandas as pd
################################preparetion of life table#####################################
#############################################################################################
import pandas as pd

def clean_left_life_table(file_name):

    raw = pd.read_excel(
        file_name,
        header=None
    )

    left = raw.iloc[4:, [1, 2, 3]].copy()

    left.columns = [
        "age",
        "male",
        "female"
    ]

    left["age"] = pd.to_numeric(
        left["age"], errors="coerce"
    )

    left["male"] = pd.to_numeric(
        left["male"], errors="coerce"
    )

    left["female"] = pd.to_numeric(
        left["female"], errors="coerce"
    )

    left = left.dropna(
        subset=["age"]
    )

    left["age"] = left["age"].astype(int)

    return left

life_table_left = clean_left_life_table("life_table.xls")
def clean_right_life_table(file_name):

    raw = pd.read_excel(
        file_name,
        header=None
    )

    right = raw.iloc[4:, [5, 6, 7]].copy()

    right.columns = [
        "age",
        "male",
        "female"
    ]

    right["age"] = pd.to_numeric(
        right["age"], errors="coerce"
    )

    right["male"] = pd.to_numeric(
        right["male"], errors="coerce"
    )

    right["female"] = pd.to_numeric(
        right["female"], errors="coerce"
    )

    right = right.dropna(
        subset=["age"]
    )

    right["age"] = right["age"].astype(int)

    return right

life_table_right = clean_right_life_table("life_table.xls")


raw = pd.read_excel("life_table.xls", header=None)

life_table = pd.concat(
    [life_table_left,life_table_right [life_table_right["age"] > 55]],
    ignore_index=True
)

life_table = life_table.sort_values(
    "age"
).reset_index(drop=True)


############################################################################################################
###############################preparetion of current employess#############################################
############################################################################################################
data=pd.read_excel("data/current_employees.xlsx")

############information of table#######################
#data=pd.DataFrame(data)
#print(data.info())
#print(data.columns)
#print(data.dtypes)
####################missing value###################
#print(data.isnull().sum())
####################values in the table#######################
#print(data["GenderCode"].unique())
#print(data["DegreeCode"].unique())
#print(data["StatusTitle"].unique())
#print(data["DegreeCode"].value_counts())
#print(data[data["DegreeCode"]== 992001281])
#############################################calculating age################################################
############################################################################################################
###########################################################################################################
import jdatetime

import jdatetime


def jalali_to_gregorian(date_string):
    year, month, day = map(int, date_string.split("/"))
    jalali_date = jdatetime.date(year, month, day)
    return jalali_date.togregorian()

data["birth_date_gregorian"] = data["birth date"].apply(jalali_to_gregorian)

valuation_data_jalali=jdatetime.date(1404,12,29)
valuation_date = pd.Timestamp(valuation_data_jalali.togregorian())
data["age"] = (
    valuation_date - pd.to_datetime(data["birth_date_gregorian"])
).dt.days / 365
data["age"]=data["age"].astype(int)
data["service_years"]=data["history"]/365
data["service_years"]=data["service_years"].astype(int)

data["StatusTitle"] = data["StatusTitle"].replace({
    "فعال": "active",
    "معلق": "inactive"
})
data["DegreeCode"]=data["DegreeCode"].astype("category")


features=data[
        [
             "Code"
              ,"StatusTitle",
              "DegreeCode",
              "GenderCode",
               "married status",
               "wage",
               "age",
               "service_years"
             ]
        ].copy()

employee_code=features["Code"]
X=features.drop("Code",axis=1)

X=pd.get_dummies(X, columns=["StatusTitle","DegreeCode","married status"],dtype=int)


from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

from sklearn.ensemble import IsolationForest

model = IsolationForest(
    contamination=0.01,
    random_state=42
)

features["anomaly"] = model.fit_predict(X_scaled)


#########################################################################################################################################
########################################################################################################################################
#######################################################data cleaning for retired people#################################################
#######################################################################################################################################
#######################################################################################################################################
data_retirement=pd.read_excel("data/retired.xlsx")

############information of table#######################
data_retirement=pd.DataFrame(data_retirement)
print(data_retirement.info())
# print(data_retirement.columns)
# print(data_retirement.dtypes)
data_retirement["anniuity"] = (
 data_retirement["anniuity"]
     .str.replace(",", "", regex=False)
     .astype(float)
 )
print(data_retirement["anniuity"].head())

data_retirement["birth_date_gregorian"] = data_retirement["birthDate"].apply(jalali_to_gregorian)

valuation_data_jalali=jdatetime.date(1404,12,29)
valuation_date = pd.Timestamp(valuation_data_jalali.togregorian())
valuation_data_jalali=jdatetime.date(1404,12,29)
valuation_date = pd.Timestamp(valuation_data_jalali.togregorian())
data_retirement["age"] = (
   valuation_date - pd.to_datetime(data_retirement["birth_date_gregorian"])
 ).dt.days / 365
#print(data_retirement.columns)
data_retirement["age"]=data_retirement["age"].astype(int)
#print(data_retirement.head())

#########################################################################################################################################
########################################################################################################################################
#######################################################data cleaning for survivors#################################################
#######################################################################################################################################
#######################################################################################################################################
data_survivor=pd.read_excel("data/survivor.xlsx")


############information of table#######################
data_survivor=pd.DataFrame(data_survivor)
print(data_survivor.info())
# print(data_retirement.columns)
# print(data_retirement.dtypes)
data_survivor["birth_date_gregorian"] = data_survivor["birthDate"].apply(jalali_to_gregorian)

valuation_data_jalali=jdatetime.date(1404,12,29)
valuation_date = pd.Timestamp(valuation_data_jalali.togregorian())
valuation_data_jalali=jdatetime.date(1404,12,29)
valuation_date = pd.Timestamp(valuation_data_jalali.togregorian())
data_survivor["age"] = (
   valuation_date - pd.to_datetime(data_survivor["birth_date_gregorian"])
 ).dt.days / 365
#print(data_retirement.columns)
data_survivor["age"]=data_survivor["age"].astype(int)
print(data_survivor.dtypes)