"""
This is a model based on the Borssele III and IV offshore wind farm.
The model have been made using the already existing Hornsrev1 site as a basis, making it compatible with the PyWake tutorial.
"""
from py_wake import np
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
import matplotlib.pyplot as plt
#The wind farm consists of 77 wind turbines with following coordinates:
wt_x = [-11731, -10385, -8962, -7654, -6231, -10615, -8962, -7192, -5231, -4115, -2769, -1269, -9346, -7692, -6038, -3885, -8346, -6346, -4231, -2154, 0, -7192, -5077, -3423, -1923, -5769, -3154, -4577, -3000, -1577, -269, 808, -2846, -1577, -115, 1154, 1769, -1346, 192, 1346, 2731, -1154, 385, 1962, 3077, 385, 846, 2500, 3692, 4615, 1692, 1885, 3500, 4231, 3154, 3231, 4539, 4577, 4731, 5038, 5231, 5423, 5769, 6115, 6423, -3731, -2577, -1192, 154, 1346, 2769, 3923, -2269, -654, 577, 1692, 2538]
wt_y = [1308, 1692, 2077, 2577, 3038, 269, 923, 1384, 2461, 2038, 1500, 1038, -1038, -615, -153, 423, -2038, -1615, -1077, -577, 0, -3192, -3154, -2269, -2231, -4423, -3885, -5615, -5769, -3846, -2269, -885, -7308, -5423, -3769, -2308, -1308, -7154, -5192, -3577, -1731, -9038, -6923, -4923, -3462, -10346, -8615, -6962, -5462, -4154, -11731, -9731, -8654, -7077, -13115, -11038, -14538, -13231, -11923, -10462, -9154, -7808, -6231, -4769, -3346, 3885, 4192, 4731, 5154, 5462, 5885, 6308, 3308, 3385, 2154, 3577, 4692]
power_curve = np.array([[3.0, 0.0],
                        [4.0, 249.0],
                        [5.0, 613.0],
                        [6.0, 1226.0],
                        [7.0, 2030.0],
                        [8.0, 3123.0],
                        [9.0, 4444.0],
                        [10.0, 5900.0],
                        [11.0, 7299.0],
                        [12.0, 8601.0],
                        [13.0, 9272.0],
                        [14.0, 9500.0],
                        [15.0, 9500.0],
                        [16.0, 9500.0],
                        [17.0, 9500.0],
                        [18.0, 9500.0],
                        [19.0, 9500.0],
                        [20.0, 9500.0],
                        [21.0, 9500.0],
                        [22.0, 9500.0],
                        [23.0, 9500.0],
                        [24.0, 9500.0],
                        [25.0, 9500.0]]) * [1, 1000]
#Reference Ct-curve from the DTU 10 MW turbine
#As the Ct-curve of the V164-9.5 MW wind turbine wasnt accessible a reference Ct-curve from a similar sized wind turbine already in PyWake was used.
ct_curve = np.array([[3, 0.0],
                     [4, 0.923],
                     [5, 0.919],
                     [6, 0.904],
                     [7, 0.858],
                     [8, 0.814],
                     [9, 0.814],
                     [10, 0.814],
                     [11, 0.814],
                     [12, 0.577],
                     [13, 0.419],
                     [14, 0.323],
                     [15, 0.259],
                     [16, 0.211],
                     [17, 0.175],
                     [18, 0.148],
                     [19, 0.126],
                     [20, 0.109],
                     [21, 0.095],
                     [22, 0.084],
                     [23, 0.074],
                     [24, 0.066],
                     [25, 0.059],
                     ])
class V164(WindTurbine):
    def __init__(self, method='linear'):
        """
        Parameters
        ----------
        method : {'linear', 'pchip'}
            linear(fast) or pchip(smooth and gradient friendly) interpolation
        """
        WindTurbine.__init__(self, name='V164', diameter=164, hub_height=109,
                             powerCtFunction=PowerCtTabular(power_curve[:, 0], power_curve[:, 1], 'w',
                                                            ct_curve[:, 1], method=method))
#The Weibull parameters are data collected from Global wind atlas at the coordinatesN 51.438601°, E 3.026184° of the windfarm at 100m and rougness 0.00.
class Borssele3and4(UniformWeibullSite):
    def __init__(self, ti=.1, shear=None):
        f = [6, 8, 7, 7, 4, 4, 9, 13, 18, 11, 7, 6]#This is the probability of each wind direction.""" 
        a = [8.60, 8.89, 9.52, 9.81, 9.35, 8.90, 12.26, 12.08, 12.57, 9.96, 8.95, 9.05]#This is the Weibull scaling parameters for each wind direction sector."""
        k = [2.213, 2.400, 2.732, 2.639, 3.014, 2.311, 2.592, 2.736, 2.482, 2.068, 1.889, 1.979]#This is the Weibull shape parameter for each wind direction sector."""
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
s = Borssele3and4()
x, y = wt_x, wt_y
plt.figure()
wts.plot_xy(x,y)
plt.xlim()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.legend()

plt.figure()
Borssele3and4().plot_wd_distribution(n_wd=12);
plt.title('Wind rose')
"""
Here the AEP of the model is calculated using the NOJ wake deficit model.
"""
from py_wake import NOJ
windTurbines = V164()
site = Borssele3and4()
noj = NOJ(site,windTurbines)
simulationResult = noj(wt_x,wt_y)
simulationResult.aep
print ("Total AEP of Borssele III & IV: %f GWh"%simulationResult.aep().sum())