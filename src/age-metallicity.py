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

vdb = pd.read_csv("data/vandenBerg_table2.csv")
kdb = pd.read_csv("data/Krause21.csv")

plt.figure(figsize=(8,6))
plt.scatter(vdb["FeH"], vdb["Age"], label="VandenBerg 2013")
plt.scatter(kdb["FeH"], kdb["Age"], label="Krause 2021")
plt.xlabel("Metallicity [Fe/H]")
plt.ylabel("Age (Gyr)")
plt.title("Age–Metallicity Relation of Milky Way GCs")
plt.legend()
plt.savefig("results/age_metallicity.png")
plt.show()