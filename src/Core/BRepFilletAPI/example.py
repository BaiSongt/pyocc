# -*- coding: utf-8 -*-

"""
This file demonstrates the use of the `BRepFilletAPI` package to create fillets.
# 本文件演示 `BRepFilletAPI` 包的使用方法来创建圆角。

It shows how to create a solid, select some of its edges, and apply a constant
radius fillet to them.
# 它展示了如何创建一个实体，选择其部分边缘，并为它们应用一个恒定半径的圆角。
"""

# Import necessary classes
# 导入必要的类
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopTools import TopTools_MapOfShape # Import the map for uniqueness
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Line

def fillet_box_edges():
    """
    Creates a box and applies fillets to its top edges.
    # 创建一个盒子并为其顶部边缘应用圆角。
    """
    print("--- Applying fillets to selected edges of a box ---")
    # --- 为盒子的选定边缘应用圆角 ---

    # 1. Create the base shape: a box.
    # 1. 创建基础形状：一个盒子。
    box_size = (100.0, 80.0, 60.0)
    # The BRepPrimAPI_MakeBox constructor with 3 arguments creates a box
    # from (0,0,0) to (dx, dy, dz).
    # # BRepPrimAPI_MakeBox 使用3个参数的构造函数会创建一个从(0,0,0)到(dx,dy,dz)的盒子。
    the_box = BRepPrimAPI_MakeBox(box_size[0], box_size[1], box_size[2]).Shape()
    print(f"Created a box with size {box_size}.")
    # 已创建一个尺寸为 {box_size} 的盒子。

    # 2. Instantiate the MakeFillet tool with the box shape.
    # 2. 使用盒子形状实例化 MakeFillet 工具。
    mk_fillet = BRepFilletAPI_MakeFillet(the_box)

    # 3. Select the edges to be filleted, ensuring uniqueness.
    # 3. 选择要进行圆角处理的边，并确保唯一性。
    fillet_radius = 10.0
    edge_explorer = TopExp_Explorer(the_box, TopAbs_EDGE)
    edge_map = TopTools_MapOfShape() # Create a map to store unique edges

    print(f"Selecting top edges and adding a fillet of radius {fillet_radius}...")
    # 正在选择顶部边缘并添加半径为 {fillet_radius} 的圆角...

    while edge_explorer.More():
        an_edge = edge_explorer.Current()
        # Use the map to process each unique edge only once.
        # # 使用 map 来确保每个唯一的边只被处理一次。
        if edge_map.Add(an_edge):
            # To identify the top edges, we check if the edge is a line and lies on the Z=60 plane.
            # # 为了识别顶部边缘，我们检查该边是否为直线且位于 Z=60 的平面上。
            adaptor = BRepAdaptor_Curve(an_edge)
            if adaptor.GetType() == GeomAbs_Line:
                p1 = adaptor.Value(adaptor.FirstParameter())
                p2 = adaptor.Value(adaptor.LastParameter())
                if p1.Z() == box_size[2] and p2.Z() == box_size[2]:
                    print(f"  - Found top edge with points: ({p1.X():.1f}, {p1.Y():.1f}, {p1.Z():.1f}) -> ({p2.X():.1f}, {p2.Y():.1f}, {p2.Z():.1f})")
                    #   - 找到顶点坐标为 ... 的顶边
                    mk_fillet.Add(fillet_radius, an_edge)
        
        edge_explorer.Next()

    # 4. Build the filleted shape.
    # 4. 构建圆角形状。
    mk_fillet.Build()
    if not mk_fillet.IsDone():
        print("Fillet operation failed.")
        # 圆角操作失败。
        return

    filleted_box = mk_fillet.Shape()
    print("Successfully created the filleted box.")
    # 已成功创建带圆角的盒子。

    # 5. Verification
    # 5. 验证
    assert not filleted_box.IsNull()
    print("Verification successful: The result is a valid shape.")
    # 验证成功：结果是一个有效的形状。

if __name__ == '__main__':
    fillet_box_edges()