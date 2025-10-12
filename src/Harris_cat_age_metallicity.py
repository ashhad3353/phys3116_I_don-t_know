#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
harris_p1=pd.read_csv("data/HarrisPartI.csv")
harris_p2=pd.read_csv("data/HarrisPartIII.csv")
harris_cat=pd.merge(harris_p1,harris_p2,on='ID',how='inner')# Merging the 2 parts of the catalog into 1 dataframe by combining all of the columns into 1 set 
vbd=pd.read_csv("data/vandenBerg_table2.csv")
vbd.rename(columns={"#NGC":"ID"},inplace=True)# Renaming the column "#NGC" to "ID" to match the Harris catalog column name "ID"
def add_NGC(s):
   return("NGC "+ s)
vbd["ID"]=vbd["ID"].apply(add_NGC)# Adding "NGC " to the front of each value in the "ID" column to match the Harris catalog format
harris_cat_merged=pd.merge(harris_cat,vbd,on='ID',how='inner')# Merging the Harris catalog with VandenBerg catalog into 1 dataframe by combining all matching columns into 1 set.
#Plotting the radial velocity from Harris catalog vs the metallicity from merged catalog
#%% 
plt.errorbar(harris_cat_merged["L"],harris_cat_merged["v_LSR"],
#Plotting Error in v_LSR
yerr=harris_cat_merged["v_r_e"], fmt='o', ecolor='black', elinewidth=1.5, capsize=1, label='Harris catalog')
plt.xlabel("Galactic Longitude (degrees)")
plt.ylabel("Line of sight velocity(km/s)")
plt.title('Galactic Longitude vs Line of sight velocity')
plt.savefig("results/Longitude_vs_velocity.png")
plt.grid(True)
plt.show()

#%%


#Plotting the half light radius from Harris catalog vs the concentration from merged catalog
plt.scatter(np.log10(harris_cat_merged["r_h"]),harris_cat_merged["c"],
## making a colour bar based on age
c=np.log10(harris_cat_merged["Age"]),marker='.')
cbar=plt.colorbar()
plt.xlabel('half light radius (pc)')
plt.ylabel('concentration')
plt.title('Half light radius vs Concentration')
plt.savefig("results/half_light_radius_vs_concentration.png")
cbar.set_label('Log 10 of Age(Gyr)')
plt.show()

# %%
#Just testing linear regression and outlier detection
slope, intercept,r ,p, std_err = stats.linregress(np.log10(harris_cat_merged["r_h"]),harris_cat_merged["c"])
c_fit = slope * np.log10(harris_cat_merged["r_h"]) + intercept
residuals = harris_cat_merged["c"] - c_fit
z= stats.zscore(residuals)
outliers = np.where(np.abs(z) > 2)[0] # Identifying outliers with z-score greater than 2

#2D KDE plot
xy=np.vstack([np.log10(harris_cat_merged["r_h"]),harris_cat_merged["c"]])
kde=stats.gaussian_kde(xy)
xr=np.linspace(np.log10(harris_cat_merged["r_h"]).min(),np.log10(harris_cat_merged["r_h"]).max(),100)
yr=np.linspace(harris_cat_merged["c"].min(),harris_cat_merged["c"].max(),100)
X,Y=np.meshgrid(xr,yr)
Z=kde(np.vstack([X.ravel(),Y.ravel()])).reshape(X.shape)

#Plotting the half light radius from Harris catalog vs the concentration from merged catalog
plt.contourf(X,Y,Z,levels=5,colors='white')
plt.scatter(np.log10(harris_cat_merged["r_h"]),harris_cat_merged["c"])
plt.plot(xr, slope * xr + intercept, 'r', label='Linear fit')
plt.scatter(np.log10(harris_cat_merged["r_h"][outliers]),harris_cat_merged["c"][outliers],facecolors='none',edgecolors='b',s=100,label='Outliers')
plt.xlabel(' log10 of half light radius (pc)')
plt.ylabel('concentration')
plt.title('Half light radius vs Concentration')
plt.savefig("results/half_light_radius_vs_concentration.png")
cbar.set_label('Log 10 of Age(Gyr)')
plt.show()