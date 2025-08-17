# -*- coding: utf-8 -*-

"""
Phase 1 Summary Example: Core Concepts

This script is a summary of the core concepts learned in Phase 1:
1.  `gp`: Used to define points for the box and sphere.
2.  `TopoDS`: The underlying structure for all shapes created.
3.  `BRepPrimAPI`: To create the primitive box and sphere shapes.
4.  `BRepAlgoAPI`: To perform the boolean CUT operation.
5.  `AIS` & `V3d`: To visualize the final result in a window.

This script creates a box with a spherical hole and displays it.
"""

# 1. Import all necessary modules
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Display.SimpleGui import init_display

def create_box_with_hole():
    """Creates the shape from the BRepAlgoAPI lesson."""
    the_box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), gp_Pnt(100, 100, 100)).Shape()
    the_sphere = BRepPrimAPI_MakeSphere(gp_Pnt(50, 50, 50), 30).Shape()
    result_shape = BRepAlgoAPI_Cut(the_box, the_sphere).Shape()
    return result_shape

if __name__ == '__main__':
    # 2. Initialize the viewer
    display, start_display, add_menu, add_function_to_menu = init_display()
    print("Viewer initialized for Phase 1 Summary Example.")

    # 3. Create the shape
    my_shape = create_box_with_hole()

    # 4. Display the shape
    display.DisplayShape(my_shape, update=True, color="cyan", transparency=0.2)
    
    print("Shape displayed. Please interact with the 3D window.")
    print("You need to manually close the window to end the script.")

    # 5. Start the viewer's event loop
    start_display()

    print("Viewer window closed. Script finished.")
