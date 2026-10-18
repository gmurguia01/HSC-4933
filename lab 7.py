#############################
# Darcy Warms               #
# Lab 7 : Linear Regression #
# HSC 4933                  #
# 10/8/26                   #
#############################

# Imports

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Prompt user for dataset


print("Available datasets: ")
print("1. birthwt.csv")
print("2. places_2025.csv")

dataset_choice = input("Please enter your dataset : ")

#Deleted unecessary code
if dataset_choice == "1" or dataset_choice == "birthwt.csv":
    csv_path = "birthwt.csv"

elif dataset_choice == "2" or dataset_choice == "places_2025.csv":
    csv_path = "places_2025.csv"

else:
    print("Invalid choice. Please run the program again.")
    raise SystemExit

# Load .csv

df = pd.read_csv(csv_path, thousands=",")


# Convert headings to snake case
#made column name easier to understand
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# List available column names

print("Available columns: ")
print(df.columns.tolist())


# Prompt user to name X and Y variables
#made the code more user friendly to remove user error
x_col = input("Please name your X variable: ").strip().lower()
y_col = input("Please name your Y variable: ").strip().lower()

#validates column name

if x_col not in df.columns or y_col not in df.columns:
    print("Invalid column name. Please run the program again.")
    raise SystemExit

# Drop rows with missing values
#prevents the removal of rows with values from being removed
data = df[[x_col, y_col]].copy()

data[x_col] = pd.to_numeric(data[x_col], errors="coerce")
data[y_col] = pd.to_numeric(data[y_col], errors="coerce")

data = data.dropna()

#range of X


min_value = float(input("Enter the minimum X value: "))
max_value = float(input("Enter the maximum X value: "))


data = data[
    (data[x_col] >= min_value) &
    (data[x_col] <= max_value)
]


# Create scatterplot

fig1, ax1 = plt.subplots(figsize=(8, 6))

ax1.scatter(data[x_col], data[y_col], alpha=0.6, edgecolor="k", linewidth=0.3)
ax1.set_xlabel(x_col)
ax1.set_ylabel(y_col)
ax1.set_title(f"{y_col} vs {x_col} (n = {len(data)})")
ax1.grid(alpha=0.3)

fig1.tight_layout()

# Ask user if they want to save file

save_scatter = input("Would you like to save this scatterplot? (y/n): ")
if save_scatter == "y":
    scatter_file = input("Please enter a file name.")
    fig1.savefig(scatter_file, dpi=300)
    print(f"Saved scatterplot to {scatter_file}")

# Perform linear regression

X = sm.add_constant(data[x_col])
model = sm.OLS(data[y_col], X).fit()

# Print summary

print("OLS Regression Summary: ")
print(model.summary())
# Print values needed for trends document
print("Intercept (β0):", model.params["const"])
print("Slope (β1):", model.params[x_col])
print("R²:", model.rsquared)

# Create new scatterplot with regression

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.scatter(data[x_col], data[y_col], alpha=0.6, edgecolor="black")

# Create the regression line

x_line = np.linspace(data[x_col].min(), data[x_col].max(), 100)
y_line = model.params["const"] + model.params[x_col] * x_line

# creates second plot with regression

ax2.plot(
    x_line,
    y_line,
    color="crimson",
    linewidth=2,
    label=f"OLS line (R-squared = {model.rsquared:.3f})"
)
ax2.set_xlabel(x_col)
ax2.set_ylabel(y_col)
ax2.set_title(f"{y_col} vs {x_col} with OLS line (n = {len(data)})")
ax2.grid(alpha=0.3)
ax2.legend()
fig2.tight_layout()

# Ask user if they want to save scatterplot with regression line

save_scatter = input("Would you like to save this scatterplot with OLS regression line? (y/n): ")
if save_scatter == "y":
    scatter_file = input("Please enter a file name.")
    fig2.savefig(scatter_file, dpi=300)
    print(f"Saved scatterplot to {scatter_file}")



# Second Y variable

second_y = input("Enter a second Y variable: ").strip().lower()

# Check if the column exists

if second_y not in df.columns:
    print("Invalid column name.")
else:
    #comparison graph

    fig3, ax3 = plt.subplots(figsize=(8, 6))

    #Y variable

    ax3.scatter(
        data[x_col],
        data[y_col],
        color="blue",
        label=y_col
    )

    #second Y axis

    ax4 = ax3.twinx()

    #second Y variable

    ax4.scatter(
        data[x_col],
        df.loc[data.index, second_y],
        color="orange",
        label=second_y
    )

    #title

    ax3.set_xlabel(x_col)
    ax3.set_ylabel(y_col, color="blue")
    ax4.set_ylabel(second_y, color="orange")

    ax3.set_title(f"{y_col} and {second_y} vs {x_col}")

    #legends

    ax3.legend(loc="upper left")
    ax4.legend(loc="upper right")

    #Diplsay

    fig3.tight_layout()
    plt.show()


