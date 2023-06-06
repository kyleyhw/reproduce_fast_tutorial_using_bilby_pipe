import h5py
import numpy as np
import corner

# f = h5py.File('match_test_data0_1126259642-413_analysis_H1L1_result.hdf5', 'r')
f = h5py.File('match_test_2_data0_1126259642-413_analysis_H1L1_result.hdf5', 'r')

for key in f.keys():
    print(key)
    print(type(f[key]))

dims = 4

parameters = ['mass_ratio', 'chirp_mass_source', 'luminosity_distance', 'theta_jn']
posteriors = ['q_post', 'm_post', 'dL_post', 'thetajn_post']

post_dict = {}
injected_dict = {}
lower_quantiles_dict = {}
upper_quantiles_dict = {}

for i in range(dims):
    print('injected %s =' %parameters[i], f['injection_parameters'][parameters[i]][()])
    post_dict[posteriors[i]] = f['posterior'][parameters[i]][:]
    injected_dict[parameters[i]] = f['injection_parameters'][parameters[i]][()]
    lower_quantiles_dict[parameters[i]] = np.quantile(post_dict[posteriors[i]], 0.05)
    upper_quantiles_dict[parameters[i]] = np.quantile(post_dict[posteriors[i]], 0.95)

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

fig.savefig('corner_plot.png')