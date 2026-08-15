import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
from current_employees import data
from current_employees import data_retirement
from current_employees import data_survivor
pd.set_option("display.float_format", lambda x: f"{x:,.0f}")
def create_groups(data, column, group_size=5):

    min_value = int(data[column].min())
    max_value = int(data[column].max())

    start = (min_value // group_size) * group_size
    end = ((max_value // group_size) + 1) * group_size

    bins = list(range(start, end + group_size, group_size))

    labels = [
        f"{bins[i]}-{bins[i+1]-1}"
        for i in range(len(bins) - 1)
    ]

    data = data.copy()

    data[f"{column}_group"] = pd.cut(
        data[column],
        bins=bins,
        labels=labels,
        right=False
    )

    return data

data=create_groups(data,"age",5)
age_gender = pd.pivot_table(data,index="age_group",columns="GenderCode",values="age",aggfunc="count",fill_value=0)

age_gender = age_gender.rename(columns={2: "Female",1: "Male"})

age_gender["Total"] = age_gender["Male"] + age_gender["Female"]
age_gender.loc["Total"] = age_gender.sum()

data = create_groups(data,"service_years",5)
service_gender = pd.pivot_table(data,index="service_years_group",columns="GenderCode",values="Code",aggfunc="count",fill_value=0)
service_gender = service_gender.rename(columns={1: "Male",2: "Female"})
service_gender["Total"] = service_gender["Male"] +service_gender["Female"]
service_gender.loc["total"]=service_gender.sum()

average_age_employee=data["age"].mean()
print(average_age_employee)

average_service_years=data["service_years"].mean()
print(average_service_years)

average_wage_employee=data["wage"].mean()
print(average_wage_employee)

average_retired_age=data_retirement["age"].mean()
print(average_retired_age)


age_wage = pd.pivot_table(data,index="service_years_group",columns="GenderCode",values="wage",aggfunc="mean",fill_value=0)
age_wage = age_wage.rename(columns={1: "Male",2: "Female"})
age_wage["average"] = data.groupby("service_years_group")["wage"].mean()
age_wage.loc["Average"] = age_wage.mean()



age_liability_emplyee=pd.pivot_table(data,index="age_group",columns="GenderCode",values="accrued_liabilities",aggfunc="sum",fill_value=0)
age_liability_emplyee=age_liability_emplyee.rename(columns={1: "Male",2: "Female"})
age_liability_emplyee["sum_liabilites"] = data.groupby("age_group")["accrued_liabilities"].sum()
age_liability_emplyee.loc["sum_liability"]=age_liability_emplyee.sum()


age_liability_before_retirement=pd.pivot_table(data,index="age_group",columns="GenderCode",values="death_liability_before_retirement",aggfunc="sum",fill_value=0)
age_liability_before_retirement=age_liability_before_retirement.rename(columns={1: "Male",2: "Female"})
age_liability_before_retirement["sum_liabilites"] = data.groupby("age_group")["death_liability_before_retirement"].sum()
age_liability_before_retirement.loc["sum_liability"]=age_liability_before_retirement.sum()


data_retirement=create_groups(data_retirement,"age",5)
age_liability_retirement=pd.pivot_table(data_retirement,index="age_group",columns="GenderCode",values="liabilies",aggfunc="sum",fill_value=0)
age_liability_retirement=age_liability_retirement.rename(columns={1: "Male",2: "Female"})
age_liability_retirement["sum_liabilites"] = data_retirement.groupby("age_group")["liabilies"].sum()
age_liability_retirement.loc["sum_liability"]=age_liability_retirement.sum()
age_anniuity_retirement=pd.pivot_table(data_retirement,index="age_group",columns="GenderCode",values="anniuity",aggfunc="mean",fill_value=0)
age_anniuity_retirement=age_anniuity_retirement.rename(columns={1: "Male",2: "Female"})
age_anniuity_retirement["average"]=data_retirement.groupby("age_group")["anniuity"].mean()
age_anniuity_retirement.loc["average"]=age_anniuity_retirement.mean()
age_gender_retirement= pd.pivot_table(data_retirement,index="age_group",columns="GenderCode",values="age",aggfunc="count",fill_value=0)
age_gender_retirement= age_gender_retirement.rename(columns={2: "Female",1: "Male"})
age_gender_retirement["Total"] = age_gender_retirement["Male"] + age_gender_retirement["Female"]
age_gender_retirement.loc["Total"] = age_gender.sum()


data_survivor=create_groups(data_survivor,"age",5)
age_gender_survivor= pd.pivot_table(data_survivor,index="age_group",columns="GenderCode",values="age",aggfunc="count",fill_value=0)
age_gender_survivor=age_gender_survivor.rename(columns={"مرد" : "Male","زن" :"Female"})
age_gender_survivor["Total"] = age_gender_survivor["Male"] + age_gender_survivor["Female"]
age_gender_survivor.loc["Total"] = age_gender_survivor.sum()

age_liability_survivor=pd.pivot_table(data_survivor,index="age_group",columns="GenderCode",values="liabilies",aggfunc="sum",fill_value=0)
age_liability_survivor=age_liability_survivor.rename(columns={"مرد" : "Male","زن" :"Female"})
age_liability_survivor["sum_liabilites"] = data_survivor.groupby("age_group")["liabilies"].sum()
age_liability_survivor.loc["sum_liability"]=age_liability_survivor.sum()
age_annuity_survivor=pd.pivot_table(data_survivor,index="age_group",columns="GenderCode",values="anniuity",aggfunc="mean",fill_value=0)
age_annuity_survivor=age_annuity_survivor.rename(columns={"مرد" : "Male","زن" :"Female"})
age_annuity_survivor["average"]=data_survivor.groupby("age_group")["anniuity"].mean()
age_annuity_survivor.loc["average"]=age_annuity_survivor.mean()

active_chart = age_liability_emplyee.reset_index()[["age_group", "Male", "Female"]].copy()
output_file = "output/actuarial_results.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    

    age_wage.to_excel(writer, sheet_name="age_wage", index=True)

    age_gender.to_excel(writer, sheet_name="age_gender", index=True)
    service_gender.to_excel(writer, sheet_name="service_gender", index=True)
    age_wage.to_excel(writer, sheet_name="age_wage", index=True)
    age_liability_emplyee.to_excel(writer, sheet_name="age_liability_emplyee", index=True)
    age_liability_before_retirement.to_excel(writer, sheet_name="age_liability_before_retirement", index=True)
    age_gender_retirement.to_excel(writer, sheet_name="age_gender_retirement", index=True)
    age_anniuity_retirement.to_excel(writer, sheet_name="age_anniuity_retirementge", index=True)
    age_liability_retirement.to_excel(writer, sheet_name="seage_liability_retirement", index=True)
    age_gender_survivor.to_excel(writer, sheet_name="age_gender_survivor", index=True)
    age_annuity_survivor.to_excel(writer, sheet_name="age_annuity_survivore", index=True)
    age_liability_survivor.to_excel(writer, sheet_name="age_liability_survivor", index=True)










######################################################chart#######################################################
active_chart["status"] = "Active"
active_chart_death_liability = age_liability_before_retirement.reset_index()[["age_group", "Male", "Female"]].copy()
active_chart_death_liability["status"] = "death_before_retirment"

retired_chart = age_liability_retirement.reset_index()[["age_group", "Male", "Female"]].copy()

retired_chart["status"] = "retired"

survivor_chart = age_liability_survivor.reset_index()[["age_group", "Male", "Female"]].copy()

survivor_chart["status"] = "survivor"


data_chart=pd.concat([active_chart,active_chart_death_liability,retired_chart,survivor_chart],ignore_index=True)
data_chart = data_chart[data_chart["age_group"] != "sum_liability"].copy()
data_chart["Male_million"] = data_chart["Male"] / 1_000_000
data_chart["Female_million"] = data_chart["Female"] / 1_000_000




import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------
# Prepare data
# --------------------------------------------------

plot_data = data_chart[
    data_chart["age_group"] != "sum_liability"
].copy()

age_order = [
    "5-9", "10-14", "15-19", "20-24",
    "25-29", "30-34", "35-39", "40-44",
    "45-49", "50-54", "55-59", "60-64",
    "65-69", "70-74", "75-79", "80-84",
    "85-89", "90-94", "95-99"
]

plot_data["age_group"] = pd.Categorical(
    plot_data["age_group"],
    categories=age_order,
    ordered=True
)

# Convert to million Rial
plot_data["Total_million"] = (
    plot_data["Male"] + plot_data["Female"]
) / 1_000_000

plot_data["Male_million"] = (
    plot_data["Male"] / 1_000_000
)

plot_data["Female_million"] = (
    plot_data["Female"] / 1_000_000
)

# --------------------------------------------------
# Create matrices
# --------------------------------------------------

total_surface = plot_data.pivot(
    index="status",
    columns="age_group",
    values="Total_million"
).reindex(columns=age_order)

male_surface = plot_data.pivot(
    index="status",
    columns="age_group",
    values="Male_million"
).reindex(columns=age_order)

female_surface = plot_data.pivot(
    index="status",
    columns="age_group",
    values="Female_million"
).reindex(columns=age_order)

# Male/Female difference
difference_surface = male_surface - female_surface

# Coordinates
X, Y = np.meshgrid(
    np.arange(len(age_order)),
    np.arange(len(total_surface.index))
)

# --------------------------------------------------
# Four 3D surfaces
# --------------------------------------------------

fig, axes = plt.subplots(
    2,
    2,
    figsize=(13, 9),
    subplot_kw={"projection": "3d"}
)
status_labels = {
    "Active": "Active",
    "death_before_retirment": "Disability",
    "retired": "Retired",
    "survivor": "Survivor"
}


surfaces = [
    (axes[0, 0], total_surface, "Total Liability", "viridis"),
    (axes[0, 1], male_surface, "Male Liability", "plasma"),
    (axes[1, 0], female_surface, "Female Liability", "cividis"),
    (axes[1, 1], difference_surface, "Male − Female Liability", "coolwarm")
]

for ax, data, title, cmap in surfaces:

    Z = data.values

    surface = ax.plot_surface(
        X,
        Y,
        Z,
        cmap=cmap,
        edgecolor="black",
        linewidth=0.25,
        alpha=0.9
    )

    ax.set_title(
        title,
        fontsize=12,
        pad=18
    )

    ax.set_xlabel(
        "Age Group",
        fontsize=9,
        labelpad=10
    )

    ax.set_ylabel(
        "Category",
        fontsize=9,
        labelpad=10
    )

    ax.set_zlabel(
        "Million Rial",
        fontsize=9,
        labelpad=10
    )

    # Show every second age label
    age_positions = np.arange(len(age_order))

    ax.set_xticks(age_positions[::2])

    ax.set_xticklabels(
        age_order[::2],
        rotation=45,
        ha="right",
        fontsize=7
    )

    ax.set_yticks(
        np.arange(len(data.index))
    )
    

    ax.set_yticklabels(
    [status_labels.get(status, status) for status in data.index],
    fontsize=7
)
   

    ax.tick_params(
        axis="z",
        labelsize=7
    )

    ax.view_init(
        elev=25,
        azim=-120
    )

    fig.colorbar(
        surface,
        ax=ax,
        shrink=0.50,
        pad=0.08
    )


fig.suptitle(
    "Actuarial Liability Analysis",
    fontsize=16,
    fontweight="bold",
    y=0.98
)

plt.subplots_adjust(
    left=0.02,
    right=0.96,
    bottom=0.06,
    top=0.90,
    wspace=0.12,
    hspace=0.18
)
plt.savefig("output/actuarial_liability_3d.png",dpi=300,bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(
    2,
    2,
    figsize=(13, 9),
    subplot_kw={"projection": "3d"}
)

statuses = [
    "Active",
    "death_before_retirment",
    "retired",
    "survivor"
]

status_labels = {
    "Active": "Active",
    "death_before_retirment": "Disability",
    "retired": "Retired",
    "survivor": "Survivor"
}

charts = [
    (axes[0, 0], "Total Liability", "Total_million"),
    (axes[0, 1], "Male Liability", "Male_million"),
    (axes[1, 0], "Female Liability", "Female_million")
]

# --------------------------------------------------
# First 3 charts
# --------------------------------------------------

for ax, title, value_column in charts:

    for y, status in enumerate(statuses):

        status_data = plot_data[
            plot_data["status"] == status
        ]

        for x, age in enumerate(age_order):

            row = status_data[
                status_data["age_group"] == age
            ]

            if row.empty:
                continue

            value = row[value_column].iloc[0]

            ax.bar3d(
                x - 0.2,
                y,
                0,
                0.4,
                0.4,
                value,
                alpha=0.85
            )

    ax.set_title(
        title,
        fontsize=12,
        pad=18
    )

    ax.set_xlabel(
        "Age Group",
        fontsize=8,
        labelpad=10
    )

    ax.set_ylabel(
        "Liability Category",
        fontsize=8,
        labelpad=10
    )

    ax.set_zlabel(
        "Million Rial",
        fontsize=8,
        labelpad=10
    )

    ax.set_xticks(
        np.arange(len(age_order))[::2]
    )

    ax.set_xticklabels(
        age_order[::2],
        rotation=45,
        ha="right",
        fontsize=7
    )

    ax.set_yticks(
        np.arange(len(statuses))
    )

    ax.set_yticklabels(
        [status_labels[s] for s in statuses],
        fontsize=7
    )

    ax.view_init(
        elev=25,
        azim=-120
    )


# --------------------------------------------------
# Fourth chart: Male - Female
# --------------------------------------------------

ax = axes[1, 1]

for y, status in enumerate(statuses):

    status_data = plot_data[
        plot_data["status"] == status
    ]

    for x, age in enumerate(age_order):

        row = status_data[
            status_data["age_group"] == age
        ]

        if row.empty:
            continue

        male = row["Male_million"].iloc[0]
        female = row["Female_million"].iloc[0]

        difference = male - female

        ax.bar3d(
            x - 0.2,
            y,
            0,
            0.4,
            0.4,
            difference,
            alpha=0.85
        )

ax.set_title(
    "Male − Female Liability",
    fontsize=12,
    pad=18
)

ax.set_xlabel(
    "Age Group",
    fontsize=8,
    labelpad=10
)

ax.set_ylabel(
    "Liability Category",
    fontsize=8,
    labelpad=10
)

ax.set_zlabel(
    "Million Rial",
    fontsize=8,
    labelpad=10
)

ax.set_xticks(
    np.arange(len(age_order))[::2]
)

ax.set_xticklabels(
    age_order[::2],
    rotation=45,
    ha="right",
    fontsize=7
)

ax.set_yticks(
    np.arange(len(statuses))
)

ax.set_yticklabels(
    [status_labels[s] for s in statuses],
    fontsize=7
)

ax.view_init(
    elev=25,
    azim=-120
)


# --------------------------------------------------
# Overall title
# --------------------------------------------------

fig.suptitle(
    "Actuarial Liability Analysis",
    fontsize=17,
    fontweight="bold"
)

plt.subplots_adjust(
    left=0.03,
    right=0.97,
    bottom=0.07,
    top=0.91,
    wspace=0.10,
    hspace=0.15
)

# Save for Word / GitHub
plt.savefig("output/actuarial_liability_3d_bars.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
#####################################################################################################################
##################################################vilion chart#######################################################
####################################################################################################################
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
from current_employees import data
active_v = data[["age", "GenderCode", "accrued_liabilities"]].copy()
active_v["liability"] = active_v["accrued_liabilities"]
disability_v = data[["age", "GenderCode", "death_liability_before_retirement"]].copy()
disability_v["liability"] = (disability_v["death_liability_before_retirement"])
retired_v = data_retirement[["age", "GenderCode", "liabilies"]].copy()
retired_v["liability"] = retired_v["liabilies"]
survivor_v = data_survivor[["age", "GenderCode", "liabilies"]].copy()
survivor_v["liability"] = survivor_v["liabilies"]
for data in [active_v,disability_v,retired_v,survivor_v]:
    data["liability_million"] = (data["liability"] / 1_000_000)


active_v["Gender"] = active_v["GenderCode"].map({1: "Male",2: "Female"})
disability_v["Gender"] = disability_v["GenderCode"].map({1: "Male",2: "Female"})
retired_v["Gender"] = retired_v["GenderCode"].map({1: "Male",2: "Female"})
survivor_v["Gender"] = survivor_v["GenderCode"].map({"مرد": "Male","زن": "Female"})

import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Create 2 × 2 figure
# -----------------------------

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 9)
)


charts = [
    (axes[0, 0], active_v, "Active"),
    (axes[0, 1], disability_v, "Disability"),
    (axes[1, 0], retired_v, "Retired"),
    (axes[1, 1], survivor_v, "Survivor")
]


# -----------------------------
# Create violin plots
# -----------------------------

for ax, data, title in charts:

    sns.violinplot(
        data=data,
        x="Gender",
        y="liability_million",
        inner="box",
        cut=0,
        ax=ax
    )

    ax.set_title(
        title,
        fontsize=13,
        fontweight="bold",
        pad=10
    )

    ax.set_xlabel(
        "Gender",
        fontsize=9
    )

    ax.set_ylabel(
        "Liability (Million Rial)",
        fontsize=9
    )

    ax.tick_params(
        axis="both",
        labelsize=8
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )


# -----------------------------
# Overall title
# -----------------------------

fig.suptitle(
    "Individual Actuarial Liability Distribution by Category and Gender",
    fontsize=16,
    fontweight="bold"
)


plt.tight_layout(
    rect=[0, 0, 1, 0.95]
)


# -----------------------------
# Save
# -----------------------------

plt.savefig("output/individual_liability_violin_4_categories.png",dpi=300,bbox_inches="tight")


plt.show()

