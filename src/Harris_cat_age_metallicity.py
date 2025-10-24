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
galactic_longitude=harris_cat_merged["L"]
line_of_sight_velocity=harris_cat_merged["v_LSR"]
#letting the sin function be defined here for curve fitting since it best fits rotation curve trend
def sine_function(galactic_longitude, amplitude, frequency, phase, offset):
    longitude_radians = np.radians(galactic_longitude)
    return amplitude * np.sin(longitude_radians * frequency + phase) + offset # Sine function definition
#estimate initial parameters for curve fitting
initial_amplitude = (np.max(line_of_sight_velocity) - np.min(line_of_sight_velocity)) / 2
initial_frequency = 2 # Assuming 2 full sine wave cycles over 360 degrees
initial_phase = 0
initial_offset = np.mean(line_of_sight_velocity)
initial_parameters = [initial_amplitude, initial_frequency, initial_phase, initial_offset]
#curve fitting tool from scipy
from scipy.optimize import curve_fit
popt, pcov = curve_fit(sine_function, galactic_longitude, line_of_sight_velocity, p0=initial_parameters)
# Extracting the fitted parameters
fitted_amplitude, fitted_frequency, fitted_phase, fitted_offset = popt

#Trying to identify outliers based on our data based on residuals
residuals = line_of_sight_velocity - sine_function(galactic_longitude, *popt)
std_dev = np.std(residuals)
max_deviation = 2 * std_dev
outliers = np.abs(residuals) > max_deviation

# creating fitted values for plotting the sine curve
longitudes=np.linspace(0, 360, 500)
v_fit = sine_function(longitudes, *popt)
# Plot data and fitted curve
plt.plot(galactic_longitude, line_of_sight_velocity, 'o', label='Data')
plt.plot(longitudes, v_fit, 'r-', label='Fitted rotation curve')
if np.any(outliers):
    for i in np.where(outliers)[0]:
        plt.scatter(galactic_longitude[i], line_of_sight_velocity[i], facecolors='none', edgecolors='r', s=100)
        plt.annotate(harris_cat_merged["ID"].iloc[i], (galactic_longitude.iloc[i], line_of_sight_velocity.iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')
plt.xlabel("Galactic Longitude (degrees)")
plt.ylabel("Line of sight velocity(km/s)")
plt.title('Galactic Longitude vs Line of sight velocity with a curve fit')
plt.legend()
plt.savefig("results/Longitude_vs_velocity_sine_fit.png")
plt.show()

#%%
m,b=np.polyfit(harris_cat_merged["r_h"],harris_cat_merged["c"],1)
residuals_concentration=harris_cat_merged["c"]-(m*harris_cat_merged["r_h"]+b)
std_dev_concentration=np.std(residuals_concentration)
max_deviation_concentration=2*std_dev_concentration
outliers_concentration=np.abs(residuals_concentration)>max_deviation_concentration

#Plotting the half light radius from Harris catalog vs the concentration from merged catalog
plt.scatter(harris_cat_merged["r_h"],harris_cat_merged["c"],
## making a colour bar based on age
c=np.log10(harris_cat_merged["Age"]),marker='.')
cbar=plt.colorbar()
plt.plot(harris_cat_merged["r_h"],m*harris_cat_merged["r_h"]+b,color='red',label='Best fit line')
# highlighting any outliers found on our fitted data 
if np.any(outliers_concentration):
    for i in np.where(outliers_concentration)[0]:
        plt.scatter(harris_cat_merged["r_h"].iloc[i], harris_cat_merged["c"].iloc[i], facecolors='none', edgecolors='r', s=100)
        plt.annotate(harris_cat_merged["ID"].iloc[i], (harris_cat_merged["r_h"].iloc[i], harris_cat_merged["c"].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')
plt.title('Half light radius vs Concentration')
plt.xlabel('half light radius (pc)')
plt.ylabel('concentration')
plt.legend()
cbar.set_label('Log 10 of Age(Gyr)')
plt.savefig("results/half_light_radius_vs_concentration.png")
plt.show()
# %%