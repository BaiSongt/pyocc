# -*- coding: utf-8 -*-

"""
This file demonstrates the use of the `BRepBuilderAPI` package.
# 本文件演示 `BRepBuilderAPI` 包的使用方法。

It shows the "bottom-up" approach to modeling: creating points, then edges,
collecting edges into a wire, and finally building a face from the wire.
# 它展示了“自下而上”的建模方法：创建点，然后是边，将边收集成线框，最后从线框构建一个面。
"""

# Import necessary classes
# 导入必要的类
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.TopoDS import TopoDS_Face

def build_face_from_points():
    """
    Builds a rectangular face from four points.
    # 从四个点构建一个矩形面。
    """
    print("--- Building a Face from scratch using BRepBuilderAPI ---")
    # --- 使用 BRepBuilderAPI 从零开始构建一个面 ---

    # 1. Define the geometry: four points for the rectangle corners.
    # 1. 定义几何形状：矩形的四个角点。
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(100, 0, 0)
    p3 = gp_Pnt(100, 50, 0)
    p4 = gp_Pnt(0, 50, 0)
    print("Defined 4 corner points.")
    # 已定义4个角点。

    # 2. Create the topological edges from the points.
    # 2. 从点创建拓扑边。
    edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()
    print("Created 4 edges from the points.")
    # 已从点创建4条边。

    # 3. Create a wire by connecting the edges.
    # 3. 通过连接边来创建一个线框。
    make_wire = BRepBuilderAPI_MakeWire()
    make_wire.Add(edge1)
    make_wire.Add(edge2)
    make_wire.Add(edge3)
    make_wire.Add(edge4)
    
    make_wire.Build()
    if not make_wire.IsDone():
        print("Wire construction failed.")
        # 线框构建失败。
        return
    
    my_wire = make_wire.Wire()
    print("Created a closed wire from the 4 edges.")
    # 已从4条边创建了一个闭合线框。

    # 4. Create a face from the closed wire.
    # 4. 从闭合线框创建一个面。
    # The `True` argument indicates that we want to build a planar face.
    # # 参数 `True` 表示我们希望构建一个平面。
    make_face = BRepBuilderAPI_MakeFace(my_wire, True)
    make_face.Build()

    if not make_face.IsDone():
        print("Face construction failed.")
        # 面构建失败。
        return

    my_face = make_face.Face()
    print("Successfully created a face from the wire.")
    # 已成功从线框创建了一个面。

    # 5. Verification
    # 5. 验证
    # Check if the result is a valid TopoDS_Face.
    # # 检查结果是否为一个有效的 TopoDS_Face。
    assert not my_face.IsNull()
    assert isinstance(my_face, TopoDS_Face)
    print("Verification successful: The result is a valid face.")
    # 验证成功：结果是一个有效的面。

if __name__ == '__main__':
    build_face_from_points()
