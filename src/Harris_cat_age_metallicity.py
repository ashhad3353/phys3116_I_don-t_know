import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
harris_p1=pd.read_csv("data/HarrisPartI.csv")
harris_p2=pd.read_csv("data/HarrisPartIII.csv")
harris_cat=pd.merge(harris_p1,harris_p2,on='ID',how='inner')# Merging the 2 parts of the catalog into 1 dataframe by combining all of the columns into 1 set 
vbd=pd.read_csv("data/vandenBerg_table2.csv")
harris_cat_merged=pd.merge(harris_cat,vbd,on='ID',how='inner')# Merging the Harris catalog with VandenBerg catalog into 1 dataframe by combining all of the columns into 1 set.
#Plotting the radial velocity from Harris catalog vs the metallicity from VandenBerg catalog
 plt.scatter(vbd["FeH"],harris_cat["v_LSR"],label="Harris Catalog")
plt.xlabel("Metallicity [Fe/H]")
plt.ylabel("Radial Velocity (km/s)")
plt.title("Radial Velocity vs Metallicity [Fe/H]")
plt.savefig("results/RadialVelocity_vs_Metallicity.png")
plt.show()
# Plot is currently not working, different column sizes in the 2 dataframes. Will try and work on a fix later. 
