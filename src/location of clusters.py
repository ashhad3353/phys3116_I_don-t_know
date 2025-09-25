# I'm going to try and find roughly the most common location of clusters, 
# By comparing X,Y,Z of the data in HarrisPartI.csv
# I'll be plotting a 3-D plot of this data 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D. #package i found for 3-D plotting

H1 = pd.read_csv("data/HarrisPartI.csv")
list(H1.columns)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(H1['X'], H1['Y'], H1['Z'], c=H1['Z'], cmap='viridis')
plt.show()

