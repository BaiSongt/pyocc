# -*- coding: utf-8 -*- 

"""
This file demonstrates how to generate a polygonal mesh from a B-Rep shape
using the `BRepMesh` package.
# 本文件演示了如何使用 `BRepMesh` 包从B-Rep形状生成多边形网格。

It shows how to take a precise geometric shape (a sphere), run the meshing
algorithm, and then access the resulting triangulation data.
# 它展示了如何获取一个精确的几何形状（球体），运行网格化算法，然后访问最终的三角化数据。
"""

# --- Imports --- 
# --- 导入 --- 
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopLoc import TopLoc_Location

def mesh_a_shape():
    """
    Creates a sphere, meshes it, and reports the mesh statistics.
    # 创建一个球体，对其进行网格化，并报告网格统计信息。
    """
    print("--- Meshing a B-Rep Shape ---")
    # --- 对一个B-Rep形状进行网格化 ---

    # 1. Create the B-Rep shape: a sphere.
    # 1. 创建B-Rep形状：一个球体。
    radius = 50.0
    sphere = BRepPrimAPI_MakeSphere(radius).Shape()
    print(f"Created a sphere with radius {radius}.")
    # 已创建一个半径为 {radius} 的球体。

    # 2. Perform the meshing operation.
    # 2. 执行网格化操作。
    # The `BRepMesh_IncrementalMesh` constructor performs the meshing.
    # The mesh data is then stored within the B-Rep shape itself.
    # # `BRepMesh_IncrementalMesh` 的构造函数会执行网格化。
    # # 网格数据随后被存储在B-Rep形状内部。
    linear_deflection = 0.5 # The max distance between mesh and precise shape
    # # 线性挠度：网格与精确形状之间的最大距离
    print(f"Running the mesher with a linear deflection of {linear_deflection}...")
    # 正在以 {linear_deflection} 的线性挠度运行网格化程序...
    BRepMesh_IncrementalMesh(sphere, linear_deflection)
    print("Meshing complete.")
    # 网格化完成。

    # 3. Access the triangulation data from the shape.
    # 3. 从形状中访问三角化数据。
    # We need to iterate through all faces of the shape and get the triangulation
    # for each face. Then, we sum up the statistics.
    # # 我们需要遍历形状的所有面，获取每个面的三角化数据，然后将统计数据相加。
    total_nodes = 0
    total_triangles = 0
    face_explorer = TopExp_Explorer(sphere, TopAbs_FACE)

    print("\n--- Accessing Triangulation Data ---")
    # --- 正在访问三角化数据 ---
    face_count = 0
    while face_explorer.More():
        face_count += 1
        a_face = face_explorer.Current()
        # Get the triangulation for the face
        # # 获取该面的三角化数据
        a_location = TopLoc_Location()
        # The BRep_Tool.Triangulation method returns the Poly_Triangulation object
        # # BRep_Tool.Triangulation 方法返回 Poly_Triangulation 对象
        triangulation = BRep_Tool.Triangulation(a_face, a_location)

        if triangulation is not None:
            num_nodes = triangulation.NbNodes()
            num_triangles = triangulation.NbTriangles()
            total_nodes += num_nodes
            total_triangles += num_triangles
            print(f"  - Face #{face_count}: Found {num_nodes} nodes and {num_triangles} triangles.")
            #   -面 #{face_count}: 找到 {num_nodes} 个节点和 {num_triangles} 个三角形。
        else:
            print(f"  - Face #{face_count}: No triangulation found.")
            #   -面 #{face_count}: 未找到三角化数据。

        face_explorer.Next()
    
    print("\n--- Meshing Statistics ---")
    # --- 网格化统计 ---
    print(f"Total number of nodes: {total_nodes}")
    # 节点总数：{total_nodes}
    print(f"Total number of triangles: {total_triangles}")
    # 三角形总数：{total_triangles}

    # 4. Verification
    # 4. 验证
    assert total_triangles > 0
    print("\nVerification successful: The shape was meshed.")
    # 验证成功：形状已被网格化。

if __name__ == '__main__':
    mesh_a_shape()
