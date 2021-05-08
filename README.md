# Predicting CO2 Emissions Using Historical CO2 Data with PySta package 

Multiple efforts have been made to bring awareness to the public and one of them is to show the current data and predict the trends of CO2 levels in the future. We will be critiquing the given model. 


Unobserved parameters:
1. c0 and c1
These two parameters are the ones capable of the long-term growth of the C02 (ppm). This represents the linear trend of increase. 

2. c2 and c3
These parameters are responsible for the seasonal variations of the model. This can be seen by the oscillation trend and is based on a yearly pattern. 

3. c4
This parameter is responsible for the random noise which is used to cover for other uncertainties that are not included in the model. 

These variables are what we are going to use PyStan to sample with our assigned equations. The main objective of this project is to improvee the old model to make our predictions for the CO2 emission trajectory more accurate. 
