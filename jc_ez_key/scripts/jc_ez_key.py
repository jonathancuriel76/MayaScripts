'''
Name: jc_ez_key.py

Author: Jonathan Curiel

Email: jonathancuriel76@gmail.com

Description: 
This script will allow you to set and remove keyframes on the default tranform nodes 
(translate, rotate, scale) using a simple interface.

Instructions: 
Place script into your maya/<version>/prefs/scripts directory.
Place icons into your maya/<version>/prefs/icons directory.

Shelf Command: To launch the EZKey UI, use these commands -
import jc_ez_key
jc_ez_key.ez_key_ui()

'''

import maya.cmds as cmds
from functools import partial

# create the ezkey ui
def ez_key_ui():
    # icon paths
    icon_del_all = cmds.internalVar(upd=True) + "icons/ez_all_delete.bmp"
    icon_add_all = cmds.internalVar(upd=True) + "icons/ez_all.bmp"
    icon_del_x = cmds.internalVar(upd=True) + "icons/ez_x_delete.bmp"
    icon_add_x = cmds.internalVar(upd=True) + "icons/ez_x.bmp"
    icon_del_y = cmds.internalVar(upd=True) + "icons/ez_y_delete.bmp"
    icon_add_y = cmds.internalVar(upd=True) + "icons/ez_y.bmp"
    icon_del_z = cmds.internalVar(upd=True) + "icons/ez_z_delete.bmp"
    icon_add_z = cmds.internalVar(upd=True) + "icons/ez_z.bmp"
    
    if cmds.window("ez_key", exists=True):
        cmds.deleteUI("ez_key")
    
    win = cmds.window("ez_key", w=128, h=256, rtf=True, mnb=False, mxb=False, sizeable=False, title="EZKey")
    
    # define layout
    row_column = cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[1, 32])
    
    # x translate
    xt_btn = cmds.symbolButton(image=icon_add_x, c=partial(super_keyer, "add", "translateX"))
    xt_del_btn = cmds.symbolButton(image=icon_del_x, c=partial(super_keyer, "del", "translateX"))
    cmds.text(label="    Translate X    ")
    
    # y translate
    yt_btn = cmds.symbolButton(image=icon_add_y, c=partial(super_keyer, "add", "translateY"))
    yt_del_btn = cmds.symbolButton(image=icon_del_y, c=partial(super_keyer, "del", "translateY"))
    cmds.text(label="    Translate Y    ")
    
    # x translate
    zt_btn = cmds.symbolButton(image=icon_add_z, c=partial(super_keyer, "add", "translateZ"))
    zt_del_btn = cmds.symbolButton(image=icon_del_z, c=partial(super_keyer, "del", "translateZ"))
    cmds.text(label="    Translate Z    ")
    
    # all translate
    t_all_btn = cmds.symbolButton(image=icon_add_all, c=partial(super_keyer, "add_all", "translate"))
    t_del_btn = cmds.symbolButton(image=icon_del_all, c=partial(super_keyer, "del_all", "translate"))
    cmds.text(label="    All Translate    ")
    
    cmds.separator(style="in")
    cmds.separator(style="in")
    cmds.separator(style="in")
    
    # x rotate
    xr_btn = cmds.symbolButton(image=icon_add_x, c=partial(super_keyer, "add", "rotateX"))
    xr_del_btn = cmds.symbolButton(image=icon_del_x, c=partial(super_keyer, "del", "rotateX"))
    cmds.text(label="    Rotate X    ")
    
    # y rotate
    yr_btn = cmds.symbolButton(image=icon_add_y, c=partial(super_keyer, "add", "rotateY"))
    yr_del_btn = cmds.symbolButton(image=icon_del_y, c=partial(super_keyer, "del", "rotateY"))
    cmds.text(label="    Rotate Y    ")
    
    # x rotate
    zr_btn = cmds.symbolButton(image=icon_add_z, c=partial(super_keyer, "add", "rotateZ"))
    zr_del_btn = cmds.symbolButton(image=icon_del_z, c=partial(super_keyer, "del", "rotateZ"))
    cmds.text(label="    Rotate Z    ")
    
    # all rotate
    r_all_btn = cmds.symbolButton(image=icon_add_all, c=partial(super_keyer, "add_all", "rotate"))
    r_del_btn = cmds.symbolButton(image=icon_del_all, c=partial(super_keyer, "del_all", "rotate"))
    cmds.text(label="    All Rotate    ")
    
    cmds.separator(style="in")
    cmds.separator(style="in")
    cmds.separator(style="in")
    
    # x scale
    xs_btn = cmds.symbolButton(image=icon_add_x, c=partial(super_keyer, "add", "scaleX"))
    xs_del_btn = cmds.symbolButton(image=icon_del_x, c=partial(super_keyer, "del", "scaleX"))
    cmds.text(label="    Scale X    ")
    
    # y scale
    ys_btn = cmds.symbolButton(image=icon_add_y, c=partial(super_keyer, "add", "scaleY"))
    ys_del_btn = cmds.symbolButton(image=icon_del_y, c=partial(super_keyer, "del", "scaleY"))
    cmds.text(label="    Scale Y    ")
    
    # x scale
    zs_btn = cmds.symbolButton(image=icon_add_z, c=partial(super_keyer, "add", "scaleZ"))
    zs_del_btn = cmds.symbolButton(image=icon_del_z, c=partial(super_keyer, "del", "scaleZ"))
    cmds.text(label="    Scale Z    ")
    
    # all scale
    s_all_btn = cmds.symbolButton(image=icon_add_all, c=partial(super_keyer, "add_all", "scale"))
    s_del_btn = cmds.symbolButton(image=icon_del_all, c=partial(super_keyer, "del_all", "scale"))
    cmds.text(label="    All Scale    ")
    
    cmds.separator(style="in")
    cmds.separator(style="in")
    cmds.separator(style="in")
    
    # all transforms
    add_all_btn = cmds.symbolButton(image=icon_add_all, c=partial(super_keyer, "add_all", "transforms"))
    del_all_btn = cmds.symbolButton(image=icon_del_all, c=partial(super_keyer, "del_all", "transforms"))
    cmds.text(label="    All Transforms    ")  
    
    # show window
    cmds.showWindow(win)

# create the super keyer function
def super_keyer(operation, transform, *args):
    current_time = int(cmds.currentTime(query=True))
    sel = cmds.ls(selection=True)
    
    if len(sel) == 0:
        cmds.warning("Nothing selected to edit keyframe(s).")
    else:
        for item in sel:
            if operation == "add":
                cmds.setKeyframe(at=transform, itt="linear")
            elif operation == "del":
                cmds.cutKey(at=transform, t=(current_time, current_time))
            elif operation == "add_all" or operation == "del_all":
                if transform == "translate":
                    key_all_translate(operation, current_time)
                elif transform == "rotate":
                    key_all_rotate(operation, current_time)
                elif transform == "scale":
                    key_all_scale(operation, current_time)
                else:
                    key_all_transforms(operation, current_time)
            else:
                warning("Something went completely wrong. You should never see this")

def key_all_translate(op, time):
    if op == "add_all":
        cmds.setKeyframe(at="translateX", itt="linear")
        cmds.setKeyframe(at="translateY", itt="linear")
        cmds.setKeyframe(at="translateZ", itt="linear")
    else:
        cmds.cutKey(at="translateX", t=(time, time))
        cmds.cutKey(at="translateY", t=(time, time))
        cmds.cutKey(at="translateZ", t=(time, time))
    
def key_all_rotate(op, time):
    if op == "add_all":
        cmds.setKeyframe(at="rotateX", itt="linear")
        cmds.setKeyframe(at="rotateY", itt="linear")
        cmds.setKeyframe(at="rotateZ", itt="linear")
    else:
        cmds.cutKey(at="rotateX", t=(time, time))
        cmds.cutKey(at="rotateY", t=(time, time))
        cmds.cutKey(at="rotateZ", t=(time, time))
    
def key_all_scale(op, time):
    if op == "add_all":
        cmds.setKeyframe(at="scaleX", itt="linear")
        cmds.setKeyframe(at="scaleY", itt="linear")
        cmds.setKeyframe(at="scaleZ", itt="linear")
    else:
        cmds.cutKey(at="scaleX", t=(time, time))
        cmds.cutKey(at="scaleY", t=(time, time))
        cmds.cutKey(at="scaleZ", t=(time, time))

def key_all_transforms(op, time):
    key_all_translate(op, time)
    key_all_rotate(op, time)
    key_all_scale(op, time)