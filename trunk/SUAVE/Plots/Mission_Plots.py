import SUAVE
from SUAVE.Core import Units 
import pylab as plt 
import matplotlib
import matplotlib.pyplot as plt  
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from SUAVE.Methods.Aerodynamics.XFOIL.compute_airfoil_polars import read_airfoil_geometry

# ------------------------------------------------------------------
#   Altitude, SFC & Weight
# ------------------------------------------------------------------
def plot_altitude_sfc_weight(results, line_color = 'bo-', save_figure = False, save_filename = "Altitude_SFC_Weight"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values():

        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        aoa      = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        mass     = segment.conditions.weights.total_mass[:,0] / Units.lb
        altitude = segment.conditions.freestream.altitude[:,0] / Units.ft
        mdot     = segment.conditions.weights.vehicle_mass_rate[:,0]
        thrust   =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc      = (mdot / Units.lb) / (thrust /Units.lbf) * Units.hr

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , altitude , line_color)
        axes.set_ylabel('Altitude (ft)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)        
        axes.grid(True)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , sfc , line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('sfc (lb/lbf-hr)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)        
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mass , 'ro-' )
        axes.set_ylabel('Weight (lb)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)        
        axes.grid(True)
        
    if save_figure:
        plt.savefig(save_filename + ".png")  
        
    return

# ------------------------------------------------------------------
#   Aircraft Velocities
# ------------------------------------------------------------------
def plot_aircraft_velocities(results, line_color = 'bo-', save_figure = False, save_filename = "Aircraft_Velocities"):
    axis_font = {'fontname':'Arial', 'size':'14'}  
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values():

        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        Lift     = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag     = -segment.conditions.frames.wind.drag_force_vector[:,0] / Units.lbf
        Thrust   = segment.conditions.frames.body.thrust_force_vector[:,0] / Units.lb
        velocity = segment.conditions.freestream.velocity[:,0]
        pressure = segment.conditions.freestream.pressure[:,0]
        density  = segment.conditions.freestream.density[:,0]
        EAS      = velocity * np.sqrt(density/1.225)
        mach     = segment.conditions.freestream.mach_number[:,0]

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , velocity / Units.kts, line_color)
        axes.set_ylabel('velocity (kts)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)        
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , EAS / Units.kts, line_color)
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Equivalent Airspeed',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)        
        axes.grid(True)    
        
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , mach , line_color)
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Mach',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)        
        axes.grid(True)    
        
    if save_figure:
        plt.savefig(save_filename + ".png") 
        
    return

# ------------------------------------------------------------------
#   Disc and Power Loadings
# ------------------------------------------------------------------
def plot_disc_power_loading(results, line_color = 'bo-', save_figure = False, save_filename = "Disc_Power_Loading"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values():

        time  = segment.conditions.frames.inertial.time[:,0] / Units.min
        DL    = segment.conditions.propulsion.disc_loading
        PL    = segment.conditions.propulsion.power_loading   
   
        axes = fig.add_subplot(2,1,1)
        axes.plot(time, DL, line_color)
        axes.set_ylabel('Disc Loading lb/ft2',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)
        axes.grid(True)       
  
        axes = fig.add_subplot(2,1,2)
        axes.plot(time, PL, line_color )       
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Power Loading (lb/hp)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)         

    if save_figure:
        plt.savefig(save_filename + ".png")          
        
    return


# ------------------------------------------------------------------
#   Aerodynamic Coefficients
# ------------------------------------------------------------------
def plot_aerodynamic_coefficients(results, line_color = 'bo-', save_figure = False, save_filename = "Aerodynamic_Coefficients"):
    axis_font = {'fontname':'Arial', 'size':'14'}  
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)
    for segment in results.segments.values():

        time = segment.conditions.frames.inertial.time[:,0] / Units.min
        cl   = segment.conditions.aerodynamics.lift_coefficient[:,0,None] 
        cd   = segment.conditions.aerodynamics.drag_coefficient[:,0,None] 
        aoa  = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        l_d  = cl/cd

        axes = fig.add_subplot(4,1,1)
        axes.plot( time , aoa , line_color )
        axes.set_ylabel('Angle of Attack (deg)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)

        axes = fig.add_subplot(4,1,2)
        axes.plot( time , cl, line_color )
        axes.set_ylabel('CL',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)    
        
        axes = fig.add_subplot(4,1,3)
        axes.plot( time , cd, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('CD',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)    
        
        axes = fig.add_subplot(4,1,4)
        axes.plot( time , l_d, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('L/D',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)            
                
    if save_figure:
        plt.savefig(save_filename + ".png") 
        
    return

# ------------------------------------------------------------------
#   Aerodynamic Forces
# ------------------------------------------------------------------
def plot_aerodynamic_forces(results, line_color = 'bo-', save_figure = False, save_filename = "Aerodynamic_Forces"):
    axis_font = {'fontname':'Arial', 'size':'14'}  
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]  
        Lift   = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]          
        eta    = segment.conditions.propulsion.throttle[:,0]

        axes = fig.add_subplot(2,2,1)
        axes.plot( time , eta , line_color )
        axes.set_ylabel('Throttle',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)         
        axes.grid(True)	 

        axes = fig.add_subplot(2,2,2)
        axes.plot( time , Lift , line_color)
        axes.set_ylabel('Lift (N)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)         
        axes.grid(True)
        
        axes = fig.add_subplot(2,2,1)
        axes.plot( time , Thrust , line_color)
        axes.set_ylabel('Thrust (N)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)         
        axes.grid(True)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , Drag , line_color)
        axes.set_ylabel('Drag (N)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)         
        axes.grid(True)        
    
        
    if save_figure:
        plt.savefig(save_filename + ".png") 
            
    return


# ------------------------------------------------------------------
#   Drag Components
# ------------------------------------------------------------------
def plot_drag_components(results, line_color = 'bo-', save_figure = False, save_filename = "Drag_Components"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename,figsize=(8,10))
    axes = plt.gca()
    for segment in results.segments.values():

        time           = segment.conditions.frames.inertial.time[:,0] / Units.min
        drag_breakdown = segment.conditions.aerodynamics.drag_breakdown
        cdp            = drag_breakdown.parasite.total[:,0]
        cdi            = drag_breakdown.induced.total[:,0]
        cdc            = drag_breakdown.compressible.total[:,0]
        cdm            = drag_breakdown.miscellaneous.total[:,0]
        cd             = drag_breakdown.total[:,0]
         
        axes.plot( time , cdp , 'ko-', label='CD parasite' )
        axes.plot( time , cdi , line_color, label='CD induced' )
        axes.plot( time , cdc , 'go-', label='CD compressibility' )
        axes.plot( time , cdm , 'yo-', label='CD miscellaneous' )
        axes.plot( time , cd  , 'ro-', label='CD total'   )
        if i == 0:
            axes.legend(loc='upper center')   

    axes.set_xlabel('Time (min)',axis_font)
    axes.set_ylabel('CD',axis_font)
    axes.grid(True)         
    
    if save_figure:
        plt.savefig(save_filename + ".png") 
        
    return


# ------------------------------------------------------------------
#   Electronic Conditions
# ------------------------------------------------------------------
def plot_electronic_conditions(results, line_color = 'bo-', save_figure = False, save_filename = "Electronic_Conditions"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)
    for segment in results.segments.values():  
    
        time           = segment.conditions.frames.inertial.time[:,0] / Units.min
        energy         = segment.conditions.propulsion.battery_energy[:,0] 
        specific_power = segment.conditions.propulsion.battery_specfic_power[:,0]
        volts          = segment.conditions.propulsion.voltage_under_load[:,0] 
        volts_oc       = segment.conditions.propulsion.voltage_open_circuit[:,0]     
        current        = segment.conditions.propulsion.current[:,0]      
        battery_amp_hr = (energy*0.000277778)/volts
        C_rating   = current/battery_amp_hr
        
        axes = fig.add_subplot(2,2,1)
        axes.plot(time,specific_power, 'bo-')
        axes.set_ylabel('Specific Power kW/hg')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)      
        axes.grid(True)  
        axes.grid(True)       
    
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, energy*0.000277778, line_color)
        axes.set_ylabel('Battery Energy (W-hr)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)      
        axes.grid(True)   
    
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, volts, 'bo-',label='Under Load')
        axes.plot(time,volts_oc, 'ro-',label='Open Circuit')
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Battery Voltage (Volts)',axis_font)  
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)         
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, C_rating, line_color)
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('C-Rating (C)',axis_font)  
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)
 
    if save_figure:
        plt.savefig(save_filename + ".png")       
        
    return

def plot_residuals(results, line_color = 'bo-', save_figure = False, save_filename = "Residuals"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)
    for segment in results.segments.values():
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        if 'network' in segment.state.residuals:
            network_res = len(segment.state.residuals.network[0]) 
            for i in range(network_res-1):   
                net_residuals = segment.state.residuals.network[:,i]
                axes = fig.add_subplot(2,2,i+1)
                axes.plot( time , net_residuals, line_color)    
                axes.set_ylabel('Network Residuals ' + str(i+1),axis_font)
                axes.set_xlabel('Time (min)',axis_font)   
                axes.grid(True) 
                
        if 'forces' in segment.state.residuals:
            forces_res  = len(segment.state.residuals.forces[0]) 
            for j in range(network_res-1):
                forces_residuals = segment.state.residuals.forces[:,j]
                axes = fig.add_subplot(2,2,network_res+j)
                axes.plot( time , forces_residuals, line_color)
                axes.set_ylabel('Force Residuals ' + str(j+1) , axis_font)
                axes.set_xlabel('Time (min)', axis_font) 
                axes.grid(True) 

    return 
# ------------------------------------------------------------------
#   Flight Conditions
# ------------------------------------------------------------------
def plot_flight_conditions(results, line_color = 'bo-', save_figure = False, save_filename = "Flight_Conditions"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)
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
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)         
        axes.grid(True)            

        axes = fig.add_subplot(2,2,2)
        axes.plot( time , airspeed , line_color )
        axes.set_ylabel('Airspeed (m/s)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)

        axes = fig.add_subplot(2,2,3)
        axes.plot( time , theta, line_color )
        axes.set_ylabel('Pitch Angle (deg)',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)    
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , x, 'bo-', time , y, 'go-' , time , z, 'ro-')
        axes.set_ylabel('Displacement',axis_font)
        axes.set_xlabel('Time (min)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)           
        
    if save_figure:
        plt.savefig(save_filename + ".png")
        
    return


# ------------------------------------------------------------------
#   Propulsion Conditions
# ------------------------------------------------------------------
def plot_propulsor_conditions(results, line_color = 'bo-', save_figure = False, save_filename = "Propulsor"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    save_filename1 = save_filename + '_Results_1'
    save_filename2 = save_filename + '_Results_2'
    fig = plt.figure(save_filename1)
    fig.set_size_inches(10, 8)  
    for segment in results.segments.values():
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min        
        thrust   = segment.conditions.frames.body.thrust_force_vector[:,2]
        torque   = segment.conditions.propulsion.motor_torque[:,0] 
        effp     = segment.conditions.propulsion.etap[:,0]
        effm     = segment.conditions.propulsion.etam[:,0]
        
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, -thrust, line_color)
        axes.set_ylabel('Thrust (N)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)      
        axes.grid(True)   

        axes = fig.add_subplot(2,2,2)
        axes.plot(time, torque, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Torque (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)   
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, effm, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Motor Efficiency (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, effp, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Propeller Efficiency (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)           
        plt.ylim((0,1))
        
    fig = plt.figure(save_filename2)
    fig.set_size_inches(10, 8)  
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        rpm      = segment.conditions.propulsion.rpm  [:,0] 
        tip_mach = segment.conditions.propulsion.propeller_tip_mach[:,0]  
        throttle = segment.conditions.propulsion.throttle[:,0] 
        Cp       = segment.conditions.propulsion.propeller_power_coefficient[:,0]        

        axes = fig.add_subplot(2,2,1)
        axes.plot(time, throttle, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Throttle')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, Cp, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Coefficient')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, rpm, line_color)
        axes.set_ylabel('RPM',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)
        axes.grid(True)  
                
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, tip_mach, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Mach',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)
        
    if save_figure:
        plt.savefig(save_filename1 + ".png") 
        plt.savefig(save_filename2 + ".png")
            
    return


# ------------------------------------------------------------------
#   Stability Coefficients
# ------------------------------------------------------------------
def plot_stability_coefficients(results, line_color = 'bo-', save_figure = False, save_filename = "Stability_Coefficients"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        cm       = segment.conditions.stability.static['CM'][:,0,None] 
        cm_alpha = segment.conditions.stability.static['Cm_alpha'][:,0,None] 
        SM       = ((segment.conditions.stability.static['NP'][:,0,None] - 2.0144 )/ 0.9644599977664836)*100  
        aoa      = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        
        axes = fig.add_subplot(2,2,1)
        axes.plot( time , aoa, line_color )
        axes.set_ylabel(r'$AoA$',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)    
         
        axes = fig.add_subplot(2,2,2)
        axes.plot( time , cm, line_color )
        axes.set_ylabel(r'$C_M$',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)    
        
        axes = fig.add_subplot(2,2,3)
        axes.plot( time , cm_alpha, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel(r'$C_M\alpha$',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)    
        
        axes = fig.add_subplot(2,2,4)
        axes.plot( time , SM, line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Static Margin (%)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True) 
    
    if save_figure:
        plt.savefig(save_filename + ".png")
        
    return

# ------------------------------------------------------------------    
#   Solar Flux
# ------------------------------------------------------------------
def plot_solar_flux(results, line_color = 'bo-', save_figure = False, save_filename = "Solar_Flux"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename) 
    for segment in results.segments.values():               
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        flux   = segment.conditions.propulsion.solar_flux[:,0] 
        charge = segment.conditions.propulsion.battery_draw[:,0] 
        energy = segment.conditions.propulsion.battery_energy[:,0] / Units.MJ
    
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , flux , line_color )
        axes.set_ylabel('Solar Flux (W/m$^2$)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)               
        axes.grid(True)
    
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , charge , line_color )
        axes.set_ylabel('Charging Power (W)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)               
        axes.grid(True)
    
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , energy , line_color )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Battery Energy (MJ)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)               
        axes.grid(True)              
    
    if save_figure:
        plt.savefig(save_filename + ".png")
        
    return

# ------------------------------------------------------------------    
#   Lift Propulsor (Lift + Cruise eVTOL Configurations)
# ------------------------------------------------------------------
def plot_lift_propulsor(results, line_color = 'bo-', save_figure = False, save_filename = "Lift_Propulsor"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    save_filename1 = save_filename + '_Results_Pt1'
    save_filename2 = save_filename + '_Results_Pt2'
    save_filename3 = save_filename + '_Results_Pt3'
    fig = plt.figure(save_filename1)
    fig.set_size_inches(10, 8)  
    for segment in results.segments.values():
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min        
        thrust   = segment.conditions.frames.body.thrust_force_vector[:,2]
        torque   = segment.conditions.propulsion.motor_torque_lift[:,0] 
        effp     = segment.conditions.propulsion.propeller_efficiency_lift[:,0]
        effm     = segment.conditions.propulsion.motor_efficiency_lift[:,0]
        
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, -thrust, line_color)
        axes.set_ylabel('Thrust (N)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)      
        axes.grid(True)   
    
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, torque, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Torque (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)   
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, effm, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Motor Efficiency (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, effp, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Propeller Efficiency (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)           
        plt.ylim((0,1))
        
    fig = plt.figure(save_filename2)
    fig.set_size_inches(10, 8)  
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        rpm      = segment.conditions.propulsion.rpm_lift  [:,0] 
        tip_mach = segment.conditions.propulsion.propeller_tip_mach_lift[:,0]  
        throttle = segment.conditions.propulsion.throttle_lift[:,0] 
        Cp       = segment.conditions.propulsion.propeller_power_coefficient_lift[:,0]        

        axes = fig.add_subplot(2,2,1)
        axes.plot(time, throttle, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Throttle')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, Cp, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Coefficient')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, rpm, line_color)
        axes.set_ylabel('RPM',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)
        axes.grid(True)  
                
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, tip_mach, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Mach',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
    

    fig = plt.figure(save_filename3)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values():
        time  = segment.conditions.frames.inertial.time[:,0] / Units.min
        DL    = segment.conditions.propulsion.disc_loading_lift
        PL    = segment.conditions.propulsion.power_loading_lift  
   
        axes = fig.add_subplot(2,1,1)
        axes.plot(time, DL, line_color)
        axes.set_ylabel('Disc Loading lb/ft2',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)
        axes.grid(True)       
  
        axes = fig.add_subplot(2,1,2)
        axes.plot(time, PL, line_color )       
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Power Loading (lb/hp)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
    if save_figure:
        plt.savefig(save_filename1 + ".png") 
        plt.savefig(save_filename2 + ".png")
        plt.savefig(save_filename3 + ".png")
            
    return 

# ------------------------------------------------------------------    
#   Cruise Propulsor (Lift + Cruise eVTOL Configurations)
# ------------------------------------------------------------------
def plot_cruise_propulsor(results, line_color = 'bo-', save_figure = False, save_filename = "Cruise_Propulsor"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    save_filename1 = save_filename + '_Results_1'
    save_filename2 = save_filename + '_Results_2'
    save_filename3 = save_filename + '_Results_Pt3'
    fig = plt.figure(save_filename1)
    fig.set_size_inches(10, 8)  
    for segment in results.segments.values():
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min        
        thrust   = segment.conditions.frames.body.thrust_force_vector[:,2]
        torque   = segment.conditions.propulsion.motor_torque_forward[:,0] 
        effp     = segment.conditions.propulsion.propeller_efficiency_forward[:,0]
        effm     = segment.conditions.propulsion.motor_efficiency_forward[:,0]
        
        axes = fig.add_subplot(2,2,1)
        axes.plot(time, -thrust, line_color)
        axes.set_ylabel('Thrust (N)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)      
        axes.grid(True)   
    
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, torque, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Torque (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)   
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, effm, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Motor Efficiency (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)
        
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, effp, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Propeller Efficiency (N-m)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True)           
        plt.ylim((0,1))
        
    fig = plt.figure(save_filename2)
    fig.set_size_inches(10, 8)  
    for segment in results.segments.values(): 
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        rpm      = segment.conditions.propulsion.rpm_forward  [:,0] 
        tip_mach = segment.conditions.propulsion.propeller_tip_mach_forward[:,0] 
        throttle = segment.conditions.propulsion.throttle[:,0] 
        Cp       = segment.conditions.propulsion.propeller_power_coefficient[:,0]        

        axes = fig.add_subplot(2,2,1)
        axes.plot(time, throttle, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Throttle')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
        axes = fig.add_subplot(2,2,2)
        axes.plot(time, Cp, 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Coefficient')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
        axes = fig.add_subplot(2,2,3)
        axes.plot(time, rpm, line_color)
        axes.set_ylabel('RPM',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)
        axes.grid(True)  
                
        axes = fig.add_subplot(2,2,4)
        axes.plot(time, tip_mach, line_color )
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Mach',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
    fig = plt.figure(save_filename3)
    fig.set_size_inches(10, 8) 
    for segment in results.segments.values():
        time  = segment.conditions.frames.inertial.time[:,0] / Units.min
        DL    = segment.conditions.propulsion.disc_loading_forward
        PL    = segment.conditions.propulsion.power_loading_forward  
    
        axes = fig.add_subplot(2,1,1)
        axes.plot(time, DL, line_color)
        axes.set_ylabel('Disc Loading lb/ft2',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)
        axes.grid(True)       
    
        axes = fig.add_subplot(2,1,2)
        axes.plot(time, PL, line_color )       
        axes.set_xlabel('Time (mins)',axis_font)
        axes.set_ylabel('Power Loading (lb/hp)',axis_font)
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False)     
        axes.grid(True) 
        
    if save_figure:
        plt.savefig(save_filename1 + ".png") 
        plt.savefig(save_filename2 + ".png")
        plt.savefig(save_filename3 + ".png")

            
    return 
    

# ------------------------------------------------------------------    
#   Residuals
# ------------------------------------------------------------------
def plot_residuals(results, line_color = 'bo-', save_figure = False, save_filename = "Residuals"):
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename) 
    for segment in results.segments.values():
        time        = segment.conditions.frames.inertial.time[:,0] / Units.min
        residuals_1 = segment.state.residuals.network[:,0]
        residuals_2 = segment.state.residuals.network[:,1]
        
        axes = fig.add_subplot(2,2,1)
        axes.plot( time , residuals_1, 'bo-')
        axes.set_ylabel('residual 1')
        axes.set_xlabel('Time (min)')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True)  
        
        axes = fig.add_subplot(2,2,2)
        axes.plot( time , residuals_2, 'bo-')
        axes.set_ylabel('residual 2')
        axes.set_xlabel('Time (min)')
        axes.get_yaxis().get_major_formatter().set_scientific(False)
        axes.get_yaxis().get_major_formatter().set_useOffset(False) 
        axes.grid(True) 
        
    if save_figure:
        plt.savefig(save_filename + ".png")
        
    return         



# ------------------------------------------------------------------
#   Propeller Geoemtry 
# ------------------------------------------------------------------
def plot_propeller_geometry(prop, line_color = 'bo-', save_figure = False, save_filename = "Propeller_Geometry"):   
    # unpack
    Rt     = prop.tip_radius          
    Rh     = prop.hub_radius          
    num_B  = prop.number_blades       
    a_sec  = prop.airfoil_sections           
    a_secl = prop.airfoil_section_location   
    beta   = prop.twist_distribution         
    b      = prop.chord_distribution         
    r      = prop.radius_distribution        
    t      = prop.max_thickness_distribution
    
    # prepare plot parameters
    dim = len(b)
    theta = np.linspace(0,2*np.pi,num_B+1)

    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8)     
    ax = plt.axes(projection='3d') 
    ax.set_zlim3d(-1, 1)        
    ax.set_ylim3d(-1, 1)        
    ax.set_xlim3d(-1, 1)     
    
    chord = np.outer(np.linspace(0,1,10),b)
    for i in range(num_B):  
        # plot propeller planfrom
        surf_x = np.cos(theta[i]) * (chord*np.cos(beta)) - np.sin(theta[i]) * (r) 
        surf_y = np.sin(theta[i]) * (chord*np.cos(beta)) + np.cos(theta[i]) * (r) 
        surf_z = chord*np.sin(beta)                                
        ax.plot_surface(surf_x ,surf_y ,surf_z, color = 'gray')
        
        if  a_sec != None and a_secl != None:
            # check dimension of section  
            dim_sec = len(a_secl)
            if dim_sec != dim:
                raise AssertionError("Number of sections not equal to number of stations") 
                      
            # get airfoil coordinate geometry     
            airfoil_data = read_airfoil_geometry(a_sec)       
            
            #plot airfoils 
            for j in range(dim):
                airfoil_max_t = airfoil_data.thickness_to_chord[a_secl[j]]
                airfoil_xp = b[j] - airfoil_data.x_coordinates[a_secl[j]]*b[j]
                airfoil_yp = r[j]*np.ones_like(airfoil_xp)            
                airfoil_zp = airfoil_data.y_coordinates[a_secl[j]]*b[j]  * (t[j]/(airfoil_max_t*b[j]))
                
                transformation_1 = [[np.cos(beta[j]),0 , -np.sin(beta[j])], [0 ,  1 , 0] , [np.sin(beta[j]) , 0 , np.cos(beta[j])]]
                transformation_2 = [[np.cos(theta[i]) ,-np.sin(theta[i]), 0],[np.sin(theta[i]) , np.cos(theta[i]), 0], [0 ,0 , 1]] 
                transformation  = np.matmul(transformation_2,transformation_1)
                
                airfoil_x = np.zeros(len(airfoil_yp))
                airfoil_y = np.zeros(len(airfoil_yp))
                airfoil_z = np.zeros(len(airfoil_yp))     
                
                for k in range(len(airfoil_yp)):
                    vec_1 = [[airfoil_xp[k]],[airfoil_yp[k]], [airfoil_zp[k]]]
                    vec_2  = np.matmul(transformation,vec_1)
                    airfoil_x[k] = vec_2[0]
                    airfoil_y[k] = vec_2[1]
                    airfoil_z[k] = vec_2[2]
                            
                ax.plot3D(airfoil_x, airfoil_y, airfoil_z, color = 'gray')
                
    if save_figure:
        plt.savefig(save_filename + ".png")  
                    
    return


# ------------------------------------------------------------------
#   Propeller Performance
# ------------------------------------------------------------------
def plot_propeller_performance(noise, line_color = 'bo-', save_figure = False, save_filename = "Propeller_Performance"): 
    axis_font = {'fontname':'Arial', 'size':'14'} 
    fig = plt.figure(save_filename)
    fig.set_size_inches(10, 8) 
    T = noise.blade_T_distribution[:][0]
    Q = noise.blade_Q_distribution[:][0]
    r = noise.radius_distribution
           
    axes = fig.add_subplot(2,1,1)
    axes.plot(r, T , line_color)
    axes.set_ylabel('T (N)',axis_font)
    axes.set_xlabel('r (m)',axis_font)
    axes.get_yaxis().get_major_formatter().set_scientific(False)
    axes.get_yaxis().get_major_formatter().set_useOffset(False)
    axes.grid(True)      
    
    if save_figure:
        plt.savefig(save_filename + ".png")  
        
    return