"""
This is a model based on the Borssele I and II offshore wind farm.
The model have been made using the already existing Hornsrev1 site as a basis, making it compatible with the PyWake tutorial.
"""
from py_wake import np
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
import matplotlib.pyplot as plt
#The wind farm consists of 94 SG8.0-167 DD wind turbines with following coordinates:
wt_x = [3838, 2416, 3391, 4142, 5036, 5868, 6619, 7452, 8711, 8508, 8305, 7066, 8000, 6477, 5523, 4934, 5442, 6782, 7716, 6802, 6863, 9462, 9706, 10477, 8223, 8508, 8751, 9198, 10497, 11330, 11939, 12223, 12406, 12528, 12792, 12995, 13117, 13340, 12244, 11330, 10355, 9259, 10051, 9970, 10863, 11228, 11492, 7756, 8832, 9970, 11066, 12142, 12832, 12629, 12447, 12244, 12000, 11777, 11635, 11391, 10437, 9563, 8711, 6843, 6091, 6294, 6355, 6640, 6883, 7188, 7411, 7594, 8832, 10071, 11350, 8690, 9888, 11330, 8447, 9584, 11046, 8122, 9299, 10782, 7817, 9056, 10701, 7614, 8893, 10274, 7594, 9076, 10193, 8102]
wt_y = [365, 995, 2152, 3269, 4426, 5462, 6457, 7513, 7939, 6883, 5645, 5178, 4000, 3777, 2660, 1259, -365, 1482, 2437, 183, -1117, 5178, 6416, 5340, -1665, -183, 1320, 2741, 3249, 4183, 3269, 2234, 1239, 223, -914, -1949, -2944, -4122, -3635, -3208, -2640, -2173, -893, 690, 1929, 81, -1584, -4061, -4670, -5239, -5685, -6274, -6863, -7959, -9137, -10254, -11411, -12589, -13665, -14802, -15939, -16914, -17970, -16792, -15797, -14274, -12731, -11046, -9746, -8284, -6883, -5462, -6132, -6883, -7168, -7614, -8467, -8426, -9178, -9970, -9665, -10579, -11431, -10964, -12122, -12812, -12122, -13645, -14335, -13543, -15310, -15756, -14822, -16853]

power_curve = np.array([[3.0, 0.0],
                        [4.0, 169.0],
                        [5.0, 593.0],
                        [6.0, 1307.0],
                        [7.0, 2186.0],
                        [8.0, 3278.0],
                        [9.0, 4687.0],
                        [10.0, 6112.0],
                        [11.0, 7249.0],
                        [12.0, 7795.0],
                        [13.0, 7947.0],
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

#As the Ct-curve of the SG8.0-167 DD wind turbine wasnt accessible, a reference Ct-curve was used.
#The Ct-curve used was the one of the LW 8 MW reference wind turbine, which is a wind turbine model based on the similarly sized Vestas V164-8 MW wind turbine.
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

class SG8_167(WindTurbine):
    def __init__(self, method='linear'):
        """
        Parameters
        ----------
        method : {'linear', 'pchip'}
            linear(fast) or pchip(smooth and gradient friendly) interpolation
        """
        WindTurbine.__init__(self, name='SG8_167', diameter=167, hub_height=116,
                             powerCtFunction=PowerCtTabular(power_curve[:, 0], power_curve[:, 1], 'w',
                                                            ct_curve[:, 1], method=method))
#The Weibull parameters are data collected from Global wind atlas at the coordinates N 51.438601°, E 3.026184° of the windfarm at 100m.
class Borssele1and2(UniformWeibullSite):
    def __init__(self, ti=.1, shear=None):
        f = [6, 8, 7, 7, 4, 4, 9, 13, 18, 11, 7, 6]#This is the probability of each wind direction.""" 
        a = [8.60, 8.89, 9.52, 9.81, 9.35, 8.90, 12.26, 12.08, 12.57, 9.96, 8.95, 9.05]#This is the Weibull scaling parameters for each wind direction sector."""
        k = [2.213, 2.400, 2.732, 2.639, 3.014, 2.311, 2.592, 2.736, 2.482, 2.068, 1.889, 1.979] #This is the Weibull shape parameter for each wind direction sector."""
        UniformWeibullSite.__init__(self, np.array(f) / np.sum(f), a, k, ti=ti, shear=shear)
        self.initial_position = np.array([wt_x, wt_y]).T

def main():
    wt = SG8_167()
    print('SG8.0-167 DD rotor diameter[m]:', wt.diameter())
    print('Hub heigh[m]:', wt.hub_height())

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

wts=SG8_167()
s = Borssele1and2
x, y = wt_x, wt_y
plt.figure()
wts.plot_xy(x,y)
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.legend()

plt.figure()
Borssele1and2().plot_wd_distribution(n_wd=12);
plt.title('Wind rose')
"""
Here the AEP and wake losses of the model is calculated using the NOJ wake deficit model.
"""
from py_wake import NOJ
windTurbines = SG8_167()
site = Borssele1and2()
noj = NOJ(site,windTurbines)
simulationResult = noj(wt_x,wt_y)
simulationResult.aep
print ("Total AEP of Borssele I & II: %f GWh"%simulationResult.aep().sum())
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
