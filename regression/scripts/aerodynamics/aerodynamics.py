# aerodynamics.py
# 
# Created:  Sep 2014, T. MacDonald
# Modified: Nov 2016, T. MacDonald
#
# Modified to match compressibility drag updates

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------


import SUAVE
from SUAVE.Core import Units
from SUAVE.Core import Data

import numpy as np
import pylab as plt

import copy, time
import random
from SUAVE.Attributes.Gases.Air import Air
import sys
#import vehicle file
sys.path.append('../Vehicles')
from Boeing_737 import vehicle_setup


def main():
    
    # initialize the vehicle
    vehicle = vehicle_setup() 
    for wing in vehicle.wings:
        wing.areas.wetted   = 2.0 * wing.areas.reference
        wing.areas.exposed  = 0.8 * wing.areas.wetted
        wing.areas.affected = 0.6 * wing.areas.wetted  
                  
    # initalize the standard vlm aero model  
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.process.compute.lift.inviscid_wings.settings.use_weissinger            = False
    aerodynamics.process.compute.lift.inviscid_wings.settings.use_surrogate             = True
    aerodynamics.process.compute.lift.inviscid_wings.settings.plot_vortex_distribution  = True
    aerodynamics.process.compute.lift.inviscid_wings.settings.plot_vehicle              = True 
    aerodynamics.geometry = vehicle        
    aerodynamics.initialize()    
    
    # initalize the weissinger aero model - results are used in regression
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.process.compute.lift.inviscid_wings.settings.use_weissinger            = True
    aerodynamics.process.compute.lift.inviscid_wings.settings.use_surrogate             = True
    aerodynamics.process.compute.lift.inviscid_wings.settings.plot_vortex_distribution  = False
    aerodynamics.process.compute.lift.inviscid_wings.settings.plot_vehicle              = False   
    aerodynamics.geometry = vehicle        
    aerodynamics.initialize()    
        
    #no of test points
    test_num = 11
    
    #specify the angle of attack
    angle_of_attacks = np.linspace(-.174,.174,test_num)[:,None] #* Units.deg
    
    
    # Cruise conditions (except Mach number)
    state = SUAVE.Analyses.Mission.Segments.Conditions.State()
    state.conditions = SUAVE.Analyses.Mission.Segments.Conditions.Aerodynamics()
    
    
    state.expand_rows(test_num)    
        
    # --------------------------------------------------------------------
    # Initialize variables needed for CL and CD calculations
    # Use a pre-run random order for values
    # --------------------------------------------------------------------

    Mc = np.array([[0.9  ],
       [0.475],
       [0.05 ],
       [0.39 ],
       [0.815],
       [0.645],
       [0.305],
       [0.22 ],
       [0.56 ],
       [0.73 ],
       [0.135]])
    
    rho = np.array([[0.8],
           [1. ],
           [0.5],
           [1.1],
           [0.4],
           [1.3],
           [0.6],
           [0.3],
           [0.9],
           [0.7],
           [1.2]])
    
    mu = np.array([[1.85e-05],
           [1.55e-05],
           [1.40e-05],
           [1.10e-05],
           [2.00e-05],
           [8.00e-06],
           [6.50e-06],
           [9.50e-06],
           [1.70e-05],
           [1.25e-05],
           [5.00e-06]])
    
    T = np.array([[270.],
           [250.],
           [280.],
           [260.],
           [240.],
           [200.],
           [290.],
           [230.],
           [210.],
           [300.],
           [220.]])
    
    pressure = np.array([[ 100000.],
           [ 190000.],
           [ 280000.],
           [ 370000.],
           [ 460000.],
           [ 550000.],
           [ 640000.],
           [ 730000.],
           [ 820000.],
           [ 910000.],
           [1000000.]])
    
    re = np.array([[12819987.97468646],
           [ 9713525.47464844],
           [  599012.59815633],
           [12606549.94372309],
           [ 5062187.10214493],
           [29714816.00808047],
           [ 9611290.40694227],
           [ 2112171.68320523],
           [ 8612638.72342302],
           [14194381.78364854],
           [ 9633881.90543247]])    
    
    air = Air()
    a = air.compute_speed_of_sound(T,pressure)
    
    re = rho*a*Mc/mu

    
    state.conditions.freestream.mach_number = Mc
    state.conditions.freestream.density = rho
    state.conditions.freestream.dynamic_viscosity = mu
    state.conditions.freestream.temperature = T
    state.conditions.freestream.pressure = pressure
    state.conditions.freestream.reynolds_number = re
    
    state.conditions.aerodynamics.angle_of_attack = angle_of_attacks   
    
    
    # --------------------------------------------------------------------
    # Surrogate
    # --------------------------------------------------------------------    
    
            
    #call the aero model        
    results = aerodynamics.evaluate(state)
    
    #build a polar for the markup aero
    polar = Data()    
    CL = results.lift.total
    CD = results.drag.total
    polar.lift = CL
    polar.drag = CD    
    
    
    # --------------------------------------------------------------------
    # Test compute Lift
    # --------------------------------------------------------------------    
    lift = state.conditions.aerodynamics.lift_coefficient
    lift_r = np.array([ -1.07052515,-0.83788102,-0.60523689,-0.37259275,-0.13994862, 0.09269551,
                          0.32533964, 0.55798377, 0.7906279 , 1.02327204, 1.25591617])[:,None]  
  
    print('lift = ', lift)
    
    lift_test = np.abs((lift-lift_r)/lift)
    
    print('\nCompute Lift Test Results\n')
    #print lift_test
        
    assert(np.max(lift_test)<1e-6), 'Aero regression failed at compute lift test'    
    
    
    # --------------------------------------------------------------------
    # Test compute drag 
    # --------------------------------------------------------------------
    
    #compute_aircraft_drag(conditions, configuration, geometry)
    
    # Pull calculated values
    drag_breakdown = state.conditions.aerodynamics.drag_breakdown
    # Only one wing is evaluated since they rely on the same function
    cd_c           = drag_breakdown.compressible['main_wing'].compressibility_drag
    cd_i           = drag_breakdown.induced.total
    cd_m           = drag_breakdown.miscellaneous.total
    cd_p_fuse      = drag_breakdown.parasite['fuselage'].parasite_drag_coefficient
    cd_p_wing      = drag_breakdown.parasite['main_wing'].parasite_drag_coefficient
    cd_tot         = drag_breakdown.total
   
    print('cd_m =', cd_m)
    
   
    (cd_c_r, cd_i_r, cd_m_r, cd_p_fuse_r, cd_p_wing_r, cd_tot_r) = reg_values()
    
    drag_tests = Data()
    drag_tests.cd_c = np.abs((cd_c-cd_c_r)/cd_c)
    for ii,cd in enumerate(drag_tests.cd_c):
        if np.isnan(cd):
            drag_tests.cd_c[ii] = np.abs((cd_c[ii]-cd_c_r[ii])/np.min(cd_c[cd_c!=0]))
    drag_tests.cd_i = np.abs((cd_i-cd_i_r)/cd_i)
    drag_tests.cd_m = np.abs((cd_m-cd_m_r)/cd_m)
    drag_tests.cd_p_fuse      = np.abs((cd_p_fuse - cd_p_fuse_r)/cd_p_fuse)
    drag_tests.cd_p_wing      = np.abs((cd_p_wing - cd_p_wing_r)/cd_p_wing)
    drag_tests.cd_tot         = np.abs((cd_tot - cd_tot_r)/cd_tot)
    
    print('\nCompute Drag Test Results\n')    
    print('cd_tot=', cd_tot)
   
    for i, tests in list(drag_tests.items()): 
       
        assert(np.max(tests)<1e-4),'Aero regression test failed at ' + i
        
    #return conditions, configuration, geometry, test_num
      
def reg_values():
    cd_c_r = np.array([[ 1.91350062e-05,4.85545834e-09,6.76371959e-23,2.16812328e-09,2.80253645e-04,2.28463559e-05,
                         9.16414844e-10,1.61940004e-11,2.66735406e-05,2.14705495e-03,5.72829283e-14 ]]).T    
      
    cd_i_r = np.array([[0.04355469,0.02730153,0.01587736,0.00583811,0.00132687,0.00088987,
                        0.00460866,0.01297305,0.02437378,0.03983724,0.06086974 ]]).T
        
    cd_m_r = np.array([[0.00117677,0.00117677,0.00117677,0.00117677,0.00117677,0.00117677,
                        0.00117677,0.00117677,0.00117677,0.00117677,0.00117677 ]]).T
    
    cd_p_fuse_r     = np.array([[0.00573221,0.00669671,0.01034335,0.00656387,0.00669973,0.00560398,
                                 0.00687499,0.0085221 ,0.00669252,0.0060046 ,0.00697051  ]]).T        
      
    cd_p_wing_r     = np.array([[0.00584709,0.00597292,0.00949947,0.00577587,0.00658233, 
                                 0.00505553,0.00603557,0.00765395,0.00605556,0.00560651,0.00607082  ]]).T

    cd_tot_r        = np.array([[0.06737282,0.04617997,0.04445771,0.02382848,0.02225982,0.01655281,
                                 0.02335716,0.03639974,0.04333983,0.0601218 ,0.08091877   ]]).T
    
    return cd_c_r, cd_i_r, cd_m_r, cd_p_fuse_r, cd_p_wing_r, cd_tot_r

if __name__ == '__main__':

    main()
    
    print('Aero regression test passed!')
      
