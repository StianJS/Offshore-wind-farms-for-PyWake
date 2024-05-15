"""
This is a model based on the Borkum Riffgrund II offshore wind farm.
The model have been made using the already existing Hornsrev1 site as a basis, making it compatible with the PyWake tutorial.
"""
from py_wake import np
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
import matplotlib.pyplot as plt
#The wind farm consists of 56 V164-8 MW wind turbines with following coordinates:
wt_x = [-5781, -4534, -3795, -2356, -5753, -5027, -3493, -2356, -5726, -5027, -2356, -5685, -5000, -4247, -3479, -1932, -5219, -2712, -1932, -4685, -3726, 0, -4301, -3014, -1151, 384, -3479, -2712, -1151, 384, 1945, -2836, -1945, -1164, 384, 2110, 3027, -2274, -1164, 384, -1808, -1329, -493, 384, 1137, 1890, 2630, 3384, 4137, 4890, 5644, 6425, 5767, 7301, 7301, 7301]
wt_y = [3877, 4301, 4301, 4301, 3110, 3110, 3082, 3082, 2329, 2329, 2356, 1575, 1575, 1575, 1575, 1575, 822, 822, 890, -27, 41, 0, -507, -740, -753, -753, -1534, -1534, -1548, -1562, -1534, -2342, - 2342, -2342, -2342, -2507, -2384, -3055, -3123, -3123, -3644, -4260, -4123, -3904, -3726, -3548, -3356, -3205, -3014, -2822, -2644, -2466, 3904, 3904, 3151, 2370]

power_curve = np.array([[3.0, 0.0],
                        [4.0, 100.0],
                        [5.0, 650.0],
                        [6.0, 1150.0],
                        [7.0, 1850.0],
                        [8.0, 2900.0],
                        [9.0, 4150.0],
                        [10.0, 5600.0],
                        [11.0, 7100.0],
                        [12.0, 7800.0],
                        [13.0, 8000.0],
                        [14.0, 8000.0],
                        [15.0, 8000.0],
                        [16.0, 8000.0],
                        [17.0, 8000.0],
                        [18.0, 8000.0],
                        [19.0, 8000.0],
                        [20.0, 8000.0],
                        [21.0, 8000.0],
                        [22.0, 8000.0],
                        [23.0, 8000.0],
                        [24.0, 8000.0],
                        [25.0, 8000.0]]) * [1, 1000]
#As the Ct-curve of the V164-8 MW wind turbine wasnt accessible a reference Ct-curve was used.
#The Ct-curve used was the one of the LW 8 MW reference wind turbine, which is a wind turbine model based on the Vestas V164-8 MW wind turbine.
#Description of an 8 MW reference wind turbine: https://iopscience.iop.org/article/10.1088/1742-6596/753/9/092013#references
ct_curve = np.array([[3, 0.0],
                     [4, 0.92],
                     [5, 0.85],
                     [6, 0.82],
                     [7, 0.80],
                     [8, 0.78],
                     [9, 0.76],
                     [10, 0.73],
                     [11, 0.67],
                     [12, 0.52],
                     [13, 0.39],
                     [14, 0.30],
                     [15, 0.24],
                     [16, 0.19],
                     [17, 0.16],
                     [18, 0.14],
                     [19, 0.12],
                     [20, 0.10],
                     [21, 0.09],
                     [22, 0.08],
                     [23, 0.07],
                     [24, 0.06],
                     [25, 0.05],
                     ])

class V164(WindTurbine):
    def __init__(self, method='linear'):
        """
        Parameters
        ----------
        method : {'linear', 'pchip'}
            linear(fast) or pchip(smooth and gradient friendly) interpolation
        """
        WindTurbine.__init__(self, name='V164', diameter=164, hub_height=105,
                             powerCtFunction=PowerCtTabular(power_curve[:, 0], power_curve[:, 1], 'w',
                                                            ct_curve[:, 1], method=method))
#The Weibull parameters are based on data from Global wind atlas at the coordinates N 54.580061°, E 6.294479°of the windfarm and height 100m and roughness 0.00.
class BorkumRiffgrund2(UniformWeibullSite):
    def __init__(self, ti=.1, shear=None):
        f = [ 5, 4, 6, 8, 6, 6, 8, 12, 14, 12, 10, 9]#This is the probability of each wind direction.""" 
        a = [8.48, 7.56, 9.29, 11.10, 11.54, 10.99, 11.28, 12.67, 12.67, 11.96, 11.54, 10.26]#This is the Weibull scaling parameters for each wind direction sector."""
        k = [2.166, 2.162, 2.178, 2.299, 2.604, 2.607, 2.002, 2.467, 2.396, 2.342, 2.568, 2.186]#This is the Weibull shape parameter for each wind direction sector."""
        UniformWeibullSite.__init__(self, np.array(f) / np.sum(f), a, k, ti=ti, shear=shear)
        self.initial_position = np.array([wt_x, wt_y]).T

def main():
    wt = V164()
    print('Turbine diameter[m]:', wt.diameter())
    print('Hub height[m]:', wt.hub_height())

    plt.figure()
    ws = np.linspace(3, 20, 100)    
    plt.plot(ws, wt.power(ws) * 1e-3, label='Power')
    c = plt.plot([], [], label='Ct')[0].get_color()
    plt.ylabel('Power [kW]')
    plt.xlabel('Wind speed [m/s]')
    ax = plt.gca().twinx()
    ax.plot(ws, wt.ct(ws), color=c)
    ax.set_ylabel('Ct')
    plt.xlabel('Wind speed [m/s]')
    plt.gcf().axes[0].legend(loc=1)
    plt.show()

if __name__ == '__main__':
    main()

wts=V164()
s = BorkumRiffgrund2
x, y = wt_x, wt_y
plt.figure()
wts.plot_xy(x,y)
plt.xlim()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.legend()

plt.figure()
BorkumRiffgrund2().plot_wd_distribution(n_wd=12);
plt.title('Wind rose')

"""
Here the AEP and wake losses of the model is calculated using the NOJ wake deficit model.
"""
from py_wake import NOJ
windTurbines = V164()
site = BorkumRiffgrund2()
noj = NOJ(site,windTurbines)
simulationResult = noj(wt_x,wt_y)
simulationResult.aep
print ("Total AEP of Borkum Riffgrund II: %f GWh"%simulationResult.aep().sum())
wf_model = NOJ(site, windTurbines)
sim_res = wf_model(x, y, # wind turbine positions
                   h=None, # wind turbine heights(defaults to the heights defined in windTurbines)
                   type=0, # Wind turbine types
                   wd=None,# Wind direction
                   ws=None,# Wind speed
                  )
sim_res
sim_res.aep()
aep_with_wake_loss = sim_res.aep().sum().data
aep_witout_wake_loss = sim_res.aep(with_wake_loss=False).sum().data
wake_loss = aep_witout_wake_loss - aep_with_wake_loss
print('wake loss: %f'%wake_loss, 'GWh per year')
