# -*- coding: utf-8 -*-

"""
This final example brings everything together.
It demonstrates how to:
1. Create complex shapes using the techniques from previous lessons.
2. Visualize those shapes in a 3D viewer window.

We will create the 'box with a hole' and display it.
"""

# 1. Import all necessary modules
# Modeling
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

# Visualization
# `init_display` is a key function that sets up the viewer.
from OCC.Display.SimpleGui import init_display

def create_box_with_hole():
    """Creates the shape from the BRepAlgoAPI lesson."""
    the_box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), gp_Pnt(100, 100, 100)).Shape()
    the_sphere = BRepPrimAPI_MakeSphere(gp_Pnt(50, 50, 50), 30).Shape()
    result_shape = BRepAlgoAPI_Cut(the_box, the_sphere).Shape()
    return result_shape

if __name__ == '__main__':
    # 2. Initialize the viewer
    # This function creates a Qt window and returns a handle to the display context.
    display, start_display, add_menu, add_function_to_menu = init_display()
    print("Viewer initialized. A new window should appear.")

    # 3. Create the shape to be displayed
    my_shape = create_box_with_hole()

    # 4. Display the shape
    # `DisplayShape` is the core function to show a shape.
    # - `update=True` tells the viewer to re-render the scene immediately.
    # - `color` can be specified by name.
    # - `transparency` is a float between 0.0 (opaque) and 1.0 (fully transparent).
    display.DisplayShape(my_shape, update=True, color="blue", transparency=0.5)
    
    # You can display multiple shapes
    # display.DisplayShape(another_shape, color="red")

    print("Shape displayed. Please interact with the 3D window.")
    print("You need to manually close the window to end the script.")

    # 5. Start the viewer's event loop
    # This will open the window and make it responsive to mouse and keyboard events.
    start_display()

    # The script will pause here until the user closes the viewer window.
    print("Viewer window closed. Script finished.")
