import h5py
import numpy as np
import corner

run_name = 'match_test_7'

f = h5py.File('data/' + run_name + '_data0_1126259642-413_analysis_H1L1_result.hdf5', 'r')

for key in f.keys():
    print(key)
    print(type(f[key]))

dims = 4

fixed_parameters = ['a_1', 'a_2', 'tilt_1', 'tilt_2', 'phi_12', 'phi_jl', 'dec', 'ra', 'psi', 'phase']
parameters = ['mass_ratio', 'chirp_mass_source', 'luminosity_distance', 'theta_jn']
posteriors = ['q_post', 'm_post', 'dL_post', 'thetajn_post']

post_dict = {}
injected_dict = {}
lower_quantiles_dict = {}
upper_quantiles_dict = {}

fixed_param_dict = {}

for i in range(dims):
    print('injected %s =' %parameters[i], f['injection_parameters'][parameters[i]][()])
    post_dict[posteriors[i]] = f['posterior'][parameters[i]][:]
    injected_dict[parameters[i]] = f['injection_parameters'][parameters[i]][()]
    lower_quantiles_dict[parameters[i]] = np.quantile(post_dict[posteriors[i]], 0.05)
    upper_quantiles_dict[parameters[i]] = np.quantile(post_dict[posteriors[i]], 0.95)

for fixed_param in fixed_parameters:
    fixed_param_dict[fixed_param] = set(f['posterior'][fixed_param][:])

data = np.array(list(post_dict.values())).T
injected_values = np.array(list(injected_dict.values()))
lower_quantiles = np.array(list(lower_quantiles_dict.values()))
upper_quantiles = np.array(list(upper_quantiles_dict.values()))

fig = corner.corner(data, labels=[
        r"$q$",
        r"$M$",
        r"$d_L [Mpc]$",
        r"$\theta_{JN}$",
    ], show_titles=True)

post_best_estimates = np.median(data, axis=0)

corner.overplot_lines(fig, injected_values, color='blue')
corner.overplot_points(fig, injected_values[None], marker='s', color='blue', label='injected value')

corner.overplot_lines(fig, post_best_estimates, color='orange')
corner.overplot_points(fig, post_best_estimates[None], marker='s', color='orange', label='best estimate')

corner.overplot_lines(fig, lower_quantiles, color='red')
corner.overplot_lines(fig, upper_quantiles, color='red')

fig.suptitle(run_name)

fig.savefig('plots/' + run_name + '_corner_plot.png')

print(fixed_param_dict)