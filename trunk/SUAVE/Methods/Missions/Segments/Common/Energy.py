## @ingroup Methods-Missions-Segments-Common
# Energy.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero
#           Jul 2017, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
#  Initialize Battery
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def initialize_battery(segment):
    """ Sets the initial battery energy at the start of the mission
    
        Assumptions:
        N/A
        
        Inputs:
            segment.state.initials.conditions:
                propulsion.battery_energy    [Joules]
            segment.battery_energy           [Joules]
            
        Outputs:
            segment.state.conditions:
                propulsion.battery_energy    [Joules]

        Properties Used:
        N/A
                                
    """    
    
    if 'battery_energy' in segment:
        energy_initial                   = segment.battery_energy
        temperature_initial              = segment.battery_cell_temperature
        battery_age_in_days              = segment.battery_age_in_days
        battery_charge_throughput        = segment.battery_charge_throughput
        battery_discharge                = segment.battery_discharge  
        ambient_temperature              = segment.ambient_temperature
        battery_resistance_growth_factor = segment.battery_resistance_growth_factor 
        battery_capacity_fade_factor     = segment.battery_capacity_fade_factor     
    
    elif segment.state.initials:
        energy_initial                   = segment.state.initials.conditions.propulsion.battery_energy[-1,0]
        temperature_initial              = segment.state.initials.conditions.propulsion.battery_cell_temperature[-1,0]
        battery_charge_throughput        = segment.state.initials.conditions.propulsion.battery_charge_throughput  
        battery_age_in_days              = segment.battery_age_in_days
        battery_discharge                = segment.battery_discharge
        ambient_temperature              = segment.state.initials.conditions.propulsion.ambient_temperature
        battery_resistance_growth_factor = segment.state.initials.conditions.propulsion.battery_resistance_growth_factor
        battery_capacity_fade_factor     = segment.state.initials.conditions.propulsion.battery_capacity_fade_factor
                  
    else:
        energy_initial                   = 0.0
        temperature_initial              = 20.0
        ambient_temperature              = 20
        battery_age_in_days              = 1
        battery_charge_throughput        = 0.0
        battery_resistance_growth_factor = 1.0
        battery_capacity_fade_factor     = 1.0  
        battery_discharge                = True
     
    if 'battery_cell_temperature' in segment:
        temperature_initial              = segment.battery_cell_temperature 
     
    segment.state.conditions.propulsion.battery_energy[:,0]              = energy_initial
    segment.state.conditions.propulsion.battery_temperature[:,0]         = temperature_initial
    segment.state.conditions.propulsion.battery_age_in_days              = battery_age_in_days
    segment.state.conditions.propulsion.battery_charge_throughput        = battery_charge_throughput 
    segment.state.conditions.propulsion.battery_discharge                = battery_discharge
    segment.state.conditions.propulsion.ambient_temperature              = ambient_temperature
    segment.state.conditions.propulsion.battery_resistance_growth_factor = battery_resistance_growth_factor 
    segment.state.conditions.propulsion.battery_capacity_fade_factor     = battery_capacity_fade_factor        
    
    return

# ----------------------------------------------------------------------
#  Update Thrust
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def update_thrust(segment):
    """ Evaluates the energy network to find the thrust force and mass rate

        Inputs -
            segment.analyses.energy_network    [Function]

        Outputs -
            state.conditions:
               frames.body.thrust_force_vector [Newtons]
               weights.vehicle_mass_rate       [kg/s]


        Assumptions -


    """    
    
    # unpack
    energy_model = segment.analyses.energy

    # evaluate
    results   = energy_model.evaluate_thrust(segment.state)

    # pack conditions
    conditions = segment.state.conditions
    conditions.frames.body.thrust_force_vector = results.thrust_force_vector
    conditions.weights.vehicle_mass_rate       = results.vehicle_mass_rate
    

## @ingroup Methods-Missions-Segments-Common
def update_battery(segment):
    """ Evaluates the energy network to find the thrust force and mass rate

        Inputs -
            segment.analyses.energy_network    [Function]

        Outputs -
            state.conditions:
               frames.body.thrust_force_vector [Newtons]
               weights.vehicle_mass_rate       [kg/s]


        Assumptions -


    """    
    
    # unpack
    energy_model = segment.analyses.energy

    # evaluate
    results   = energy_model.evaluate_thrust(segment.state)

def update_battery_age(segment):  
     
    SOC     = segment.conditions.propulsion.state_of_charge
    V_oc    = np.mean(segment.conditions.propulsion.battery_OCV)
    t       = segment.conditions.propulsion.battery_age_in_days 
    Q_prior = segment.conditions.propulsion.battery_charge_throughput  
    Temp    = np.mean(segment.conditions.propulsion.battery_cell_temperature) 
    
    # aging model  
    delta_DOD = abs(SOC[0][0] - SOC[-1][0])
    rms_V_oc  = np.sqrt(np.mean(V_oc**2)) 
    alpha_cap = 0*((7.542*V_oc - 23.75)*1E6) * np.exp(-6976/(Temp +273))  # currently inactive
    alpha_res = 0*((5.270*V_oc - 16.32)*1E5) * np.exp(-5986/(Temp +273))  # currently inactive
    beta_cap  = 7.348E-3 * (rms_V_oc - 3.667)**2 +  7.60E-4 + 4.081E-3*delta_DOD
    beta_res  = 2.153E-4 * (rms_V_oc - 3.725)**2 - 1.521E-5 + 2.798E-4*delta_DOD
     
    segment.conditions.propulsion.battery_capacity_fade_factor     = 1 - 0.5*( + alpha_cap*(t**0.75) + beta_cap*np.sqrt(Q_prior))    
    segment.conditions.propulsion.battery_resistance_growth_factor = 1 + 0.5*( + alpha_res*(t**0.75) + beta_res*Q_prior) 
    