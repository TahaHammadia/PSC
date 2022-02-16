from scipy.optimize import curve_fit
import numpy as np

def P(x, a):
    return np.sqrt(2/np.pi)* (x**2*np.exp(-x**2/(2*a**2)))/a**3

def logistique(x, m1, s1, m2, s2, m3, s3, a):
    y1 = P(x-m1, s1)
    y2 = P(x-m2, s2)
    y3 = P(x-m3, s3)
    return a*(y1 + y2 + y3)


init_vals = np.array([559.2301741237069, 21.39477382989631, 370.6739453645084, 373.6288048243284, -2069.8630727315517, 4762.318472841551, 9799/0.01])
# les valeurs initiales sont prises pour trois fittings maxwelliens pour les énergies [E1..E5], [E6. .E10], [E11. .E16]
best_vals, covar = curve_fit(logistique, Ereel, ncorr, p0=init_vals)
print('best_vals: {}'.format(best_vals))