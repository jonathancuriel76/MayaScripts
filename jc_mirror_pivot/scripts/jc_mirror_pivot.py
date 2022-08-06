'''
Name: jc_mirror_pivot.py

Author: Jonathan Curiel

Email: jonathancuriel76@gmail.com

Description: 
This script will allow you to mirror a mesh from its pivot, with the options to
make a copy and combine. 

Instructions: 
Place script into your maya/<version>/prefs/scripts directory.
Place icons into your maya/<version>/prefs/icons directory.
Use the icon mirror_pivot.bmp for your shelf if you'd like.

Shelf Command: To launch the EZKey UI, use these commands -
import jc_mirror_pivot
jc_mirror_pivot.mirror_pivot_ui()

'''

import maya.cmds as cmds

# function to execute the mirror
def mirror_pivot(axis):
    
    # query the checkbox values for duplicating
    dup_check_value = cmds.checkBoxGrp("dc_checkbox_grp", query=True, v1=True)
    combine_check_value = cmds.checkBoxGrp("dc_checkbox_grp", query=True, v2=True)
    
    if dup_check_value == True:
       if axis == "x":
           mirror_dup(".scaleX", combine_check_value)
       elif axis == "y":
           mirror_dup(".scaleY", combine_check_value)
       else:
           mirror_dup(".scaleZ", combine_check_value)
    else:
        if axis == "x":
            mirror(".scaleX")
        elif axis == "y":
            mirror(".scaleY")
        else:
            mirror(".scaleZ")
            

# duplicate and mirror function and check to combine              
def mirror_dup(scale_axis, combine_value):
    selected_objs = cmds.ls(sl=True)
    dup_counter = []
    for obj in selected_objs:
        cmds.select(obj)
        cmds.makeIdentity(apply=True, translate=0, rotate=0, scale=1)
        cmds.Duplicate()
        dup = cmds.ls(sl=True)
        dup_counter.append(dup[0])
        cmds.setAttr(dup[0]+scale_axis, -1)
        cmds.makeIdentity(apply=True, translate=0, rotate=0, scale=1)
        cmds.ReversePolygonNormals()
        op_var = cmds.getAttr(dup[0]+scale_axis)
        if op_var == 1:
            cmds.setAttr(dup[0] + ".opposite", 0)
        cmds.select(dup[0])
        if combine_value == True:
            world_loc = cmds.xform(query=True, ws=True, sp=True)
            cmds.select(obj, add=True)
            cmds.polyUnite(obj, dup[0], ch=False)
            cmds.rename(obj)
            combined = cmds.ls(sl=True)
            cmds.polyMergeVertex(d=0.0001)
            cmds.select(combined[0])
            cmds.delete(all=True, constructionHistory=True)
            cmds.xform(ws=True, sp=(world_loc[0], world_loc[1], world_loc[2]), rp=(world_loc[0], world_loc[1], world_loc[2]))
        
# mirror only function
def mirror(scale_axis):
    selected_objs = cmds.ls(sl=True)
    for obj in selected_objs:
        cmds.select(obj)
        cmds.makeIdentity(apply=True, translate=0, rotate=0, scale=1)
        cmds.setAttr(obj+scale_axis, -1)
        cmds.makeIdentity(apply=True, translate=0, rotate=0, scale=1)
        cmds.ReversePolygonNormals()
        op_var = cmds.getAttr(obj + ".opposite")
        if op_var == 1:
            cmds.setAttr(obj + ".opposite", 0)
        cmds.select(obj)

# function to build the simple UI
def mirror_pivot_ui():
    if cmds.window("mirror_pivot_ui", exists=True):
        cmds.deleteUI("mirror_pivot_ui")
        
    cmds.window("mirror_pivot_ui", title="Mirror Pivot", mnb=False, mxb=False, width=190, height=100, sizeable=False)
    cmds.columnLayout("cbg_column_layout")
    cmds.separator("separator", height=3, style="none")
    cmds.checkBoxGrp("dc_checkbox_grp", numberOfCheckBoxes=2, labelArray2=["Duplicate", "Combine"], )
    cmds.setParent("..")
    
    cmds.rowLayout("btn_row_layout",
                   numberOfColumns=5,
                   columnAttach5=["both", "both", "both", "both", "both"],
                   columnAlign5=["center", "center", "center", "center", "center"],
                   columnWidth5=[60, 60, 60, 60, 60])
    cmds.button("x_button", label="- X -", height=60, command=lambda *args:mirror_pivot("x"))
    cmds.button("y_button", label="- Y -", height=60, command=lambda *args:mirror_pivot("y"))
    cmds.button("z_button", label="- Z -", height=60, command=lambda *args:mirror_pivot("z"))
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.showWindow("mirror_pivot_ui")