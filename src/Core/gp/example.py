# -*- coding: utf-8 -*-

"""
This file contains examples of how to use the `gp` (Geometric Primitives) package.
The `gp` package is the foundation for all geometric operations in OCCT.
"""

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf

def create_point_and_vector():
    """
    Demonstrates the creation of a 3D point and a 3D vector.
    """
    # Create a 3D point at coordinates (1.0, 2.0, 3.0)
    my_point = gp_Pnt(1.0, 2.0, 3.0)
    print(f"Created a gp_Pnt at: ({my_point.X()}, {my_point.Y()}, {my_point.Z()})")

    # Create a 3D vector with components (5.0, 5.0, 0.0)
    my_vector = gp_Vec(5.0, 5.0, 0.0)
    print(f"Created a gp_Vec with components: ({my_vector.X()}, {my_vector.Y()}, {my_vector.Z()})")
    
    return my_point, my_vector

def translate_point():
    """
    Demonstrates how to apply a translation transformation to a point.
    """
    print("\n--- Translation Example ---")
    # Create an initial point and a translation vector
    start_point = gp_Pnt(10.0, 10.0, 10.0)
    translation_vector = gp_Vec(5.0, -5.0, 5.0)

    print(f"Original point: ({start_point.X()}, {start_point.Y()}, {start_point.Z()})")
    print(f"Translation vector: ({translation_vector.X()}, {translation_vector.Y()}, {translation_vector.Z()})")

    # Create a translation transformation
    # A gp_Trsf can represent complex transformations, but here we initialize it
    # for a simple translation.
    a_transform = gp_Trsf()
    a_transform.SetTranslation(translation_vector)

    # Apply the transformation to the point.
    # The .Transformed() method returns a new, transformed point.
    # The original point `start_point` is not modified.
    end_point = start_point.Transformed(a_transform)

    print(f"Transformed point: ({end_point.X()}, {end_point.Y()}, {end_point.Z()})")
    
    # You can also translate a point directly with a vector
    # The .Translate() method modifies the point in-place.
    # Let's create a copy to modify
    point_to_modify = gp_Pnt(start_point.XYZ())
    point_to_modify.Translate(translation_vector)
    print(f"Transformed point (in-place): ({point_to_modify.X()}, {point_to_modify.Y()}, {point_to_modify.Z()})")


if __name__ == '__main__':
    create_point_and_vector()
    translate_point()
