## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift
# compute_induced_velocity_matrix.py
# 
# Created:  May 2018, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports
import SUAVE
import numpy as np
from SUAVE.Core import Units , Data

## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift
def compute_induced_velocity_matrix(data,n_sw,n_cw,theta_w):
    
    
    # unpack 
    ones = np.atleast_3d(np.ones_like(theta_w))
    XAH  = np.atleast_3d(data.XAH*ones)
    YAH  = np.atleast_3d(data.YAH*ones)
    ZAH  = np.atleast_3d(data.ZAH*ones)
    XBH  = np.atleast_3d(data.XBH*ones)
    YBH  = np.atleast_3d(data.YBH*ones)
    ZBH  = np.atleast_3d(data.ZBH*ones)

    XA1  = np.atleast_3d(data.XA1*ones)
    YA1  = np.atleast_3d(data.YA1*ones)
    ZA1  = np.atleast_3d(data.ZA1*ones)
    XA2  = np.atleast_3d(data.XA2*ones)
    YA2  = np.atleast_3d(data.YA2*ones)
    ZA2  = np.atleast_3d(data.ZA2*ones)
          
    XB1  = np.atleast_3d(data.XB1*ones)
    YB1  = np.atleast_3d(data.YB1*ones)
    ZB1  = np.atleast_3d(data.ZB1*ones)
    XB2  = np.atleast_3d(data.XB2*ones)
    YB2  = np.atleast_3d(data.YB2*ones)
    ZB2  = np.atleast_3d(data.ZB2*ones)
          
    XAC  = np.atleast_3d(data.XAC*ones)
    YAC  = np.atleast_3d(data.YAC*ones)
    ZAC  = np.atleast_3d(data.ZAC*ones)
    XBC  = np.atleast_3d(data.XBC*ones)
    YBC  = np.atleast_3d(data.YBC*ones)
    ZBC  = np.atleast_3d(data.ZBC*ones)
    XC   = np.atleast_3d(data.XC*ones)
    YC   = np.atleast_3d(data.YC*ones) 
    ZC   = np.atleast_3d(data.ZC*ones)  
    n_w  = data.n_w
    
    theta_w =  np.atleast_3d(theta_w) 
    n_aoa   = np.shape(theta_w)[0]
    
    # ---------------------------------------------------------------------------------------
    # Compute velocity induced by horseshoe vortex segments on every control point by every panel
    # --------------------------------------------------------------------------------------- 
    n_cp     = n_w*n_cw*n_sw # total number of control points 

    # Make all the hats
    n_cw_1   = n_cw-1
    XC_hats  = np.atleast_3d(np.cos(theta_w)*XC + np.sin(theta_w)*ZC)
    YC_hats  = np.atleast_3d(YC)
    ZC_hats  = np.atleast_3d(-np.sin(theta_w)*XC + np.cos(theta_w)*ZC)

    XA2_hats = np.atleast_3d(np.cos(theta_w)*XA2[:,:,n_cw_1::n_cw]   + np.sin(theta_w)*ZA2[:,:,n_cw_1::n_cw])
    YA2_hats = np.atleast_3d(YA2[:,:,n_cw_1::n_cw])
    ZA2_hats = np.atleast_3d(-np.sin(theta_w)*XA2[:,:,n_cw_1::n_cw]  + np.cos(theta_w)*ZA2[:,:,n_cw_1::n_cw])
    
    XB2_hats = np.atleast_3d(np.cos(theta_w)*XB2[:,:,n_cw_1::n_cw]   + np.sin(theta_w)*ZB2[:,:,n_cw_1::n_cw])
    YB2_hats = np.atleast_3d(YB2[:,:,n_cw_1::n_cw]) 
    ZB2_hats = np.atleast_3d(-np.sin(theta_w)*XB2[:,:,n_cw_1::n_cw]  + np.cos(theta_w)*ZB2[:,:,n_cw_1::n_cw])
    
    # Expand out the hats to be of length n instead of n_sw
    XA2_hats = np.atleast_3d(np.repeat(XA2_hats,n_cw,axis=2))
    YA2_hats = np.atleast_3d(np.repeat(YA2_hats,n_cw,axis=2))
    ZA2_hats = np.atleast_3d(np.repeat(ZA2_hats,n_cw,axis=2))
    XB2_hats = np.atleast_3d(np.repeat(XB2_hats,n_cw,axis=2))
    YB2_hats = np.atleast_3d(np.repeat(YB2_hats,n_cw,axis=2))
    ZB2_hats = np.atleast_3d(np.repeat(ZB2_hats,n_cw,axis=2))
    
    # If YBH is negative, flip A and B, ie negative side of the airplane. Vortex order flips
    boolean = YBH<0.
    XA1[boolean], XB1[boolean] = XB1[boolean], XA1[boolean]
    YA1[boolean], YB1[boolean] = YB1[boolean], YA1[boolean]
    ZA1[boolean], ZB1[boolean] = ZB1[boolean], ZA1[boolean]
    XA2[boolean], XB2[boolean] = XB2[boolean], XA2[boolean]
    YA2[boolean], YB2[boolean] = YB2[boolean], YA2[boolean]
    ZA2[boolean], ZB2[boolean] = ZB2[boolean], ZA2[boolean]    
    XAH[boolean], XBH[boolean] = XBH[boolean], XAH[boolean]
    YAH[boolean], YBH[boolean] = YBH[boolean], YAH[boolean]
    ZAH[boolean], ZBH[boolean] = ZBH[boolean], ZAH[boolean]
    
    XA2_hats[boolean], XB2_hats[boolean] = XB2_hats[boolean], XA2_hats[boolean]
    YA2_hats[boolean], YB2_hats[boolean] = YB2_hats[boolean], YA2_hats[boolean]
    ZA2_hats[boolean], ZB2_hats[boolean] = ZB2_hats[boolean], ZA2_hats[boolean]
    
    # Transpose thing
    #XA1 = np.swapaxes(XA1,1,2)
    #YA1 = np.swapaxes(YA1,1,2)
    #ZA1 = np.swapaxes(ZA1,1,2)
    #XB1 = np.swapaxes(XB1,1,2)
    #YB1 = np.swapaxes(YB1,1,2)
    #ZB1 = np.swapaxes(ZB1,1,2)  
    #XA2 = np.swapaxes(XA2,1,2)
    #YA2 = np.swapaxes(YA2,1,2)
    #ZA2 = np.swapaxes(ZA2,1,2)    
    #XB2 = np.swapaxes(XB2,1,2)
    #YB2 = np.swapaxes(YB2,1,2)
    #ZB2 = np.swapaxes(ZB2,1,2)     
       
    #XA2_hats = np.swapaxes(XA2_hats,1,2)
    #YA2_hats = np.swapaxes(YA2_hats,1,2)
    #ZA2_hats = np.swapaxes(ZA2_hats,1,2)
    #XB2_hats = np.swapaxes(XB2_hats,1,2)
    #YB2_hats = np.swapaxes(YB2_hats,1,2)
    #ZB2_hats = np.swapaxes(ZB2_hats,1,2)    
    
    XC = np.swapaxes(XC,1,2) 
    YC = np.swapaxes(YC,1,2) 
    ZC = np.swapaxes(ZC,1,2) 
    
    XC_hats = np.swapaxes(XC_hats,1,2) 
    YC_hats = np.swapaxes(YC_hats,1,2) 
    ZC_hats = np.swapaxes(ZC_hats,1,2)     
    
    # compute influence of bound vortices 
    C_AB_bv = np.transpose(vortex(XC, YC, ZC, XAH, YAH, ZAH, XBH, YBH, ZBH),axes=[1,2,3,0])

    # compute influence of 3/4 left legs
    C_AB_34_ll = np.transpose(vortex(XC, YC, ZC, XA2, YA2, ZA2, XAH, YAH, ZAH),axes=[1,2,3,0])

    # compute influence of whole panel left legs 
    C_AB_ll   =  np.transpose(vortex(XC, YC, ZC, XA2, YA2, ZA2, XA1, YA1, ZA1),axes=[1,2,3,0])

    # compute influence of 3/4 right legs
    C_AB_34_rl = np.transpose(vortex(XC, YC, ZC, XBH, YBH, ZBH, XB2, YB2, ZB2),axes=[1,2,3,0])

    # compute influence of whole right legs 
    C_AB_rl = np.transpose(vortex(XC, YC, ZC, XB1, YB1, ZB1, XB2, YB2, ZB2),axes=[1,2,3,0])

    # velocity induced by left leg of vortex (A to inf)
    C_Ainf  = np.transpose(vortex_to_inf_l(XC_hats, YC_hats, ZC_hats, XA2_hats, YA2_hats, ZA2_hats,theta_w),axes=[1,2,3,0])

    # velocity induced by right leg of vortex (B to inf)
    C_Binf  = np.transpose(vortex_to_inf_r(XC_hats, YC_hats, ZC_hats, XB2_hats, YB2_hats, ZB2_hats,theta_w),axes=[1,2,3,0])
                
    # Add the right and left influences seperateky
    C_AB_llrl_roll = C_AB_ll+C_AB_rl
    
    # Prime the arrays
    mask      = np.ones((n_aoa,n_cp,n_cp,3))
    C_AB_llrl = np.zeros((n_aoa,n_cp,n_cp,3))

    for idx in range(n_cw-1):    
        
        # Make a mask
        mask[:,n_cw-idx-1::n_cw,:]= np.zeros_like(mask[:,n_cw-idx-1::n_cw,:])  
        
        # Roll it over to the next component
        C_AB_llrl_roll = np.roll(C_AB_llrl_roll,-1,axis=1)   
        
        # Add in the components that we need
        C_AB_llrl = C_AB_llrl+ C_AB_llrl_roll*mask

    # Add all the influences together
    C_mn = C_AB_34_ll + C_AB_bv + C_AB_34_rl + C_Ainf + C_Binf + C_AB_llrl
    
    return C_mn

# -------------------------------------------------------------------------------
# vortex strength computation
# -------------------------------------------------------------------------------
def vortex(X,Y,Z,X1,Y1,Z1,X2,Y2,Z2):
    R1R2X  =   (Y-Y1)*(Z-Z2) - (Z-Z1)*(Y-Y2) 
    R1R2Y  = -((X-X1)*(Z-Z2) - (Z-Z1)*(X-X2))
    R1R2Z  =   (X-X1)*(Y-Y2) - (Y-Y1)*(X-X2)
    SQUARE = R1R2X**2 + R1R2Y**2 + R1R2Z**2
    R1     = np.sqrt((X-X1)**2 + (Y-Y1)**2 + (Z-Z1)**2)
    R2     = np.sqrt((X-X2)**2 + (Y-Y2)**2 + (Z-Z2)**2)
    R0R1   = (X2-X1)*(X-X1) + (Y2-Y1)*(Y-Y1) + (Z2-Z1)*(Z-Z1)
    R0R2   = (X2-X1)*(X-X2) + (Y2-Y1)*(Y-Y2) + (Z2-Z1)*(Z-Z2)
    RVEC   = np.array([R1R2X,R1R2Y,R1R2Z])
    COEF   = (1/(4*np.pi))*(RVEC/SQUARE) * (R0R1/R1 - R0R2/R2)
    return COEF

def vortex_to_inf_l(X,Y,Z,X1,Y1,Z1,tw): 
    DENUM =  (Z-Z1)**2 + (Y1-Y)**2
    XVEC  = -(Y1-Y)*np.sin(tw)/DENUM
    YVEC  =  (Z-Z1)/DENUM
    ZVEC  =  (Y1-Y)*np.cos(tw)/DENUM
    BRAC  =  1 + ((X-X1) / (np.sqrt((X-X1)**2+ (Y-Y1)**2+ (Z-Z1)**2)))
    RVEC   = np.array([XVEC, YVEC, ZVEC])
    COEF  = (1/(4*np.pi))*RVEC*BRAC         
    return COEF

def vortex_to_inf_r(X,Y,Z,X1,Y1,Z1,tw):
    DENUM =  (Z-Z1)**2 + (Y1-Y)**2
    XVEC  = (Y1-Y)*np.sin(tw)/DENUM
    YVEC  = -(Z-Z1)/DENUM
    ZVEC  = -(Y1-Y)*np.cos(tw)/DENUM
    BRAC  =  1 + ((X-X1) / (np.sqrt((X-X1)**2+ (Y-Y1)**2+ (Z-Z1)**2)))
    RVEC   = np.array([XVEC, YVEC, ZVEC])
    COEF  = (1/(4*np.pi))*RVEC*BRAC         
    return COEF