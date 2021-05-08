proposed_stan_code = """
data {
    int<lower=0> N;        // The number of data
    real level[N];           // co2 ppm level data
    int<lower=0> total;     // total days
    real t[total];          // days since first measurement
}
parameters {
    real<lower=0> c0;     // y
    real<lower=0> c1;     // linear
    real<lower=0> c2;     // quad
    real phi_x;           // seasonal
    real phi_y;           // seasonal
    real<lower=0> c4;     // amplitude
    real<lower=0> noise;  // noise 
} 
transformed parameters {
    real c3;
    c3 = atan2(phi_x, phi_y); //phi
} 
model { //priors
    c0 ~ normal(356,28);
    c1 ~ normal(0,10);
    c2 ~ normal(0,10);
    phi_x ~ normal(0,1);
    phi_y ~ normal(0,1); 
    c4 ~ normal(0,10);
    noise ~ normal(0,1);
    
    for(i in 1:N) {
        level[i] ~ normal(c0+c1*t[i]+(c2*(t[i]^2))+(c4)*cos(((2*pi()*t[i])/365.25)+c3),noise);
    }
}
generated quantities {
    real predicted_samples[total];
    for(i in 1:total) {
        predidcted_samples[i] = normal_rng(c0+c1*t[i]+(c2*(t[i]^2))+(c4)*cos(((2*pi()*t[i])/365.25)+c3),noise);
        }
}
"""

proposed_stan_model = pystan.StanModel(model_code = proposed_stan_code)

# Acquire Data from stan 
stan_data = { 
    'N': 3210, 
    'total':5281,
    'level': df.level[:3210], 
    't': df.days
}

# Use stan to sample from the stan model
# This took almost 30 mins 
proposed_parameters = ['c0','c1','c2','c3','c4', 'noise']
results = proposed_stan_model.sampling(data=stan_data)
samples = results.extract()

print(results.stansummary(pars=proposed_parameters)) #summary

# Extract predicted samples 
pred = samples['predicted_samples'] 

# Acquire confidence interval 
conf_int = np.percentile(pred, axis=0, q=[2.5, 97.5])
avgPred  = [np.mean(pred[:,i]) for i in range(len(df))] #taking mean

# Set limit for time 
start, end = 0, len(df) 
x = df.date[start:end]
