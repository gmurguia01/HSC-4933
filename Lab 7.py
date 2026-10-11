##########################################
# LAB # 7 |    Birthweight and places    #
#----------------------------------------#
# Gabriel Murguia |   gmurguia@usf.edu   #
#---------------10/11/2026----------------#
#       creates scatterplot and perfoms  #
# liner regression for a given dataset,  #
# saving outputs as png files and        #
#      returning regressions stats       #
##########################################

#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import re
import os

#load databases
birthwt = pd.read_csv("birthwt.csv")
places = pd.read_csv("places_2025.csv")

#Column names birthweight
new_columns = []
for column in birthwt.columns:
    column = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", column)
    column = column.strip().lower()
    column = re.sub(r"[^a-z0-9]+", "_", column)
    column = column.strip("_")
    new_columns.append(column)

birthwt.columns = new_columns

#column names places
new_columns = []
for column in places.columns:
    column = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", column)
    column = column.strip().lower()
    column = re.sub(r"[^a-z0-9]+", "_", column)
    column = column.strip("_")
    new_columns.append(column)

places.columns = new_columns

#show available columns
print("birthweight columns:")
print(birthwt.columns.tolist())

print("places columns:")
print(places.columns.tolist())

#folders
os.makedirs("figures/birthweight_figures", exist_ok=True)

os.makedirs(
    "figures/cdc_places_figures/housing_insecurity_vs_total_population",
    exist_ok=True,
)
os.makedirs(
    "figures/cdc_places_figures/obesity_vs_mental_health_disorders",
    exist_ok=True
)

#plot functions
def make_plots(df, x_column, y_column, fig1, fig2, folder):
    df = df.dropna(subset=[x_column, y_column]).copy()
    df[x_column] = pd.to_numeric(df[x_column], errors="coerce")
    df[y_column] = pd.to_numeric(df[y_column], errors="coerce")
    df = df.dropna(subset=[x_column, y_column])
    if len(df) < 2:
        print("Not Enough Data")
        return
    x = df[x_column]
    y = df[y_column]

    plt.scatter(x, y)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title("Scatterplot w/o regression")

    answer = input("Save " + fig1 + "? (y/n): ").lower()
    if answer == "y":
        file_path = folder + "/" + fig1 + ".png"
        plt.savefig(file_path)
        print("Saved to:", file_path)

    plt.show()
    plt.close()

    x_constant = sm.add_constant(x)
    model = sm.OLS(y, x_constant).fit()
    print("\nOLS Regression Results:")
    print(model.summary())

    sorted_df = df.sort_values(x_column)
    sorted_x = sorted_df[x_column]
    sorted_x_constant = sm.add_constant(sorted_x)

    plt.scatter(x, y, label="Observed data")

    plt.plot(
        sorted_x,
        model.predict(sorted_x_constant),
        color="red",
        label="OLS regression line"
     )

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title("Scatterplot With OLS Regression")
    plt.legend()

    answer = input("Save " + fig2 + "? (y/n): ").lower()
    if answer == "y":
        file_path = folder + "/" + fig2 + ".png"
        plt.savefig(file_path)
        print("Saved to:", file_path)
    plt.show()
    plt.close()
#create figures
make_plots(
    birthwt,
    "lwt",
    "bwt",
    "fig_1",
    "fig_2",
    "figures/birthweight_figures"
)

#Fig 3-4
make_plots(
    places,
    "total_population",
    "housinsecu_crude_prev",
    "fig_3",
    "fig_4",
    "figures/cdc_places_figures/housing_insecurity_vs_total_population"
)

#Fig 5-6
make_plots(
    places,
    "obesity_crude_prev",
    "mhlth_crude_prev",
    "fig_5",
    "fig_6",
    "figures/cdc_places_figures/obesity_vs_mental_health_disorders"
)
