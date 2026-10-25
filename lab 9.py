##########################################
# LAB # 9 |    Birthweight and places    #
#----------------------------------------#
# Gabriel Murguia |   gmurguia@usf.edu   #
#---------------10/25/2026---------------#
# creates count and logistic regression  #
# liner regression for a given dataset,  #
#Deleting columns returning snakecase    #
#      returning regressions stats       #
##########################################

import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import confusion_matrix
from statsmodels.stats.outliers_influence import variance_inflation_factor
import re

#Have user input data set

print("Available datasets:")
print("1. birthwt.csv")
print("2. places_2025.csv")

choice = input("Choose a dataset (1 or 2): ")

if choice == "1":
    file_name = "birthwt.csv"
elif choice == "2":
    file_name = "places_2025.csv"
else:
    print("Invalid choice")
    exit()

#Data set

try:
    data = pd.read_csv(file_name)
except FileNotFoundError:
    print("File not found")
    exit()

#snake_case columns


# Clean column names

new_columns = []

for column in data.columns:
    column = str(column).strip()
    column = column.lower()
    column = column.replace(" ", "_")

    new_columns.append(column)

# Print the results to check them
print("Original columns:", list(data.columns))
print("Cleaned columns:", new_columns)

# Replace old column names
data.columns = new_columns


#display columns

print("\nAvailable columns:")
for column in data.columns:
    print(column)

#have user input variables
predictor_input = input (
    "\nEnter predictor column name: "
)
predictors = predictor_input.split(",")
predictors = [column.strip().lower() for column in predictors]
response = input (
    "\nEnter response column name: "
).strip().lower()

#ensuring the columns exist
selected_columns = predictors + [response]
for column in selected_columns:
    if column not in data.columns:
        print("Column not found", column)
        print("Please try again")
        exit()

#have user choose regression model
print("\n choose regression model:")
print("1. Logistic regression")
print("2. Poisson regression")
model_choice = input("Enter 1 or 2: ")
if model_choice not in ["1", "2"]:
    print("Invalid choice")
    exit()

#keep selected columns
model_data = data[selected_columns].copy()
for column in selected_columns:
    model_data[column] = pd.to_numeric(
        model_data[column], errors="coerce"
    )

#removing missing values
model_data = model_data.dropna()
print("\nNumber of rows used:", len(model_data))
X = model_data[predictors]
y = model_data[response]
X = sm.add_constant(X)

#regression model
if model_choice == "1":
    if not set(y.unique()).issubset({0, 1}):
        print("Error")
        exit()

    if y.nunique() !=2:
        print("Error")
        exit()

    model = sm.Logit(y, X)
    results = model.fit()
    print("\nLOGISTIC RESULTS")
    print(results.summary())
    probabilities = results.predict(X)
    predictions = (probabilities >= 0.5).astype(int)
    matrix = confusion_matrix(
        y, predictions, labels=[0, 1]
    )

    print("\nConfusion Matrix:")
    print("Rows = Actual (0, 1)")
    print("Columns = Predicted (0, 1)")
    print(matrix)

else:
    if (y < 0).any():
        print("Error")
        exit()
    if (y % 1 != 0).any():
        print(
            "Error",
        )
        print(
            "Poisson regression needs count data"
        )
        print(
            "Ensure Poisson is appropriate"
        )

# fit model
model = sm.GLM(
    y, X, family=sm.families.Poisson()
)
results = model.fit()

#show results
print("\nPOISSON RESULTS")
print(results.summary())
vif_data = pd.DataFrame()
vif_data["variable"] = predictors
vif_data["VIF"] = [
    variance_inflation_factor(
        X.drop(columns="const").values, i
    )
    for i in range(len(predictors))
]
#print inflaction factor
print("\nVariance inflation factor (VIF):")
print(vif_data)

#save output

save_choice = input(
    "\n Save output file to .txt? (Y/N): "
).strip().lower()

if save_choice == "y":
    output_name = input(
        "\nEnter output file name: "
    ).strip()
    if output_name == "":
        output_name = "regression_results"
    if not output_name.lower().endswith(".txt"):
        output_name = output_name + ".txt"
    with open(output_name, "w") as output_file:
        output_file.write("REGRESSION RESULTS\n\n")
        output_file.write(results.summary().as_text())
        if model_choice == "1":
            output_file.write("\n\nCONFUSION MATRIX\n")
            output_file.write(
                "Rows = Actual (0, 1), Columns = Predicted (0, 1)\n"
            )
            output_file.write(str(matrix))
        else:
            output_file.write("\n\nVARIANCE INFLACTION FACTOR\n")
            output_file.write(vif_data.to_string(index=False))
    print ("Results saved to", output_name)
else:
    print("Error")
