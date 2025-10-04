"""
This script plots the Age–Metallicity relation for Milky Way
globular clusters using VandenBerg (2013) and Krause (2021) data.

Globular clusters that formed inside the Milky Way are expected to
follow an age–metallicity trend: older clusters tend to be metal-poor,
while younger clusters are more metal-rich, reflecting the chemical
evolution of our Galaxy. Outliers from this relation are interesting
because they may not share the same enrichment history. Such clusters
are potential accreted populations, likely brought in by past mergers
with dwarf galaxies.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

vdb = pd.read_csv("data/vandenBerg_table2.csv")

# filter rows without age or metallicity
vdb = vdb.dropna(subset=["Age", "FeH"])

# fit linear regression
x = vdb["FeH"].values.reshape(-1, 1)
y = vdb["Age"].values
model = LinearRegression().fit(x, y)
y_pred = model.predict(x)

# Compute residuals
vdb["Residual"] = y - y_pred

# Calculate IQR
q1 = vdb["Residual"].quantile(0.25)
q3 = vdb["Residual"].quantile(0.75)
iqr = q3 - q1

# Define bounds using 1.5 × IQR rule
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Flag outliers
outliers = vdb[(vdb["Residual"] < lower_bound) | (vdb["Residual"] > upper_bound)]
inliers  = vdb[(vdb["Residual"] >= lower_bound) & (vdb["Residual"] <= upper_bound)]

# Plot
plt.figure(figsize=(8,6))
plt.scatter(inliers["FeH"], inliers["Age"], c="blue", alpha=0.7, label="Inliers")
plt.scatter(outliers["FeH"], outliers["Age"], c="red", s=80, label="Outliers")
plt.plot(vdb["FeH"], y_pred, c="black", label="Fit")

# Labels for outliers
for _, row in outliers.iterrows():
    plt.text(row["FeH"], row["Age"]+0.2, row["Name"], fontsize=8, ha="center")

plt.xlabel("Metallicity [Fe/H]")
plt.ylabel("Age (Gyr)")
plt.title("Age–Metallicity Relation with Outliers")
plt.legend()
plt.savefig("results/age_metallicity_vandenberg.png")
plt.show()