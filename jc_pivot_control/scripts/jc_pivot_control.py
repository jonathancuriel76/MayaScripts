'''
Name: jc_pivot_control.py
Author: Jonathan Curiel
Email: jonathancuriel76@gmail.com
Description: This script will allow you to move the pivot of the selected object using the simple UI.

Shelf Command: Use the following commands to import and run the script.
import jc_pivot_control
jc_pivot_control.pivot_control_ui()

Note: I've also included an icon for you to use for your shelf.
'''

import maya.cmds as cmds

# function to get bounds of the selected object

def get_bounds(obj_selected):
    # select the object passed
    cmds.select(obj_selected, replace=True)
     
    # query the bounding box using xform and store in a list
    get_bounds_list = cmds.xform(query=True, worldSpace=True, boundingBox=True)
    # calculate the averages between minimums and maximums
    # x_average = (xmax + xmin)/2 
    x_average = (get_bounds_list[3] + get_bounds_list[0])/2
    # y_average = (ymax + ymin)/2
    y_average = (get_bounds_list[4] + get_bounds_list[1])/2
    # z_average = (zmax + zmin)/2
    z_average = (get_bounds_list[5] + get_bounds_list[2])/2
    
    # append the averages and return the list
    # get_bounds_list(xmin, ymin, zmin, xmax, ymax, zmax, xavg, yavg, zavg)
    get_bounds_list.append(x_average)
    get_bounds_list.append(y_average)
    get_bounds_list.append(z_average)
    return get_bounds_list

# function to move pivots
def move_pivot_local(mode):
    sel = cmds.ls(sl=True, typ="transform")
    if len(sel) == 0:
        cmds.confirmDialog(title="Warning", message="Select at least one mesh.", button="OK")
    else:
        for s in sel:
            # get the bounds of each selected item
            pos = get_bounds(s)
            # check which 'mode' was passed from the button press and move the pivot
            if mode == "center":
                cmds.CenterPivot(s)
            elif mode == "origin":
                cmds.move(0, 0, 0, s+".rotatePivot", s+".scalePivot", a=True, rpr=True)
            elif mode == "xmin":
                cmds.move(pos[0], pos[7], pos[8], s+".rotatePivot", s+".scalePivot", a=True, rpr=True)
            elif mode == "ymin":
                cmds.move(pos[6], pos[1], pos[8], s+".rotatePivot", s+".scalePivot", a=True, rpr=True)
            elif mode == "zmin":
                cmds.move(pos[6], pos[7], pos[2], s+".rotatePivot", s+".scalePivot", a=True, rpr=True)
            elif mode == "xmax":
                cmds.move(pos[3], pos[7], pos[8], s+".rotatePivot", s+".scalePivot", a=True, rpr=True)
            elif mode == "ymax":
                cmds.move(pos[6], pos[4], pos[8], s+".rotatePivot", s+".scalePivot", a=True, rpr=True)
            elif mode == "zmax":
                cmds.move(pos[6], pos[7], pos[5], s+".rotatePivot", s+".scalePivot", a=True, rpr=True)

# function to move pivot of all selected objects to that of the last selected object                
def move_pivot_object(*args):
    sel = cmds.ls(sl=True, typ="transform")
    if len(sel) < 2:
        cmds.confirmDialog(title="Warning", message="Select at least two objects.", button="OK")
    else:
        sel_last = cmds.ls(sl=True, tail=1)
        sel_last_copy = sel_last[0]
        cmds.select(sel_last_copy, deselect=True)
        sel_set = cmds.ls(sl=True, typ="transform")
        pivot_sel = cmds.xform(sel_last_copy, query=True, piv=True, ws=True)
        for s in sel_set:
            cmds.move(pivot_sel[0], pivot_sel[1], pivot_sel[2], s+".rotatePivot", s+".scalePivot", a=True)
        
        
# function to build the ui                    
def pivot_control_ui():
    # check if window already exists
    if cmds.window("pivot_control_main", exists=True):
        cmds.deleteUI("pivot_control_main")
    
    cmds.window("pivot_control_main", rtf=True, t="Pivot Control", mnb=False, mxb=False, w=180, h=72)
    cmds.columnLayout("main_column_layout", adjustableColumn=True, rowSpacing=0)
    cmds.text(l="Move Pivot To:")
    cmds.gridLayout("button_grid_layout", cwh=(60, 24), nrc=(3, 3))
    # max buttons
    cmds.button("xmax", l="X Max", c=lambda *args:move_pivot_local("xmax"))
    cmds.button("ymax", l="Y Max", c=lambda *args:move_pivot_local("ymax"))
    cmds.button("zmax", l="Z Max", c=lambda *args:move_pivot_local("zmax"))
    # min buttons
    cmds.button("xmin", l="X Min", c=lambda *args:move_pivot_local("xmin"))
    cmds.button("ymin", l="Y Min", c=lambda *args:move_pivot_local("ymin"))
    cmds.button("zmin", l="Z Min", c=lambda *args:move_pivot_local("zmin"))
    # center, origin and last selected, which
    # sets the pivot of all selected object to that of the last selected object
    cmds.button("center", l="Center", c=lambda *args:move_pivot_local("center"))
    cmds.button("origin", l="Origin", c=lambda *args:move_pivot_local("origin"))
    cmds.button("selected", l="Selected", c=move_pivot_object)
    cmds.showWindow("pivot_control_main")

# call ui function for local testing   
#pivot_control_ui()