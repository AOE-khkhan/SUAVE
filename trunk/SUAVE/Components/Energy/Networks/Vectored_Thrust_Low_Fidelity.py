## @ingroup Components-Energy-Networks
# Vectored_Thrust_Low_Fidelity.py
# 
# Created:  Nov 2018, M.Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE

# package imports
import numpy as np
from SUAVE.Components.Propulsors.Propulsor import Propulsor
import math 
from SUAVE.Core import Units, Data

# ----------------------------------------------------------------------
#  Network
# ----------------------------------------------------------------------

## @ingroup Components-Energy-Networks
class Vectored_Thrust_Low_Fidelity(Propulsor):
    """ This is a simple network with a battery powering a propeller through
        an electric motor
        Assumptions:
        None
        
        Source:
        None
    """  
    def __defaults__(self):
        """ This sets the default values for the network to function.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """             
        self.motor             = None
        self.propeller         = None
        self.esc               = None
        self.avionics          = None
        self.payload           = None
        self.battery           = None
        self.nacelle_diameter  = None
        self.engine_length     = None
        self.number_of_engines = None
        self.voltage           = None
        self.thrust_angle      = 0.0 
    
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
            Caps the throttle at 110% and linearly interpolates thrust off that
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
            conditions.propulsion:
                rpm                  [radians/sec]
                current              [amps]
                battery_power_draw         [watts]
                battery_energy       [joules]
                battery_voltage_open_circuit [volts]
                battery_voltage_under_load    [volts]
                motor_torque         [N-M]
                propeller_torque     [N-M]
    
            Properties Used:
            Defaulted values
        """          
    
        # unpack
        conditions = state.conditions
        numerics   = state.numerics
        motor      = self.motor
        propeller  = self.propeller
        esc        = self.esc
        avionics   = self.avionics
        payload    = self.payload
        battery    = self.battery
        num_engines= self.number_of_engines
        
        # Set battery energy
        battery.current_energy = conditions.propulsion.battery_energy  

        # Step 1 battery power
        #esc.inputs.voltagein = state.unknowns.battery_voltage_under_load
        esc.inputs.voltagein = self.voltage
        
        # Step 2
        esc.voltageout(conditions)   
        # link
        motor.inputs.voltage = esc.outputs.voltageout 
        # step 3
        motor.omega(conditions)
        # link
        propeller.inputs.omega =  motor.outputs.omega
        propeller.thrust_angle =  state.thrust_angle
        
        # step 4
        F, Q, P, Cp , noise, etap = propeller.spin(conditions)
            
        # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
        eta        = conditions.propulsion.throttle[:,0,None]
        P[eta>1.0] = P[eta>1.0]*eta[eta>1.0]
        F[eta>1.0] = F[eta>1.0]*eta[eta>1.0]

        # Run the avionics
        avionics.power()

        # Run the payload
        payload.power()
        
        # Run the motor for current
        motor.current(conditions)
        # link
        esc.inputs.currentout =  motor.outputs.current
        
        # Run the esc
        esc.currentin(conditions)

        # Calculate avionics and payload power
        avionics_payload_power = avionics.outputs.power + payload.outputs.power

        # Calculate avionics and payload current
        avionics_payload_current = avionics_payload_power/self.voltage

        # link
        battery.inputs.current  = esc.outputs.currentin*self.number_of_engines + avionics_payload_current
        battery.inputs.power_in = -(esc.outputs.voltageout*esc.outputs.currentin*self.number_of_engines + avionics_payload_power)
        battery.energy_discharge(numerics)        
    
        # Pack the conditions for outputs
        rpm                  = motor.outputs.omega*60./(2.*np.pi)
        a                    = conditions.freestream.speed_of_sound
        R                    = propeller.tip_radius      
        battery_power_draw         = battery.inputs.power_in   
          
        conditions.propulsion.rpm                                = rpm
        conditions.propulsion.current                            = esc.outputs.currentin
        conditions.propulsion.battery_power_draw                 = battery_power_draw
        conditions.propulsion.battery_energy                     = battery.current_energy    
        conditions.propulsion.battery_voltage_open_circuit       = battery.voltage_open_circuit
        conditions.propulsion.battery_voltage_under_load         = battery.voltage_under_load
        conditions.propulsion.motor_torque                       = motor.outputs.torque
        conditions.propulsion.propeller_torque                   = Q
        conditions.propulsion.acoustic_outputs[propeller.tag]    = noise
        conditions.propulsion.battery_specfic_power              = -(battery_power_draw/1000)/battery.mass_properties.mass #kWh/kg
        conditions.propulsion.propeller_tip_mach                 = (R*rpm)/a

        
        # Compute force vector       
        F_vec = self.number_of_engines * F * [np.cos(self.thrust_angle),0,-np.sin(self.thrust_angle)]   
        
        F_mag = np.atleast_2d(np.linalg.norm(F_vec, axis=1)*2.20462)  # lb   
        conditions.propulsion.disc_loading                       = (F_mag.T)/(num_engines*np.pi*(R*3.28084)**2) # lb/ft^2       
        conditions.propulsion.power_loading                      = (F_mag.T)/(battery_power_draw*0.00134102)           # lb/hp 

        mdot = np.zeros_like(F_vec)

        results = Data()
        results.thrust_force_vector = F_vec
        results.vehicle_mass_rate   = mdot   
        
        return results
    
    
    def unpack_unknowns(self,segment):
        """ This is an extra set of unknowns which are unpacked from the mission solver and send to the network.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state.unknowns.propeller_power_coefficient [None]
            state.unknowns.battery_voltage_under_load  [volts]
    
            Outputs:
            state.conditions.propulsion.propeller_power_coefficient [None]
            state.conditions.propulsion.battery_voltage_under_load  [volts]
    
            Properties Used:
            N/A
        """                  
        ones = segment.state.ones_row
        # Here we are going to unpack the unknowns (Cp) provided for this network
        segment.state.conditions.propulsion.battery_voltage_under_load       = segment.state.unknowns.battery_voltage_under_load
        segment.state.conditions.propulsion.propeller_power_coefficient      = segment.state.unknowns.propeller_power_coefficient
        segment.state.conditions.propulsion.throttle                         = segment.state.unknowns.throttle 
        #segment.state.conditions.propulsion.thurst_angle                     = segment.state.unknowns.thurst_angle
        
        return
    
    def residuals(self,segment):
        """ This packs the residuals to be send to the mission solver.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state.conditions.propulsion:
                motor_torque                          [N-m]
                propeller_torque                      [N-m]
                battery_voltage_under_load                     [volts]
            state.unknowns.battery_voltage_under_load [volts]
            
            Outputs:
            None
    
            Properties Used:
            self.voltage                              [volts]
        """        
        
        # Here we are going to pack the residuals (torque,voltage) from the network
        
        # Unpack
        q_motor   = segment.state.conditions.propulsion.motor_torque
        q_prop    = segment.state.conditions.propulsion.propeller_torque
        v_actual  = segment.state.conditions.propulsion.battery_voltage_under_load 
        v_predict = segment.state.unknowns.battery_voltage_under_load
        v_max     = self.voltage
        
        # Return the residuals
        segment.state.residuals.network[:,0] = q_motor[:,0] - q_prop[:,0]
        segment.state.residuals.network[:,1] = (v_predict[:,0] - v_actual[:,0])/v_max        
        return    
            
    __call__ = evaluate_thrust