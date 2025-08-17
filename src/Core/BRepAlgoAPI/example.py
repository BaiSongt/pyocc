# -*- coding: utf-8 -*-

"""
This file demonstrates how to use the `BRepAlgoAPI` to perform boolean operations.
We will create a box and a sphere, and then use the `Cut` operation to subtract
the sphere from the box, effectively creating a hole.
"""

# Import necessary classes
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

def create_box_with_hole():
    """
    Creates a box and cuts a sphere from it.
    """
    print("--- Boolean Cut Operation Example ---")

    # 1. Create the first shape (the object): a box.
    box_p1 = gp_Pnt(0, 0, 0)
    box_p2 = gp_Pnt(100, 100, 100)
    make_box = BRepPrimAPI_MakeBox(box_p1, box_p2)
    make_box.Build()
    if not make_box.IsDone():
        print("Box construction failed.")
        return
    the_box = make_box.Shape()
    print("Created the main box shape.")

    # 2. Create the second shape (the tool): a sphere.
    # We will place it at the center of the box so they overlap.
    sphere_center = gp_Pnt(50, 50, 50)
    sphere_radius = 30.0
    make_sphere = BRepPrimAPI_MakeSphere(sphere_center, sphere_radius)
    make_sphere.Build()
    if not make_sphere.IsDone():
        print("Sphere construction failed.")
        return
    the_sphere = make_sphere.Shape()
    print("Created the sphere shape to be used as a tool.")

    # 3. Perform the boolean operation: Cut.
    # This will subtract the_sphere from the_box.
    print("\nPerforming boolean CUT operation...")
    cut_operation = BRepAlgoAPI_Cut(the_box, the_sphere)
    cut_operation.Build()

    if not cut_operation.IsDone():
        print("Boolean cut operation failed.")
        return

    # 4. Get the resulting shape.
    result_shape = cut_operation.Shape()
    print("Successfully created the final shape (box with a spherical hole).")

    # In a real application, you would now use this `result_shape` for visualization,
    # further modeling, or analysis.

if __name__ == '__main__':
    create_box_with_hole()
