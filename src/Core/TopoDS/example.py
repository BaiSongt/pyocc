# -*- coding: utf-8 -*- 

"""
This file demonstrates how to work with the `TopoDS` (Topological Data Structure).
TopoDS defines the relationship between parts of a shape (Vertex, Edge, Face, etc.),
but doesn't describe their actual geometry.

We will create a simple shape (an Edge) and then use TopExp_Explorer to inspect
its underlying topological structure (its Vertices).
"""

# Import necessary classes
# gp: For geometric primitives (points)
# BRepBuilderAPI: To build the topological shapes (the edge)
# TopoDS: To handle and convert topological shapes
# TopExp: To explore the shape's structure
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods
from OCC.Core.TopAbs import TopAbs_VERTEX

def explore_edge():
    """
    Creates an edge and explores its sub-shapes (vertices).
    """
    print("--- Edge Exploration Example ---")

    # 1. Create the geometry for the edge: two 3D points from the `gp` package.
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(5, 5, 5)
    print(f"Created two gp_Pnt for the edge: (0,0,0) and (5,5,5)")

    # 2. Build the topological shape: a `TopoDS_Edge`.
    # We use a tool from `BRepBuilderAPI` to do this.
    # The result of .Edge() is a `TopoDS_Edge`.
    make_edge = BRepBuilderAPI_MakeEdge(p1, p2)
    if not make_edge.IsDone():
        print("Edge construction failed.")
        return
    
    my_edge = make_edge.Edge()
    print("Successfully created a TopoDS_Edge.")

    # 3. Explore the edge to find its vertices.
    # We use a TopExp_Explorer to iterate through sub-shapes.
    # `TopAbs_VERTEX` tells the explorer we are only interested in vertices.
    explorer = TopExp_Explorer(my_edge, TopAbs_VERTEX)

    print("\nExploring the edge for vertices...")
    vertex_count = 0
    while explorer.More():
        vertex_count += 1
        # Get the current sub-shape, which is a generic `TopoDS_Shape`
        current_shape = explorer.Current()

        # To work with the vertex, we must cast it from TopoDS_Shape to TopoDS_Vertex.
        # The `topods.Vertex()` function performs this safe cast.
        a_vertex = topods.Vertex(current_shape)

        print(f"  Found Vertex #{vertex_count}")
        
        # The explorer does not directly give the geometry of the vertex.
        # We would need another tool (BRep_Tool) to get the underlying gp_Pnt,
        # which we will cover in later examples.

        # Move to the next vertex in the explorer
        explorer.Next()

    if vertex_count == 0:
        print("No vertices found on the edge.")

if __name__ == '__main__':
    explore_edge()
