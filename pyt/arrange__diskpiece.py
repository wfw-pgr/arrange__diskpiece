import numpy as np
import os, sys
import gmsh
import nkUtilities.load__constants as lcn


# ========================================================= #
# ===  arrange__diskpiece.py                            === #
# ========================================================= #
def arrange__diskpiece():

    voluDim     = 3
    cnsFile     = "dat/parameter.conf"
    const       = lcn.load__constants( inpFile=cnsFile )
    
    xc, yc, zc  = 0.0, 0.0, 0.0
    dx, dy, dz  = 0.0, 0.0, const["z_thick"]
    r_inner     = const["r_inner"]
    r_outer     = const["r_outer"]

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ const["nut_xMin"], const["nut_xMax"], const["nut_Nx"] ]
    x2MinMaxNum = [ const["nut_yMin"], const["nut_yMax"], const["nut_Ny"] ]
    x3MinMaxNum = [ const["nut_zpos"], const["nut_zpos"],               1 ]
    center_pos  = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )

    for inut in range( center_pos.shape[0] ):
        xc,yc,zc    = center_pos[inut,:]
        disk1       = gmsh.model.occ.addCylinder( xc,yc,zc, dx,dy,dz, r_outer )
        disk2       = gmsh.model.occ.addCylinder( xc,yc,zc, dx,dy,dz, r_inner )
        target,tool = [(voluDim,disk1)], [(voluDim,disk2)]
        disk3       = gmsh.model.occ.cut( target, tool )
    return()

    


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] initialization of the gmsh            --- #
    # ------------------------------------------------- #
    gmsh.initialize()
    gmsh.option.setNumber( "General.Terminal", 1 )
    gmsh.option.setNumber( "Mesh.Algorithm"  , 1 )
    gmsh.option.setNumber( "Mesh.Algorithm3D", 1 )
    gmsh.option.setNumber( "Mesh.SubdivisionAlgorithm", 1 )
    gmsh.model.add( "model" )
    
    
    # ------------------------------------------------- #
    # --- [2] Modeling                              --- #
    # ------------------------------------------------- #

    arrange__diskpiece()
    
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()


    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    
    gmsh.option.setNumber( "Mesh.CharacteristicLengthMin", 0.001 )
    gmsh.option.setNumber( "Mesh.CharacteristicLengthMax", 0.001 )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/model.msh" )
    gmsh.write( "msh/model.stp" )
    gmsh.finalize()
    
