## @ingroup Plots
# Mission_Plots.py
# 
# Created:  Mar 2020, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import SUAVE
from SUAVE.Core import Units 
import matplotlib.pyplot as plt  
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Ellipse, Polygon
import colorsys 
import matplotlib.animation as animation
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ------------------------------------------------------------------
#   Altitude, SFC & Weight
# ------------------------------------------------------------------
## @ingroup Plots
def plot_altitude_sfc_weight(results, line_color = 'bo-', save_figure = False, save_filename = "Altitude_SFC_Weight" , file_type = ".png"):
    """This plots the altitude, speficic fuel comsumption and vehicle weight 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.
        freestream.altitude
        weights.total_mass
        weights.vehicle_mass_rate
        frames.body.thrust_force_vector

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	  
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min 
        mass     = segment.conditions.weights.total_mass[:,0] / Units.lb
        altitude = segment.conditions.freestream.altitude[:,0] / Units.ft
        mdot     = segment.conditions.weights.vehicle_mass_rate[:,0]
        thrust   =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc      = (mdot / Units.lb) / (thrust /Units.lbf) * Units.hr

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , altitude , line_color)
        axes.set_ylabel('Altitude (ft)',axis_font)
        set_axes(axes)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , sfc , line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('sfc (lb/lbf-hr)',axis_font)
        set_axes(axes)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mass , 'ro-' )
        axes.set_ylabel('Weight (lb)',axis_font)
        set_axes(axes)
        
    if save_figure:
        plt.savefig(save_filename + file_type)  
        
    return

# ------------------------------------------------------------------
#   Aircraft Velocities
# ------------------------------------------------------------------
## @ingroup Plots
def plot_aircraft_velocities(results, line_color = 'bo-', save_figure = False, save_filename = "Aircraft_Velocities", file_type = ".png"):
    """This plots aircraft velocity, mach , true air speed 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.freestream.
        velocity
        density
        mach_number 

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	
    axis_font = {'size':'14'}  
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min 
        velocity = segment.conditions.freestream.velocity[:,0]
        pressure = segment.conditions.freestream.pressure[:,0]
        density  = segment.conditions.freestream.density[:,0]
        EAS      = velocity * np.sqrt(density/1.225)
        mach     = segment.conditions.freestream.mach_number[:,0]

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , velocity / Units.kts, line_color)
        axes.set_ylabel('velocity (kts)',axis_font)
        set_axes(axes)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , EAS / Units.kts, line_color)
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Equivalent Airspeed',axis_font)
        set_axes(axes)    
        
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , mach , line_color)
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Mach',axis_font)
        set_axes(axes)  
        
    if save_figure:
        plt.savefig(save_filename + file_type) 
        
    return

# ------------------------------------------------------------------
#   Disc and Power Loadings
# ------------------------------------------------------------------
## @ingroup Plots
def plot_disc_power_loading(results, line_color = 'bo-', save_figure = False, save_filename = "Disc_Power_Loading", file_type = ".png"):
    """This plots the propeller disc and power loadings

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.propulsion.
        disc_loadings
        power_loading 
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	   
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10) 
    
    for i in range(len(results.segments)): 
        time  = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        DL    = results.segments[i].conditions.propulsion.disc_loading
        PL    = results.segments[i].conditions.propulsion.power_loading   
   
        axes = fig.add_subplot(2,1,1)
        axes.plot(time, DL, line_color)
        axes.set_ylabel('lift disc power N/m^2',axis_font)
        set_axes(axes)      
  
        axes = fig.add_subplot(2,1,2)
        axes.plot(time, PL, line_color )       
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('lift power loading (N/W)',axis_font)
        set_axes(axes)       

    if save_figure:
        plt.savefig(save_filename + file_type)          
        
    return


# ------------------------------------------------------------------
#   Aerodynamic Coefficients
# ------------------------------------------------------------------
## @ingroup Plots
def plot_aerodynamic_coefficients(results, line_color = 'bo-', save_figure = False, save_filename = "Aerodynamic_Coefficients", file_type = ".png"):
    """This plots the aerodynamic coefficients 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.aerodynamics.
        lift_coefficient
        drag_coefficient
        angle_of_attack
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	    
    axis_font = {'size':'14'}  
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10)
    
    for segment in results.segments.values(): 
        time = segment.conditions.frames.inertial.time[:,0] / Units.min
        cl   = segment.conditions.aerodynamics.lift_coefficient[:,0,None] 
        cd   = segment.conditions.aerodynamics.drag_coefficient[:,0,None] 
        aoa  = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        l_d  = cl/cd

        axes = fig.add_subplot(2,2,1)
        axes.plot( time , aoa , line_color )
        axes.set_ylabel('Angle of Attack (deg)',axis_font)
        set_axes(axes)

        axes = fig.add_subplot(2,2,2)
        axes.plot( time , cl, line_color )
        axes.set_ylabel('CL',axis_font)
        set_axes(axes)   
        
        axes = fig.add_subplot(2,2,3)
        axes.plot( time , cd, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('CD',axis_font)
        set_axes(axes)   
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , l_d, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('L/D',axis_font)
        set_axes(axes)            
                
    if save_figure:
        plt.savefig(save_filename + file_type) 
        
    return

# ------------------------------------------------------------------
#   Aerodynamic Forces
# ------------------------------------------------------------------
## @ingroup Plots
def plot_aerodynamic_forces(results, line_color = 'bo-', save_figure = False, save_filename = "Aerodynamic_Forces", file_type = ".png"):
    """This plots the aerodynamic forces

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.frames
         body.thrust_force_vector 
         wind.lift_force_vector        
         wind.drag_force_vector   
         
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	   
    axis_font = {'size':'14'}  
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10)
    
    for segment in results.segments.values():
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]  
        Lift   = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]          
        eta    = segment.conditions.propulsion.throttle[:,0]

        axes = fig.add_subplot(2,2,1)
        axes.plot( time , eta , line_color )
        axes.set_ylabel('Throttle',axis_font)
        set_axes(axes)	 

        axes = fig.add_subplot(2,2,2)
        axes.plot( time , Lift , line_color)
        axes.set_ylabel('Lift (N)',axis_font)
        set_axes(axes)
        
        axes = fig.add_subplot(2,2,3)
        axes.plot( time , Thrust , line_color)
        axes.set_ylabel('Thrust (N)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        set_axes(axes)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , Drag , line_color)
        axes.set_ylabel('Drag (N)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        set_axes(axes)       
    
    if save_figure:
        plt.savefig(save_filename + file_type) 
            
    return

# ------------------------------------------------------------------
#   Drag Components
# ------------------------------------------------------------------
## @ingroup Plots
def plot_drag_components(results, line_color = 'bo-', save_figure = False, save_filename = "Drag_Components", file_type = ".png"):
    """This plots the drag components of the aircraft

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.aerodynamics.drag_breakdown
          parasite.total 
          induced.total 
          compressible.total    
          miscellaneous.total     
    
    Outputs: 
    Plots
    
    Properties Used:
    N/A	
    """	  
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename,figsize=(8,10))
    axes = plt.gca()
    
    for i, segment in enumerate(results.segments.values()):
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        drag_breakdown = segment.conditions.aerodynamics.drag_breakdown
        cdp = drag_breakdown.parasite.total[:,0]
        cdi = drag_breakdown.induced.total[:,0]
        cdc = drag_breakdown.compressible.total[:,0]
        cdm = drag_breakdown.miscellaneous.total[:,0]
        cd  = drag_breakdown.total[:,0]
        
        if i == 0:
            axes.plot( time , cdp , 'ko-', label='CD parasite' )
            axes.plot( time , cdi , line_color, label='CD induced' )
            axes.plot( time , cdc , 'go-', label='CD compressibility' )
            axes.plot( time , cdm , 'yo-', label='CD miscellaneous' )
            axes.plot( time , cd  , 'ro-', label='CD total'   )    
            axes.legend(loc='upper center')   
        else:
            axes.plot( time , cdp , 'ko-')
            axes.plot( time , cdi , line_color)
            axes.plot( time , cdc , 'go-')
            axes.plot( time , cdm , 'yo-')
            axes.plot( time , cd  , 'ro-') 
            
    axes.set_xlabel('Time (min)',axis_font)
    axes.set_ylabel('CD',axis_font)
    axes.grid(True)         
    
    if save_figure:
        plt.savefig(save_filename + file_type) 
        
    return


# ------------------------------------------------------------------
#   Electronic Conditions
# ------------------------------------------------------------------
## @ingroup Plots
def plot_electronic_conditions(results, line_color = 'bo-', save_figure = False, save_filename = "Electronic_Conditions", file_type = ".png"):
    """This plots the electronic conditions of the network

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion
         battery_draw 
         battery_energy    
         battery_voltage_under_load     
         battery_voltage_open_circuit    
         current        
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	  
    
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename + "_1")
    fig.set_size_inches(12, 14)
    
    fig2 = plt.figure(save_filename + "_2")
    fig2.set_size_inches(12, 14)    
    
    for i in range(len(results.segments)):     
        time           = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        power          = results.segments[i].conditions.propulsion.battery_draw[:,0] 
        energy         = results.segments[i].conditions.propulsion.battery_energy[:,0] 
        volts          = results.segments[i].conditions.propulsion.battery_voltage_under_load [:,0] 
        volts_oc       = results.segments[i].conditions.propulsion.battery_voltage_open_circuit[:,0]  
        charge         = results.segments[i].conditions.propulsion.battery_charge_throughput[:,0]  
        bat_temp       = results.segments[i].conditions.propulsion.battery_cell_temperature[:,0] 
        current        = results.segments[i].conditions.propulsion.battery_current[:,0]      
        SOC            = results.segments[i].conditions.propulsion.battery_state_of_charge[:,0]
        battery_amp_hr = (energy/ Units.Wh )/volts  
        C_rating       = current/battery_amp_hr
        
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, -power/1000, line_color)
        axes.set_ylabel('Battery Power (kilo-Watts)',axis_font)
        set_axes(axes)       
    
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, volts, 'bo-',label='Under Load')
        axes.plot(time,volts_oc, 'ks--',label='Open Circuit') 
        axes.set_ylabel('Battery Voltage (Volts)',axis_font)  
        set_axes(axes) 
        if i == 0:
            axes.legend(loc='upper right')  
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, C_rating, line_color)
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('C-Rating (C)',axis_font)  
        set_axes(axes)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, current, line_color)
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Current (A)',axis_font)  
        set_axes(axes) 
    
        axes2 = fig2.add_subplot(2,2,1)
        axes2.plot(time, energy/ Units.Wh/1000, line_color)
        axes2.set_ylabel('Battery Energy (kW-hr)',axis_font)
        set_axes(axes2)  
        
        axes2 = fig2.add_subplot(2,2,2)
        axes2.plot(time, SOC, line_color)
        axes2.set_xlabel('Time (mins)',axis_font)
        axes2.set_ylabel('State of Charge',axis_font)  
        set_axes(axes2)        
         
        axes2 = fig2.add_subplot(2,2,3)
        axes2.plot(time, charge, line_color)
        axes2.set_xlabel('Time (mins)',axis_font)
        axes2.set_ylabel('Charge Throughput (Ah)',axis_font)  
        set_axes(axes2)  
        
        axes2 = fig2.add_subplot(2,2,4)
        axes2.plot(time, bat_temp, line_color)
        axes2.set_xlabel('Time (mins)',axis_font)
        axes2.set_ylabel('Battery Tempertature ($\degree$ C)',axis_font)  
        set_axes(axes2)     
        
    if save_figure:
        plt.savefig(save_filename + "_1" + file_type)   
        plt.savefig(save_filename + "_2" + file_type) 
        
    return


# ------------------------------------------------------------------
#   Flight Conditions
# ------------------------------------------------------------------
## @ingroup Plots
def plot_flight_conditions(results, line_color = 'bo-', save_figure = False, save_filename = "Flight_Conditions", file_type = ".png"):
    """This plots the flights the conditions 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
         frames 
             body.inertial_rotations
             inertial.position_vector 
         freestream.velocity
         aerodynamics.
             lift_coefficient
             drag_coefficient
             angle_of_attack
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	    
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10)
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        airspeed = segment.conditions.freestream.velocity[:,0] 
        theta    = segment.conditions.frames.body.inertial_rotations[:,1,None] / Units.deg
        cl       = segment.conditions.aerodynamics.lift_coefficient[:,0,None] 
        cd       = segment.conditions.aerodynamics.drag_coefficient[:,0,None] 
        aoa      = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        
        x        = segment.conditions.frames.inertial.position_vector[:,0]
        y        = segment.conditions.frames.inertial.position_vector[:,1]
        z        = segment.conditions.frames.inertial.position_vector[:,2]
        altitude = segment.conditions.freestream.altitude[:,0]
        
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, altitude, line_color)
        axes.set_ylabel('Altitude (m)',axis_font)
        set_axes(axes)            

        axes = fig.add_subplot(2,2,2)
        axes.plot( time , airspeed , line_color )
        axes.set_ylabel('Airspeed (m/s)',axis_font)
        set_axes(axes)

        axes = fig.add_subplot(2,2,3)
        axes.plot( time , theta, line_color )
        axes.set_ylabel('Pitch Angle (deg)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        set_axes(axes)   
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , x, 'bo-')      
        axes.set_ylabel('Range (m)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        set_axes(axes)         
        
    if save_figure:
        plt.savefig(save_filename + file_type)
        
    return

# ------------------------------------------------------------------
#   Propulsion Conditions
# ------------------------------------------------------------------
## @ingroup Plots
def plot_propeller_conditions(results, line_color = 'bo-', save_figure = False, save_filename = "Propeller", file_type = ".png"):
    """This plots the propeller performance

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions. 
        frames.inertial.time 
        propulsion.rpm 
        frames.body.thrust_force_vector 
        propulsion.motor_torque 
        propulsion.propeller_tip_mach 
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	 
    
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10)  
    
    for segment in results.segments.values():  
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        rpm    = segment.conditions.propulsion.rpm[:,0] 
        effp   = segment.conditions.propulsion.etap[:,0]
        Cp     = segment.conditions.propulsion.propeller_power_coefficient[:,0] 
        tm     = segment.conditions.propulsion.propeller_tip_mach[:,0]
 
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, Cp, line_color)
        axes.set_ylabel('Power Coefficient $(C_p)$',axis_font)
        set_axes(axes)

        axes = fig.add_subplot(2,2,2)
        axes.plot(time, effp , line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Propeller Efficiency $(\eta_P)$',axis_font)
        set_axes(axes)  
        
            
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, rpm, line_color)
        axes.set_ylabel('RPM',axis_font)
        set_axes(axes)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, tm, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Tip Mach',axis_font)
        set_axes(axes)     
        
    if save_figure:
        plt.savefig(save_filename + file_type)  
            
    return

# ------------------------------------------------------------------
#   Electric Propulsion efficiencies
# ------------------------------------------------------------------
## @ingroup Plots
def plot_eMotor_Prop_efficiencies(results, line_color = 'bo-', save_figure = False, save_filename = "eMotor_Prop_Propulsor", file_type = ".png"):
    """This plots the electric driven network propeller efficiencies 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion. 
         etap
         etam
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	   
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10)  
    for segment in results.segments.values():
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        effp   = segment.conditions.propulsion.etap[:,0]
        effm   = segment.conditions.propulsion.etam[:,0]
        
        axes = fig.add_subplot(1,2,1)
        axes.plot(time, effp, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Propeller Efficiency (N-m)',axis_font)
        set_axes(axes)         
        plt.ylim((0,1))
        
        axes = fig.add_subplot(1,2,2)
        axes.plot(time, effm, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Motor Efficiency (N-m)',axis_font)
        set_axes(axes)
        
    if save_figure:
        plt.savefig(save_filename + file_type)  
            
    return

# ------------------------------------------------------------------
#   Stability Coefficients
# ------------------------------------------------------------------
## @ingroup Plots
def plot_stability_coefficients(results, line_color = 'bo-', save_figure = False, save_filename = "Stability_Coefficients", file_type = ".png"):
    """This plots the static stability characteristics of an aircraft

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.stability.
       static
           CM 
           Cm_alpha 
           static_margin 
       aerodynamics.
           angle_of_attack
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	    
    axis_font = {'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(12, 10)
    
    for segment in results.segments.values():
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        cm       = segment.conditions.stability.static.CM[:,0]
        cm_alpha = segment.conditions.stability.static.Cm_alpha[:,0]
        SM       = segment.conditions.stability.static.static_margin[:,0]
        aoa      = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        
        axes = fig.add_subplot(2,2,1)
        axes.plot( time , aoa, line_color )
        axes.set_ylabel(r'$AoA$',axis_font)
        set_axes(axes)   
         
        axes = fig.add_subplot(2,2,2)
        axes.plot( time , cm, line_color )
        axes.set_ylabel(r'$C_M$',axis_font)
        set_axes(axes)  
        
        axes = fig.add_subplot(2,2,3)
        axes.plot( time , cm_alpha, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel(r'$C_M\alpha$',axis_font)
        set_axes(axes)  
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , SM, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Static Margin (%)',axis_font)
        set_axes(axes)
    
    if save_figure:
        plt.savefig(save_filename + file_type)
        
    return

# ------------------------------------------------------------------    
#   Solar Flux
# ------------------------------------------------------------------
## @ingroup Plots
def plot_solar_flux(results, line_color = 'bo-', save_figure = False, save_filename = "Solar_Flux", file_type = ".png"):
    """This plots the solar flux and power train performance of an solar powered aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion
        solar_flux 
        battery_draw 
        battery_energy 
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """
    
    axis_font = {'size':'14'} 
    fig       = plt.figure(save_filename) 
    fig.set_size_inches(8, 14)
    
    for segment in results.segments.values():               
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        flux   = segment.conditions.propulsion.solar_flux[:,0] 
        charge = segment.conditions.propulsion.battery_draw[:,0] 
        energy = segment.conditions.propulsion.battery_energy[:,0] / Units.MJ
    
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , flux , line_color )
        axes.set_ylabel('Solar Flux (W/m$^2$)',axis_font)
        set_axes(axes)
    
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , charge , line_color )
        axes.set_ylabel('Charging Power (W)',axis_font)
        set_axes(axes)
    
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , energy , line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Battery Energy (MJ)',axis_font)
        set_axes(axes)            
    
    if save_figure:
        plt.savefig(save_filename + file_type)
        
    return

# ------------------------------------------------------------------
#   Lift-Cruise Network
# ------------------------------------------------------------------
## @ingroup Plots
def plot_lift_cruise_network(results, line_color = 'bo-', save_figure = False, save_filename = "Lift_Cruise_Network", file_type = ".png"):
    """This plots the electronic and propulsor performance of a vehicle with a lift cruise network

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion
         throttle 
         rotor_throttle 
         battery_energy
         battery_specfic_power 
         battery_voltage_under_load   
         battery_voltage_open_circuit   
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """   
    axis_font = {'size':'14'} 
    # ------------------------------------------------------------------
    #   Electronic Conditions
    # ------------------------------------------------------------------
    fig = plt.figure("Lift_Cruise_Electric_Conditions")
    fig.set_size_inches(16, 8)
    for i in range(len(results.segments)):          
        time           = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        eta            = results.segments[i].conditions.propulsion.throttle[:,0]
        eta_l          = results.segments[i].conditions.propulsion.throttle_lift[:,0]
        energy         = results.segments[i].conditions.propulsion.battery_energy[:,0]/ Units.Wh
        specific_power = results.segments[i].conditions.propulsion.battery_specfic_power[:,0]
        volts          = results.segments[i].conditions.propulsion.battery_voltage_under_load [:,0] 
        volts_oc       = results.segments[i].conditions.propulsion.battery_voltage_open_circuit[:,0]  
                    
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, eta, 'bo-',label='Forward Motor')
        axes.plot(time, eta_l, 'r^-',label='Lift Motors')
        axes.set_ylabel('Throttle')
        set_axes(axes)     
        plt.ylim((0,1))
        if i == 0:
            axes.legend(loc='upper center')         
    
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, energy, 'bo-')
        axes.set_ylabel('Battery Energy (W-hr)')
        set_axes(axes)
    
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, volts, 'bo-',label='Under Load')
        axes.plot(time,volts_oc, 'ks--',label='Open Circuit')
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Battery Voltage (Volts)')  
        set_axes(axes)
        
        if i == 0:
            axes.legend(loc='upper center')                
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, specific_power, 'bo-') 
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Specific Power')  
        set_axes(axes)
        
    if save_figure:
        plt.savefig("Lift_Cruise_Electric_Conditions" + file_type)
    
   
    # ------------------------------------------------------------------
    #   Propulsion Conditions
    # ------------------------------------------------------------------
    fig = plt.figure("Prop-Rotor Network")
    fig.set_size_inches(16, 8)
    for i in range(len(results.segments)):          
        time         = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        prop_rpm     = results.segments[i].conditions.propulsion.rpm_forward[:,0] 
        prop_thrust  = results.segments[i].conditions.frames.body.thrust_force_vector[:,0]
        prop_torque  = results.segments[i].conditions.propulsion.motor_torque_forward
        prop_effp    = results.segments[i].conditions.propulsion.propeller_efficiency_forward[:,0]
        prop_effm    = results.segments[i].conditions.propulsion.motor_efficiency_forward[:,0]
        prop_Cp      = results.segments[i].conditions.propulsion.propeller_power_coefficient[:,0]
        rotor_rpm    = results.segments[i].conditions.propulsion.rpm_lift[:,0] 
        rotor_thrust = -results.segments[i].conditions.frames.body.thrust_force_vector[:,2]
        rotor_torque = results.segments[i].conditions.propulsion.motor_torque_lift[:,0]
        rotor_effp   = results.segments[i].conditions.propulsion.propeller_efficiency_lift[:,0]
        rotor_effm   = results.segments[i].conditions.propulsion.motor_efficiency_lift[:,0] 
        rotor_Cp     = results.segments[i].conditions.propulsion.propeller_power_coefficient_lift[:,0]        
    
        axes = fig.add_subplot(2,3,1)
        axes.plot(time, prop_rpm, 'bo-')
        axes.plot(time, rotor_rpm, 'r^-')
        axes.set_ylabel('RPM')
        set_axes(axes)      
    
        axes = fig.add_subplot(2,3,2)
        axes.plot(time, prop_thrust, 'bo-')
        axes.plot(time, rotor_thrust, 'r^-')
        axes.set_ylabel('Thrust (N)')
        set_axes(axes)  
    
        axes = fig.add_subplot(2,3,3)
        axes.plot(time, prop_torque, 'bo-' )
        axes.plot(time, rotor_torque, 'r^-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Torque (N-m)')
        set_axes(axes)
    
        axes = fig.add_subplot(2,3,4)
        axes.plot(time, prop_effp, 'bo-' )
        axes.plot(time, rotor_effp, 'r^-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel(r'Propeller Efficiency, $\eta_{propeller}$')
        set_axes(axes)      
        plt.ylim((0,1))
    
        axes = fig.add_subplot(2,3,5)
        axes.plot(time, prop_effm, 'bo-' )
        axes.plot(time, rotor_effm, 'r^-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel(r'Motor Efficiency, $\eta_{motor}$')
        set_axes(axes)       
        plt.ylim((0,1))
    
        axes = fig.add_subplot(2,3,6)
        axes.plot(time, prop_Cp, 'bo-' )
        axes.plot(time, rotor_Cp, 'r^-'  )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Coefficient')
        set_axes(axes)
        
    if save_figure:
        plt.savefig("Propulsor_Network" + file_type)
            
    # ------------------------------------------------------------------
    #   Propulsion Conditions
    # ------------------------------------------------------------------
    fig = plt.figure("Rotor")
    fig.set_size_inches(16, 8)
    for i in range(len(results.segments)):          
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        rpm    = results.segments[i].conditions.propulsion.rpm_lift [:,0] 
        thrust = results.segments[i].conditions.frames.body.thrust_force_vector[:,2]
        torque = results.segments[i].conditions.propulsion.motor_torque_lift
        effp   = results.segments[i].conditions.propulsion.propeller_efficiency_lift[:,0]
        effm   = results.segments[i].conditions.propulsion.motor_efficiency_lift[:,0] 
        Cp     = results.segments[i].conditions.propulsion.propeller_power_coefficient_lift[:,0]
    
        axes = fig.add_subplot(2,3,1)
        axes.plot(time, rpm, 'r^-')
        axes.set_ylabel('RPM')
        set_axes(axes)      
    
        axes = fig.add_subplot(2,3,2)
        axes.plot(time, -thrust, 'r^-')
        axes.set_ylabel('Thrust (N)')
        set_axes(axes)
    
        axes = fig.add_subplot(2,3,3)
        axes.plot(time, torque, 'r^-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Torque (N-m)')
        set_axes(axes)
    
        axes = fig.add_subplot(2,3,4)
        axes.plot(time, effp, 'r^-',label= r'$\eta_{rotor}$' ) 
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel(r'Propeller Efficiency $\eta_{rotor}$')
        set_axes(axes)    
        plt.ylim((0,1))
    
        axes = fig.add_subplot(2,3,5)
        axes.plot(time, effm, 'r^-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel(r'Motor Efficiency $\eta_{mot}$')
        set_axes(axes)
        plt.ylim((0,1))  
    
        axes = fig.add_subplot(2,3,6)
        axes.plot(time, Cp , 'r^-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Coefficient')
        set_axes(axes)            
    
    if save_figure:
        plt.savefig("Rotor" + file_type)  
        
    # ------------------------------------------------------------------
    #   Propulsion Conditions
    # ------------------------------------------------------------------
    fig = plt.figure("Propeller")
    fig.set_size_inches(16, 8)
    for i in range(len(results.segments)):          
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        rpm    = results.segments[i].conditions.propulsion.rpm_forward [:,0] 
        thrust = results.segments[i].conditions.frames.body.thrust_force_vector[:,0]
        torque = results.segments[i].conditions.propulsion.motor_torque_forward[:,0]
        effp   = results.segments[i].conditions.propulsion.propeller_efficiency_forward[:,0]
        effm   = results.segments[i].conditions.propulsion.motor_efficiency_forward[:,0]
        Cp     = results.segments[i].conditions.propulsion.propeller_power_coefficient[:,0]
    
        axes = fig.add_subplot(2,3,1)
        axes.plot(time, rpm, 'bo-')
        axes.set_ylabel('RPM')
        set_axes(axes)       
    
        axes = fig.add_subplot(2,3,2)
        axes.plot(time, thrust, 'bo-')
        axes.set_ylabel('Thrust (N)')
        set_axes(axes)   
    
        axes = fig.add_subplot(2,3,3)
        axes.plot(time, torque, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Torque (N-m)')
        set_axes(axes)  
    
        axes = fig.add_subplot(2,3,4)
        axes.plot(time, effp, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel(r'Propeller Efficiency $\eta_{propeller}$')
        set_axes(axes)            
        plt.ylim((0,1))
    
        axes = fig.add_subplot(2,3,5)
        axes.plot(time, effm, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel(r'Motor Efficiency $\eta_{motor}$')
        set_axes(axes) 
    
        axes = fig.add_subplot(2,3,6)
        axes.plot(time, Cp, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Coefficient')
        set_axes(axes)  
        
    if save_figure:
        plt.savefig("Cruise_Propulsor" + file_type)
       
    # ------------------------------------------------------------------
    #   Propulsion Conditions
    # ------------------------------------------------------------------
    fig = plt.figure("Tip_Mach") 
    for i in range(len(results.segments)):          
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
        rtm  = results.segments[i].conditions.propulsion.propeller_tip_mach_lift[:,0]
        ptm  = results.segments[i].conditions.propulsion.propeller_tip_mach_forward[:,0] 
        
        axes = fig.add_subplot(1,1,1)
        axes.plot(time, ptm, 'bo-',label='Propeller')
        axes.plot(time, rtm, 'r^-',label='Rotor')
        axes.set_ylabel('Mach')
        set_axes(axes)   
        if i == 0:
            axes.legend(loc='upper center')     
    
    if save_figure:
        plt.savefig("Tip_Mach" + file_type) 
        
        
    return

# ------------------------------------------------------------------
#   Set Axis Parameters 
# ------------------------------------------------------------------
## @ingroup Plots
def set_axes(axes):
    """This sets the axis parameters for all plots

    Assumptions:
    None

    Source:
    None

    Inputs
    axes
        
    Outputs: 
    axes

    Properties Used:
    N/A	
    """   
    
    axes.minorticks_on()
    axes.grid(which='major', linestyle='-', linewidth='0.5', color='grey')
    axes.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')      
    axes.grid(True)   

    return  