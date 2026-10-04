###################################################
# Data set conversion #          gmurguia@usf.edu #
###################################################
# (c) Gabe, Murguia, 2026 # HSC4933 # Week 5, SUN #
# Conversting data set to Excel                   #
###################################################




# import pandas
import pandas as pd

df = pd.read_csv("Maternal Health Risk Data Set.csv")

#remove duplicated files
df = df.loc[:, ~df.columns.duplicated()]

df.to_excel("Maternal Health Risk Data.xlsx", index=False)

#print that the file was created
print("Excel created")
