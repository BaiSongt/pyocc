# -*- coding: utf-8 -*-

"""
Phase 2 Summary Example: Advanced B-Rep Modeling
# 第二阶段汇总示例：进阶边界表示建模

This script demonstrates a complete workflow using advanced modeling tools:
# 本脚本演示了使用高级建模工具的完整工作流程：

1.  `BRepBuilderAPI` & `BRepPrimAPI`: To create the base L-shaped bracket.
    # 用于创建基础的L型支架。
2.  `BRepAlgoAPI`: To cut mounting holes.
    # 用于切割出安装孔。
3.  `BRepFilletAPI`: To add strengthening fillets to the joints.
    # 用于在连接处添加加强圆角。
4.  `AIS`: To visualize the final complex part.
    # 用于将最终的复杂零件进行可视化。
"""

# --- Imports ---
# --- 导入 --- 
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Circ, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_SOLID
from OCC.Display.SimpleGui import init_display

def create_bracket():
    """
    Creates a complex L-shaped bracket with holes and fillets.
    # 创建一个带有孔和圆角的复杂L型支架。
    """
    print("--- Creating a complex mechanical bracket ---")
    # --- 正在创建一个复杂的机械支架 ---

    # 1. Create the base plate (using BRepBuilderAPI and BRepPrimAPI)
    # 1. 创建基板（使用 BRepBuilderAPI 和 BRepPrimAPI）
    base_plate_profile = BRepBuilderAPI_MakeWire(
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(100, 0, 0)).Edge(),
        BRepBuilderAPI_MakeEdge(gp_Pnt(100, 0, 0), gp_Pnt(100, 80, 0)).Edge(),
        BRepBuilderAPI_MakeEdge(gp_Pnt(100, 80, 0), gp_Pnt(0, 80, 0)).Edge(),
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 80, 0), gp_Pnt(0, 0, 0)).Edge()
    ).Wire()
    base_plate_face = BRepBuilderAPI_MakeFace(base_plate_profile, True).Face()
    base_plate_solid = BRepPrimAPI_MakePrism(base_plate_face, gp_Vec(0, 0, 15)).Shape()
    print("Step 1.1: Created base plate solid.")
    # 步骤 1.1: 已创建基板实体。

    # 2. Create the vertical plate and fuse it with the base
    # 2. 创建垂直板并与基板融合
    vert_plate_profile = BRepBuilderAPI_MakeWire(
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 15), gp_Pnt(0, 0, 100)).Edge(),
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 100), gp_Pnt(0, 80, 100)).Edge(),
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 80, 100), gp_Pnt(0, 80, 15)).Edge(),
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 80, 15), gp_Pnt(0, 0, 15)).Edge()
    ).Wire()
    vert_plate_face = BRepBuilderAPI_MakeFace(vert_plate_profile, True).Face()
    vert_plate_solid = BRepPrimAPI_MakePrism(vert_plate_face, gp_Vec(15, 0, 0)).Shape()
    l_bracket = BRepAlgoAPI_Fuse(base_plate_solid, vert_plate_solid).Shape()
    print("Step 1.2: Created vertical plate and fused to form L-bracket.")
    # 步骤 1.2: 已创建垂直板并融合成L型支架。

    # 3. Add a large hole to the vertical plate (using BRepAlgoAPI_Cut)
    # 3. 在垂直板上添加一个大孔（使用 BRepAlgoAPI_Cut）
    hole_cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(15, 40, 60), gp_Dir(1, 0, 0)), 25, 15).Shape()
    l_bracket = BRepAlgoAPI_Cut(l_bracket, hole_cylinder).Shape()
    print("Step 2: Cut a large hole in the vertical plate.")
    # 步骤 2: 已在垂直板上切割出一个大孔。

    # 4. Add fillets to the internal joint (using BRepFilletAPI)
    # 4. 为内部连接处添加圆角（使用 BRepFilletAPI）
    mk_fillet = BRepFilletAPI_MakeFillet(l_bracket)
    edge_explorer = TopExp_Explorer(l_bracket, TopAbs_EDGE)
    while edge_explorer.More():
        an_edge = edge_explorer.Current()
        # Find the edge at the intersection of the two plates
        # # 找到两个板相交处的边
        from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
        adaptor = BRepAdaptor_Curve(an_edge)
        p1 = adaptor.Value(adaptor.FirstParameter())
        p2 = adaptor.Value(adaptor.LastParameter())
        if p1.X() == 15 and p2.X() == 15 and p1.Z() == 15 and p2.Z() == 15:
            mk_fillet.Add(10.0, an_edge) # Add a 10mm radius fillet
            print("Step 3: Found internal edge and added to fillet operation.")
            # 步骤 3: 已找到内部边缘并添加到圆角操作。
            break # Assume only one such edge
        edge_explorer.Next()
    
    mk_fillet.Build()
    if mk_fillet.IsDone():
        l_bracket = mk_fillet.Shape()
        print("Step 3.1: Successfully applied fillet.")
        # 步骤 3.1: 已成功应用圆角。
    else:
        print("Step 3.1: Fillet operation failed.")
        # 步骤 3.1: 圆角操作失败。

    print("--- Bracket creation complete ---")
    # --- 支架创建完成 ---
    return l_bracket

if __name__ == "__main__":
    # Initialize the viewer
    # # 初始化查看器
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Create and display the bracket
    # # 创建并显示支架
    final_bracket = create_bracket()
    display.DisplayShape(final_bracket, update=True, color="silver")

    # Start the viewer event loop
    # # 启动查看器事件循环
    start_display()
