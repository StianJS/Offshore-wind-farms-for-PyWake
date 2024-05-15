"""
This is a model based on the Hornsea Project 2 offshore wind farm.
The model have been made using the already existing Hornsrev1 site as a basis, making it compatible with the PyWake tutorial.
"""
from py_wake import np
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
import matplotlib.pyplot as plt
#The wind farm consists of 165 SG8.0-167 DD wind turbines with following coordinates.
wt_x = [-600,	1240,	2680,	-80,	1840,	3160,	-400,	960,	2680,	4120,	120,	3520,	5080,	640,	-160,	1320,	2840,	5160,	7000,	560,	2200,	3880,	80,	1960,	4920,	480,	43080,	42520,	40760,	40600,	39720,	39000,	38800,	38000,	37240,	37240,	36360,	35080,	37400,	36800,	36160,	35360,	34680,	33360,	32520,	34360,	33680,	32800,	31960,	31200,	31240,	29880,	31400,	30800,	30200,	29200,	28640,	28320,	26880,	27440,	26760,	25960,	25160,	25280,	23840,	24960,	24040,	23280,	22480,	21800,	21520,	20280,	18880,	18400,	17200,	16920,	15160,	15320,	16480,	15480,	15160,	10880,	11960,	11600,	12240,	11640,	12480,	11680,	12680,	12200,	11600,	13000,	12480,	12880,	13480,	12680,	13360,	12200,	9400,	10200,	10760,	8880,	9160,	8560,	9040,	10240,	9240,	9520,	10760,	9880,	11000,	11840,	10760,	11680,	9760,	10560,	9000,	7720,	6240,	7040,	6200,	7160,	5320,	6000,	6800,	7440,	8280,	8040,	9040,	9960,	8040,	8880,	7040,	7960,	6000,	7440,	5120,	6920,	4720,	4680,	5400,	4000,	3120,	2080,	1040,	0,	2160,	-80,	760,	2760,	3880,	-40,	120,	2760,	4120,	720,	3080,	160,	5600,	840,	120,	1240,	3000,	4560,	5920]
wt_y = [19680,	19560,	19480,	18960,	18680,	18760,	17080,	17320,	17400,	17280,	16400,	16120,	15840,	15480,	14360,	14480,	14360,	13640,	13000,	13160,	13160,	12800,	11600,	11160,	11320,	10920,	14680,	15800,	15840,	14400,	15680,	16360,	12760,	13960,	15120,	16600,	16520,	16840,	10400,	11400,	12360,	13680,	14720,	16800,	17080,	10880,	11760,	13240,	14640,	15760,	17120,	17200,	11040,	11920,	12840,	14400,	15280,	17200,	17200,	12720,	13800,	15080,	16240,	17360,	17680,	12160,	13640,	14840,	16040,	17080,	18280,	18520,	17160,	18840,	19040,	16720,	17480,	19080,	12480,	14040,	12120,	-200,	440,	1160,	2840,	3600,	4600,	5720,	7200,	7920,	8920,	10040,	10880,	13400,	14760,	16000,	17360,	19040,	-160,	1000,	2320,	560,	2560,	3440,	5000,	5920,	7440,	9080,	10280,	11600,	13080,	14880,	16520,	17600,	18160,	19280,	19280,	-120,	-240,	920,	2240,	3160,	3680,	5000,	6160,	7480,	8920,	11400,	12880,	14800,	14480,	16320,	15920,	17720,	17480,	18600,	18680,	19360,	19360,	-160,	1120,	920,	-200,	0,	-200,	0,	1480,	1640,	2000,	2920,	3400,	3240,	4440,	5160,	5480,	5960,	7080,	6800,	8000,	8080,	9080,	9880,	9640,	9560,	9720]

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

"""As the Ct-curve of the SG8.0-167 DD wind turbine wasnt accessible, a reference Ct-curve was used.
The Ct-curve used was the one of the LW 8 MW reference wind turbine, which is a wind turbine model based on the similarly sized Vestas V164-8 MW wind turbine.
Description of an 8 MW reference wind turbine: https://iopscience.iop.org/article/10.1088/1742-6596/753/9/092013#references
"""
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
        
#The Weibull parameters are data collected from Global wind atlas at the coordinatesN 53.530064°, E 1.472992° of the windfarm at a height of 100m and roughness 0.00.
class Hornsea2(UniformWeibullSite):
    def __init__(self, ti=.1, shear=None):
        f = [6, 4, 5, 7, 5, 8, 10, 13, 16, 11, 8, 7]#This is the probability of each wind direction.
        a = [9.74, 8.58, 9.03, 10.06, 9.08, 10.50, 11.65, 13.18, 13.08, 11.95, 10.04, 10.25]#This is the Weibull scaling parameters for each wind direction sector.
        k = [2.557, 2.279, 2.607, 2.232, 2.037, 2.506, 2.068, 2.428, 2.760, 2.256, 2.471, 2.182]#This is the Weibull shape parameter for each wind direction sector.
        UniformWeibullSite.__init__(self, np.array(f) / np.sum(f), a, k, ti=ti, shear=shear)
        self.initial_position = np.array([wt_x, wt_y]).T

def main():
    wt = SG8_167()
    print('SG8.0-167 DD rotor diameter[m]:', wt.diameter())
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

wts=SG8_167()
s = Hornsea2
x, y = wt_x, wt_y
plt.figure()
wts.plot_xy(x,y)
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.legend()

plt.figure()
Hornsea2().plot_wd_distribution(n_wd=12);
plt.title('Wind rose')


"""
Here the AEP of the model is calculated using the NOJ wake deficit model.
"""
from py_wake import NOJ
windTurbines = SG8_167()
site = Hornsea2()
noj = NOJ(site,windTurbines)
simulationResult = noj(wt_x,wt_y)
simulationResult.aep
print ("Total AEP of Hornsea Project 2: %f GWh"%simulationResult.aep().sum())