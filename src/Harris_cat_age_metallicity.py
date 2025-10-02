import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
harris_p1=pd.read_csv("data/HarrisPartI.csv")
harris_p2=pd.read_csv("data/HarrisPartIII.csv")
harris_cat=pd.merge(harris_p1,harris_p2,on='ID',how='inner')# Merging the 2 parts of the catalog into 1 dataframe by combining all of the columns into 1 set 
vbd=pd.read_csv("data/vandenBerg_table2.csv")
vbd.rename(columns={"#NGC":"ID"},inplace=True)# Renaming the column "#NGC" to "ID" to match the Harris catalog column name "ID"
def add_NGC(s):
   return("NGC "+ s)
vbd["ID"]=vbd["ID"].apply(add_NGC)# Adding "NGC " to the front of each value in the "ID" column to match the Harris catalog format
harris_cat_merged=pd.merge(harris_cat,vbd,on='ID',how='inner')# Merging the Harris catalog with VandenBerg catalog into 1 dataframe by combining all matching columns into 1 set.
harris_cat_merged.to_csv("results/Harris_VandenBerg_merged.csv",index=False)# Saving the merged dataframe to a csv file in the results folder
#Plotting the radial velocity from Harris catalog vs the metallicity from VandenBerg catalog
plt.scatter(harris_cat_merged["FeH"],harris_cat_merged["v_LSR"],label="Harris Catalog")
plt.xlabel("Metallicity [Fe/H]")
plt.ylabel("Radial Velocity (km/s)")
plt.title("Radial Velocity vs Metallicity [Fe/H] of NGCs")
plt.savefig("results/RadialVelocity_vs_Metallicity.png")
plt.show()

# Plot L vs v_LSR to show rotation patterns/ non-rotating clusters 
# Plot sig_v vs r_h or rho_theta to show dispersion patterns. CLusters lying well of the main sequence of points might be interesting 
# Plot r_h vs c, large r_h and low c might be indicate accreted clusters

