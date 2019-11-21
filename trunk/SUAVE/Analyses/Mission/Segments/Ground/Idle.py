## @ingroup Analyses-Mission-Segments-Ground
# Idle.py
#
# Created:   

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# SUAVE imports
from SUAVE.Analyses.Mission.Segments import Aerodynamic
from SUAVE.Methods.Missions import Segments as Methods
from SUAVE.Analyses.Mission.Segments import Conditions
 

from SUAVE.Analyses import Process
# Units
from SUAVE.Core import Units

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Ground
class Idle(Aerodynamic): 

    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  

    def __defaults__(self):  

        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """              
        
        # --------------------------------------------------------------
        #   User inputs
        # --------------------------------------------------------------
        self.altitude = None
        self.time     = 1.0 * Units.seconds
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.state.conditions.update( Conditions.Aerodynamics() )
        
        # initials and unknowns
        ones_row = self.state.ones_row
        
        
        # --------------------------------------------------------------
        #   The Solving Process
        # --------------------------------------------------------------
        
        # --------------------------------------------------------------
        #   Initialize - before iteration
        # --------------------------------------------------------------
        initialize = self.process.initialize
        
        initialize.expand_state            = Methods.expand_state
        initialize.differentials           = Methods.Common.Numerics.initialize_differentials_dimensionless
        initialize.conditions              = Methods.Ground.Idle.initialize_conditions

        # --------------------------------------------------------------
        #   Converge - starts iteration
        # --------------------------------------------------------------
        converge = self.process.converge
        
        converge.converge_root             = Methods.converge_root        

        # --------------------------------------------------------------
        #   Iterate - this is iterated
        # --------------------------------------------------------------
        iterate = self.process.iterate
        
        # Update Initials
        iterate.initials = Process()
        iterate.initials.time              = Methods.Common.Frames.initialize_time 
     
        # Unpack Unknowns
        iterate.unknowns = Process()
        iterate.unknowns.mission           = Methods.Ground.Idle.unpack_unknowns
    
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials   = Methods.Common.Numerics.update_differentials_time 
        iterate.conditions.propulsion      = Methods.Common.Energy.update_battery
        
        # --------------------------------------------------------------
        #   Finalize - after iteration
        # --------------------------------------------------------------
        finalize = self.process.finalize
        
        # Post Processing
        finalize.post_process = Process()        
        finalize.post_process.inertial_position = Methods.Ground.Idle.update_battery_age
        
        return

