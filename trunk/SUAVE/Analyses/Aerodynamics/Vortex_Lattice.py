## @ingroup Analyses-Aerodynamics
# Vortex_Lattice.py
#
# Created:  Nov 2013, T. Lukaczyk
# Modified:     2014, T. Lukaczyk, A. Variyar, T. Orra
#           Feb 2016, A. Wendorff
#           Apr 2017, T. MacDonald
#           Nov 2017, E. Botero


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# SUAVE imports
import SUAVE

from SUAVE.Core import Data
from SUAVE.Core import Units

from SUAVE.Methods.Aerodynamics.Common.Fidelity_Zero.Lift import weissinger_wing_VLM , weissinger_vehicle_VLM

# local imports
from .Aerodynamics import Aerodynamics

# package imports
import numpy as np


# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics
class Vortex_Lattice(Aerodynamics):
    """This builds a surrogate and computes lift using a basic vortex lattice.

    Assumptions:
    None

    Source:
    None
    """ 

    def __defaults__(self):
        """This sets the default values and methods for the analysis.

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
        self.tag = 'Vortex_Lattice'

        self.geometry = Data()
        self.settings = Data()

        # correction factors
        self.settings.fuselage_lift_correction           = 1.14
        self.settings.trim_drag_correction_factor        = 1.02
        self.settings.wing_parasite_drag_form_factor     = 1.1
        self.settings.fuselage_parasite_drag_form_factor = 2.3
        self.settings.aircraft_span_efficiency_factor    = 0.78
        self.settings.drag_coefficient_increment         = 0.0000

        # vortex lattice configurations
        self.settings.number_panels_spanwise = 5

        # conditions table, used for surrogate model training
        self.training = Data()        
        self.training.angle_of_attack  = np.array([-10.,-5.,0.,5.,10.]) * Units.deg
        self.training.lift_coefficient = None
        self.training.induced_drag_coefficient = None
        self.training.wing_lift_coefficients = None
        
        # surrogoate models
        self.surrogates = Data()
        self.surrogates.lift_coefficient = None
        self.surrogates.induced_drag_coefficient = None
        self.surrogates.wing_lift_coefficients = None
 
        
    def initialize(self):
        """Drives functions to get training samples and build a surrogate.

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
        # sample training data
        self.sample_training()
                    
        # build surrogate
        self.build_surrogate()


    def evaluate(self,state,settings,geometry):
        """Evaluates lift and drag using available surrogates.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        state.conditions.
          freestream.dynamics_pressure       [-]
          angle_of_attack                    [radians]

        Outputs:
        conditions.aerodynamics.lift_breakdown.
          inviscid_wings_lift[wings.*.tag]   [-] CL (wing specific)
          inviscid_wings_lift.total          [-] CL
          inviscid_wings_drag.total          [-] CDi
        conditions.aerodynamics.
          lift_coefficient_wing              [-] CL (wing specific)
        inviscid_wings_lift                  [-] CL

        Properties Used:
        self.surrogates.
          lift_coefficient                   [-] CL
          induced_drag_coefficient           [-] CDi
          wing_lift_coefficient[wings.*.tag] [-] CL (wing specific)
        """          
        """ process vehicle to setup geometry, condititon and settings
            Inputs:
                conditions - DataDict() of aerodynamic conditions
            Outputs:
                CL - array of lift coefficients, same size as alpha
                CD - array of drag coefficients, same size as alpha
            Assumptions:
                linear intperolation surrogate model on Mach, Angle of Attack
                    and Reynolds number
                locations outside the surrogate's table are held to nearest data
                no changes to initial geometry or settings
        """

        # unpack

        surrogates = self.surrogates        
        conditions = state.conditions
        
        # unpack        
        q    = conditions.freestream.dynamic_pressure
        AoA  = conditions.aerodynamics.angle_of_attack
        Sref = geometry.reference_area
        
        wings_lift_model         = surrogates.lift_coefficient
        wings_induced_drag_model = surrogates.induced_drag_coefficient
        
        # inviscid lift of wings only        
        inviscid_wings_lift                                              = Data()
        inviscid_wings_lift.total                                        = wings_lift_model(AoA)        
        inviscid_wings_drag                                              = wings_induced_drag_model(AoA)
        
        conditions.aerodynamics.lift_breakdown.inviscid_wings_lift       = Data()
        conditions.aerodynamics.lift_breakdown.inviscid_wings_lift.total = inviscid_wings_lift.total
        conditions.aerodynamics.lift_coefficient                         = inviscid_wings_lift.total
        conditions.aerodynamics.drag_breakdown.induced                   = Data()
        conditions.aerodynamics.drag_breakdown.induced.total             = inviscid_wings_drag
        
        # store model for lift coefficients of each wing
        conditions.aerodynamics.lift_coefficient_wing             = Data()      

        for wing in geometry.wings.keys():
            wings_lift_model = surrogates.wing_lift_coefficients[wing]
            inviscid_wings_lift[wing] = wings_lift_model(AoA)
            conditions.aerodynamics.lift_breakdown.inviscid_wings_lift[wing] = inviscid_wings_lift[wing]
            state.conditions.aerodynamics.lift_coefficient_wing[wing]        = inviscid_wings_lift[wing]

        return inviscid_wings_lift


    def sample_training(self):
        """Call methods to run vortex lattice for sample point evaluation.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        see properties used

        Outputs:
        self.training.
          lift_coefficient            [-] 
          wing_lift_coefficients      [-] (wing specific)

        Properties Used:
        self.geometry.wings.*.tag
        self.settings                 (passed to calculate vortex lattice)
        self.training.angle_of_attack [radians]
        """        
        # unpack
        geometry = self.geometry
        settings = self.settings
        training = self.training
        
        AoA = training.angle_of_attack
        CL  = np.zeros_like(AoA)
        CDi = np.zeros_like(AoA)
        
        wing_CLs = Data()
        wing_CDis = Data()
        for wing in geometry.wings.values():
            wing_CLs[wing.tag]  = np.zeros_like(AoA)
            wing_CDis[wing.tag] = np.zeros_like(AoA)

        # condition input, local, do not keep
        konditions              = Data()
        konditions.aerodynamics = Data()

        # calculate aerodynamics for table
        for i,_ in enumerate(AoA):
            
            # overriding conditions, thus the name mangling
            konditions.aerodynamics.angle_of_attack = AoA[i]
            
            # these functions are inherited from Aerodynamics() or overridden
            CL[i],CDi[i], wing_lifts, wing_induced_drags = calculate_lift_vortex_lattice(konditions, settings, geometry)
            for wing in geometry.wings.values():
                wing_CLs[wing.tag][i]  = wing_lifts[wing.tag]
                wing_CDis[wing.tag][i] = wing_induced_drags[wing.tag]

        # store training data 
        training.lift_coefficient = CL
        training.induced_drag_coefficient = CDi
        training.wing_lift_coefficients = wing_CLs

        return

    def build_surrogate(self):
        """Build a surrogate using sample evaluation results.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        see properties used

        Outputs:
        self.surrogates.
          lift_coefficient       <np.poly1d>
          wing_lift_coefficients <np.poly1d> (multiple surrogates)

        Properties Used:
        self.
          training.
            angle_of_attack        [radians]
            lift_coefficient       [-]
            wing_lift_coefficients [-] (wing specific)
        """        
        # unpack data
        training = self.training
        AoA_data = training.angle_of_attack
        CL_data  = training.lift_coefficient
        CDi_data = training.induced_drag_coefficient
        wing_CL_data = training.wing_lift_coefficients

        # pack for surrogate model
        X_data = np.array([AoA_data]).T
        X_data = np.reshape(X_data,-1)
        
        # learn the model
        cl_surrogate = np.poly1d(np.polyfit(X_data, CL_data ,1))
        cdi_surrogate = np.poly1d(np.polyfit(X_data, CDi_data ,1))
        
        wing_cl_surrogates = Data()        
        for wing in wing_CL_data.keys():
            wing_cl_surrogates[wing] = np.poly1d(np.polyfit(X_data, wing_CL_data[wing] ,1))

        self.surrogates.lift_coefficient = cl_surrogate
        self.surrogates.induced_drag_coefficient = cdi_surrogate
        self.surrogates.wing_lift_coefficients = wing_cl_surrogates

        return



# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------


def calculate_lift_vortex_lattice(conditions,settings,geometry):
    """Calculate the total vehicle lift coefficient and specific wing coefficients (with specific wing reference areas)
    using a vortex lattice method.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    conditions                      (passed to vortex lattice method)
    settings                        (passed to vortex lattice method)
    geometry.reference_area         [m^2]
    geometry.wings.*.reference_area (each wing is also passed to the vortex lattice method)

    Outputs:
    

    Properties Used:
    
    """            

    # unpack
    vehicle_reference_area = geometry.reference_area
    
    # compute lift of entire vehicle 
    
    # iterate over wings 
    wing_lifts = Data()
    wing_induced_drag = Data()
    for wing in geometry.wings.values():
        [wing_lift_coeff,wing_drag_coeff] = weissinger_wing_VLM(conditions,settings,wing)
        wing_lifts[wing.tag] = wing_lift_coeff
        wing_induced_drag[wing.tag] = wing_drag_coeff

    [total_lift_coeff,totat_induced_drag_coeff] = weissinger_vehicle_VLM(conditions,settings,geometry)

    return total_lift_coeff,totat_induced_drag_coeff, wing_lifts , wing_induced_drag
