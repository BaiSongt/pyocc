# -*- coding: utf-8 -*-

"""
This file demonstrates the use of the `BRepOffsetAPI` package, specifically
for creating a hollow shape with a constant thickness (shelling).
# 本文件演示 `BRepOffsetAPI` 包的使用方法，特别是用于创建一个具有恒定壁厚的中空形状（抽壳）。

It shows how to create a solid box and then use `BRepOffsetAPI_MakeThickSolid`
to turn it into an open container.
# 它展示了如何创建一个实心盒子，然后使用 `BRepOffsetAPI_MakeThickSolid` 将其变成一个开口的容器。
"""

# Import necessary classes
# 导入必要的类
from OCC.Core.gp import gp_Pnt, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeThickSolid
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane

def create_hollow_box():
    """
    Creates a box and makes it hollow by removing the top face.
    # 创建一个盒子，并通过移除顶面使其成为中空。
    """
    print("--- Creating a hollow box (shelling operation) ---")
    # --- 创建一个中空盒子（抽壳操作） ---

    # 1. Create the base shape: a solid box.
    # 1. 创建基础形状：一个实心盒子。
    box_size = (100.0, 80.0, 60.0)
    the_box = BRepPrimAPI_MakeBox(box_size[0], box_size[1], box_size[2]).Shape()
    print(f"Created a solid box with size {box_size}.")
    # 已创建一个尺寸为 {box_size} 的实心盒子。

    # 2. Find the face to be removed (the top face).
    # 2. 找到要移除的面（顶面）。
    top_face = None
    highest_z = -1.0e30 # A very small number to start with
    face_explorer = TopExp_Explorer(the_box, TopAbs_FACE)

    while face_explorer.More():
        a_face = face_explorer.Current()
        # Check if the face is a plane and find its location.
        # # 检查该面是否为平面并找出其位置。
        surf_adaptor = BRepAdaptor_Surface(a_face, True)
        if surf_adaptor.GetType() == GeomAbs_Plane:
            plane = surf_adaptor.Plane()
            # The Z coordinate of the plane's origin gives its height.
            # # 平面原点的Z坐标即为其高度。
            if plane.Location().Z() > highest_z:
                highest_z = plane.Location().Z()
                top_face = a_face
        face_explorer.Next()

    if top_face is None:
        print("Could not find the top face to remove.")
        # 未能找到要移除的顶面。
        return
    
    print(f"Found the top face at Z = {highest_z} to be removed.")
    # 已找到位于 Z = {highest_z} 的顶面作为移除对象。

    # 3. Create a list of faces to remove.
    # 3. 创建一个要移除的面的列表。
    faces_to_remove = TopTools_ListOfShape()
    faces_to_remove.Append(top_face)

    # The BRepOffsetAPI_MakeThickSolid class uses a two-step pattern:
    # 1. Create an empty instance of the algorithm.
    # 2. Call a method (e.g., MakeThickSolidByJoin) to perform the operation.
    # # BRepOffsetAPI_MakeThickSolid 类使用两步模式：
    # # 1. 创建一个空的算法实例。
    # # 2. 调用一个方法（如 MakeThickSolidByJoin）来执行操作。
    mk_thick = BRepOffsetAPI_MakeThickSolid()
    offset_thickness = -5.0
    tolerance = 1.0e-3
    mk_thick.MakeThickSolidByJoin(the_box, faces_to_remove, offset_thickness, tolerance)
    mk_thick.Build()

    if not mk_thick.IsDone():
        print("Shelling operation failed.")
        # 抽壳操作失败。
        return

    hollow_box = mk_thick.Shape()
    print(f"Successfully created a hollow box with wall thickness {-offset_thickness}.")
    # 已成功创建一个壁厚为 {-offset_thickness} 的中空盒子。

    # 5. Verification
    # 5. 验证
    assert not hollow_box.IsNull()
    print("Verification successful: The result is a valid shape.")
    # 验证成功：结果是一个有效的形状。

if __name__ == '__main__':
    create_hollow_box()
