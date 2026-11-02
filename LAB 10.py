









import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
from statsmodels.duration.hazard_regression import PHReg
import os

#Folder
if not os.path.exists("figures"):
    os.mkdir("figures")

#readmission dataset
data = pd.read_csv("km_logrank_readmission.csv")
groups = data["treatment_group"].unique()
plt.figure(figsize=(8, 5))
for group in groups:
    group_data = data[data["treatment_group"] == group]
    time = group_data["time_days"].values
    events = group_data["readmitted"].values
    survival = 1.0
    x_values = [0]
    y_values = [1.0]
    event_times = sorted(set(time[events ==1]))
    for t in event_times:
        #patients being followed
        patients_at_risk = sum(time >= t)
        readmissions = sum((time == t) & (events ==1))
        survival = survival * (
            1 - readmissions / patients_at_risk
        )
        x_values.append(t)
        y_values.append(survival)

    #kaplan-meier curve
    plt.step(
        x_values,
        y_values,
        where="post",
        label=group
    )
#log rank test

time = data["time_days"].values
events = data["readmitted"].values
group = data["treatment_group"].values
first_group = groups[0]
observed_minus_expected = 0
variance = 0

#finding events
event_times = sorted(set(time[events ==1]))
for t in event_times:
    group1_at_risk = sum(
        (time >= t) & (group == first_group)
    )
    group2_at_risk = sum(
        (time >= t) & (group != first_group)
    )
    #events in group count
    group1_events = sum(
        (time >= t) & (events == 1) & (group == first_group)
    )
    group2_events = sum(
        (time >= t) & (events == 1) & (group != first_group)
    )
    # total patients and events
    total_at_risk = group1_at_risk + group2_at_risk
    total_events = group1_events + group2_events
    expected_events = (
         total_events * group1_at_risk / total_at_risk
    )
    #observed minus expected events
    observed_minus_expected = (
        observed_minus_expected
        + group1_events
        -expected_events
    )
    # variance
    if total_at_risk > 1:
        variance = variance + (
            group1_at_risk
            * group2_at_risk
            * total_events
            * (total_at_risk - total_events)
            / (
                total_at_risk ** 2
                * (total_at_risk - 1)
            )
        )
#chi-square statistic
chi_square = observed_minus_expected ** 2 / variance

# p-value
p_value = chi2.sf(chi_square, 1)

#graph
plt.title("Kaplan-Meier Readmission-Free Survival")
plt.xlabel("Days After Hospital Discharge")
plt.ylabel("Probability of No Readmission")

plt.xlim(0, 180)
plt.ylim(0, 1.02)

plt.legend()
plt.grid()

# Display results
plt.text(
    10,
    0.10,
    "Chi-square = " + str(round(chi_square, 2))
    + "\nP-value = " + str(round(p_value, 8))
)

# Save and display the graph
plt.savefig("figures/kaplan_meier_logrank.png")
plt.show()

#results
print("Log-Rank Test Results")
print("Chi-square:", chi_square)
print("P-value:", p_value)



#COX PROPORTIONAL HAZARDS


cox_data = pd.read_csv(
    "cox_ph_heart_failure_survival.csv"
)

# Convert sex to numbers
cox_data["sex"] = cox_data["sex"].str.strip().str.lower()

cox_data["sex"] = cox_data["sex"].map({
    "female": 0,
    "male": 1
})

predictors = [
    "age",
    "sex",
    "bmi",
    "systolic_bp",
    "ejection_fraction",
    "diabetes",
    "smoker",
    "chronic_kidney_disease",
    "nyha_class",
    "beta_blocker"
]


cox_data = cox_data[
    ["time_months", "death"] + predictors
]

# Remove rows
cox_data = cox_data.dropna()



cox_model = PHReg(
    cox_data["time_months"],
    cox_data[predictors],
    status=cox_data["death"]
)

# Fit the model
cox_results = cox_model.fit()

# Print the model results
print("\nCox Proportional Hazards Results")
print(cox_results.summary())



#Cox hazard graph

# Calculate hazard ratios
hazard_ratios = np.exp(cox_results.params)

# Calculate confidence intervals
confidence_intervals = np.exp(
    cox_results.conf_int()
)

# Create the graph
plt.figure(figsize=(8, 6))
y_positions = range(len(predictors))

plt.errorbar(
    hazard_ratios,
    y_positions,
    xerr=[
        hazard_ratios - confidence_intervals[:, 0],
        confidence_intervals[:, 1] - hazard_ratios
    ],
    fmt="o",
    capsize=3
)

plt.axvline(
    1,
    color="gray",
    linestyle="--"
)

plt.yticks(y_positions, predictors)

plt.xscale("log")

plt.xlabel("Hazard Ratio")
plt.title("Cox Model: Risk of All-Cause Death")

plt.grid(axis="x")

# Save and display the graph
plt.tight_layout()

plt.savefig(
    "figures/cox_ph_hazard_ratios.png"
)

plt.show()

print("Both figures were saved in the figures folder.")