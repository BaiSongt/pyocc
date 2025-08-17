# -*- coding: utf-8 -*- 

"""
This file demonstrates how to use the `BRepPrimAPI` to create primitive 3D shapes.
We will create a simple box and then inspect its topology to count its faces,
edges, and vertices, connecting the concepts from `gp`, `TopoDS`, and `BRepPrimAPI`.
"""

# Import necessary classes
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopTools import TopTools_MapOfShape  # Import the map tool for uniqueness

def create_and_explore_box():
    """
    Creates a box using BRepPrimAPI_MakeBox and explores its sub-shapes.
    """
    print("--- Box Creation and Exploration Example ---")

    # 1. Define the geometry for the box.
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(10, 20, 30)
    print(f"Defined box corners at (0,0,0) and (10,20,30).")

    # 2. Build the topological shape.
    make_box = BRepPrimAPI_MakeBox(p1, p2)
    make_box.Build()  # Explicitly build the shape
    if not make_box.IsDone():
        print("Box construction failed.")
        return

    my_box_shape = make_box.Shape()
    print("Successfully created a box shape.")

    # 3. Explore the box to count its unique faces, edges, and vertices.
    def count_unique_subshapes(shape, shape_type):
        """Helper function to count unique sub-shapes of a given type."""
        a_map = TopTools_MapOfShape()
        explorer = TopExp_Explorer(shape, shape_type)
        while explorer.More():
            # Add the current shape to the map. The map handles duplicates.
            a_map.Add(explorer.Current())
            explorer.Next()
        return a_map.Size()  # Use .Size() to get the number of items in the map

    num_faces = count_unique_subshapes(my_box_shape, TopAbs_FACE)
    num_edges = count_unique_subshapes(my_box_shape, TopAbs_EDGE)
    num_vertices = count_unique_subshapes(my_box_shape, TopAbs_VERTEX)

    print("\nExploring the topology of the box...")
    print(f"  - Number of Faces: {num_faces}")
    print(f"  - Number of Edges: {num_edges}")
    print(f"  - Number of Vertices: {num_vertices}")

    # A standard box should have 6 faces, 12 edges, and 8 vertices.
    assert num_faces == 6
    assert num_edges == 12
    assert num_vertices == 8
    print("\nTopological counts are correct for a standard box.")

if __name__ == '__main__':
    create_and_explore_box()