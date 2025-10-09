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

plt.scatter(harris_cat_merged["L"],harris_cat_merged["v_LSR"], label="Harris Catalog")
plt.xlabel("Galactic Longitude (degrees)")
plt.ylabel("Line of sight velocity(km/s)")
plt.title('Galactic Longitude vs Line of sight velocity')
plt.savefig('Galactic Longitude vs Line of Sight velocity.png')
plt.show()


plt.scatter(harris_cat_merged["r_h"],harris_cat_merged["c"], label='Harris catalog')
plt.xlabel('half light radius (pc)')
plt.ylabel('concentration')
plt.savefig('half light radius vs concentration.png')
plt.show()





