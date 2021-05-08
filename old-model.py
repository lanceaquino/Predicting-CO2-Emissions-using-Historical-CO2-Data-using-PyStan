linear_stan_code = """
data {  
    int<lower=1> n;       // number of observations   
    real<lower=0> x_t[n] ; // CO2 ppm measured values 
    int<lower=0> t[n];      // number of days since measurements started in 1958
}
parameters {  
    //prior parameters
    real<lower=0> c0; //intercept
    real<lower=0> c1; //linear trend
    real<lower=0> c2; //seasonal variation
    real<lower=0> c3; //seasonal variation
    real c4; //gaussian noise
}
model {
    c0 ~ normal(356, 28);
    c1 ~ normal(0,10);
    c2 ~ normal(0,10);
    c3 ~ normal(0,10);
    c4 ~ normal(0,1); 
    for(i in 1:n) {
        x_t[i] ~ normal(c0 + c1*t[i] + c2*cos((2*pi()*t[i])/365.25 + c3), c4); // likelihood based on the given equation 
  }
}
"""
#Compile Stan Model
linear_stan_model = pystan.StanModel(model_code = linear_stan_code)

#Data for Stan Model
linear_stan_data = {
    'n' : num_weeks,
    'x_t': df['level'][:num_weeks],
    't': df['days'][:num_weeks]
}
#Fit Stan Model
linear_stan_results = linear_stan_model.sampling(data = linear_stan_data)
print(linear_stan_results)

#Extract the samples samples
linear_samples = linear_stan_results.extract()
linear_parameters = ['c0', 'c1', 'c2','c3', 'c4']
c0 = linear_samples['c0']
c1 = linear_samples['c1']
c2 = linear_samples['c2']
c3 = linear_samples['c3']
t = df['days'][:num_weeks]
