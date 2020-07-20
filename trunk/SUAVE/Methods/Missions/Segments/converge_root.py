## @ingroup Methods-Missions-Segments
# converge_root.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy.optimize
import numpy as np

from SUAVE.Core.Arrays import array_type

# ----------------------------------------------------------------------
#  Converge Root
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments
def converge_root(segment):
    """Interfaces the mission to a numerical solver. The solver may be changed by using root_finder.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment                            [Data]
    segment.settings.root_finder       [Data]
    state.numerics.tolerance_solution  [Unitless]

    Outputs:
    state.unknowns                     [Any]
    segment.state.numerics.converged   [Unitless]

    Properties Used:
    N/A
    """       
    
    unknowns = segment.state.unknowns.pack_array()
    
    # Find the normalization factor for the unknowns and normalize
    segment.state.unknowns_normalization_factor = 1*unknowns
    unknowns_in = unknowns/segment.state.unknowns_normalization_factor
    
    ## Run one iteration to get the scaling and normalize residuals
    segment.process.iterate(segment)
    res = segment.state.residuals.pack_array() 
    segment.state.residual_normalization_factor = 1/res
    #segment.state.residual_normalization_factor = np.multiply(segment.state.residuals.pack_array(),(np.random.random(np.shape(unknowns))+0.5))
    #segment.state.residual_normalization_factor[segment.state.residual_normalization_factor==0] = 1e-16

        
    
    try:
        root_finder = segment.settings.root_finder
    except AttributeError:
        root_finder = scipy.optimize.fsolve 
    
    if segment.use_Jacobian: 
        unknowns,infodict,ier,msg = root_finder( iterate,
                                             unknowns_in,
                                             args = segment,
                                             xtol = segment.state.numerics.tolerance_solution,
                                             fprime = FD_jacobian,
                                             maxfev = segment.state.numerics.max_evaluations,
                                             full_output = 1)
    else:
        unknowns,infodict,ier,msg = root_finder( iterate,
                                               unknowns_in,
                                               args = segment,
                                               xtol = segment.state.numerics.tolerance_solution,
                                               maxfev = segment.state.numerics.max_evaluations,
                                               full_output=1)        

    if ier!=1:
        print("Segment did not converge. Segment Tag: " + segment.tag)
        print("Error Message:\n" + msg)
        segment.state.numerics.converged = False
        segment.converged = False
    else:
        segment.state.numerics.converged = True
        segment.converged = True
         
    # store convergence results 
    segment.state.numerics.info_dict  = infodict
    segment.state.numerics.message    = msg

    return
    
# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments
def iterate(unknowns_in, segment):
    
    """Runs one iteration of of all analyses for the mission.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    state.unknowns                [Data]
    segment.process.iterate       [Data]

    Outputs:
    residuals                     [Unitless]

    Properties Used:
    N/A
    """       
    
    unknowns = unknowns_in*segment.state.unknowns_normalization_factor
    
    if isinstance(unknowns,array_type):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    segment.process.iterate(segment)
    
    residuals = segment.state.residuals.pack_array()
    
    residuals_normalized = residuals*segment.state.residual_normalization_factor    
        
    return residuals_normalized 
    
    #return residuals


## @ingroup Methods-Missions-Segments
def FD_jacobian(unknowns, segment):
    
    """Takes the jacobian of iterate using finite differencing

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    state.unknowns                [Data]
    segment.process.iterate       [Data]

    Outputs:
    jacobian                      [Unitless]

    Properties Used:
    N/A
    """
    
    length = len(unknowns)
    
    jacobian = np.zeros((length,length))
    H = 1e-8
    
    base_line = iterate(unknowns, segment)
    
    for ii in range(length):
        unk = unknowns*1.0
        
        unk[ii] = unk[ii]+H
        if isinstance(unk,array_type):
            segment.state.unknowns.unpack_array(unk)
        else:
            segment.state.unknowns = unk
            
        residuals = iterate(unknowns, segment)
        jacobian[:,ii] = (residuals-base_line)/H
        
    segment.state.numerics.jacobian_evaluations += 1
        
    return jacobian
