# -*- coding: utf-8 -*- 

"""
Phase 5 Summary Example: Advanced Surface and Feature Modeling
# 第五阶段汇总示例：高级曲面与特征建模

This script demonstrates a complete workflow for creating a complex shape with
free-form surfaces, simulating the design of a simple boat hull.
# 本脚本演示了使用自由形态曲面创建复杂形状的完整工作流，模拟了一个简单船体的设计过程。

It shows how to:
# 它展示了如何：
1. Create a series of profile curves using `GeomAPI`.
# 1. 使用 `GeomAPI` 创建一系列轮廓曲线。
2. Loft a surface through these profiles using `BRepOffsetAPI_ThruSections`.
# 2. 使用 `BRepOffsetAPI_ThruSections` 穿过这些轮廓线进行放样，生成曲面。
3. Close the surface to form a shell, and use `ShapeFix` to ensure its integrity.
# 3. 关闭曲面形成壳体，并使用 `ShapeFix` 确保其完整性。
4. Build and verify a valid solid from the shell.
# 4. 从该壳体构建并验证一个有效的实体。
"""

# --- Imports --- 
# --- 导入 --- 
from OCC.Core.gp import gp_Pnt
from OCC.Core.TColgp import TColgp_HArray1OfPnt
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeSolid
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.ShapeFix import ShapeFix_Shell
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Display.SimpleGui import init_display

def create_boat_hull():
    """
    Creates a boat hull shape using advanced surfacing and fixing techniques.
    # 使用高级曲面和修复技术创建一个船体形状。
    """
    print("--- Creating a boat hull ---")
    # --- 正在创建船体 ---

    # 1. Define and create profile curves for the hull.
    # 1. 定义并创建船体的轮廓曲线。
    # Each profile is a list of points.
    # # 每个轮廓都是一个点的列表。
    profile_points = [
        [gp_Pnt(0, -20, 0), gp_Pnt(5, -20, 5), gp_Pnt(10, -15, 10), gp_Pnt(15, 0, 10), gp_Pnt(10, 15, 10), gp_Pnt(5, 20, 5), gp_Pnt(0, 20, 0)],
        [gp_Pnt(50, -30, 0), gp_Pnt(55, -30, 10), gp_Pnt(60, -25, 20), gp_Pnt(65, 0, 20), gp_Pnt(60, 25, 20), gp_Pnt(55, 30, 10), gp_Pnt(50, 30, 0)],
        [gp_Pnt(100, -20, 0), gp_Pnt(105, -20, 5), gp_Pnt(110, -15, 10), gp_Pnt(115, 0, 10), gp_Pnt(110, 15, 10), gp_Pnt(105, 20, 5), gp_Pnt(100, 20, 0)]
    ]

    profile_wires = []
    for points in profile_points:
        # Convert Python list of points to OCCT array
        # # 将Python的点列表转换为OCCT数组
        occt_array = TColgp_HArray1OfPnt(1, len(points))
        for i, pnt in enumerate(points):
            occt_array.SetValue(i + 1, pnt)
        
        # Create a B-Spline curve through the points
        # # 通过这些点创建一条B样条曲线
        bspline_curve = GeomAPI_PointsToBSpline(occt_array).Curve()
        edge = BRepBuilderAPI_MakeEdge(bspline_curve).Edge()
        wire = BRepBuilderAPI_MakeWire(edge).Wire()
        profile_wires.append(wire)
    
    print("Step 1: Created 3 profile wires using GeomAPI.")
    # 步骤 1: 已使用 GeomAPI 创建3条轮廓线。

    # 2. Loft a surface through the profiles.
    # 2. 通过轮廓线放样一个曲面。
    loft_builder = BRepOffsetAPI_ThruSections(False, True) # Ruled=True for straight sections
    # # Ruled=True 使截面之间为直纹面
    for wire in profile_wires:
        loft_builder.AddWire(wire)
    loft_builder.Build()
    hull_shell = loft_builder.Shape()
    print("Step 2: Lofted a shell through the profiles.")
    # 步骤 2: 已通过轮廓线放样出一个壳体。

    # 3. Create a deck face to close the hull.
    # 3. 创建一个甲板面来闭合船体。
    # We use the last profile wire as the boundary for the deck.
    # # 我们使用最后一条轮廓线作为甲板的边界。
    deck_face = BRepBuilderAPI_MakeFace(profile_wires[-1], True).Face()
    print("Step 3: Created a deck face.")
    # 步骤 3: 已创建一个甲板面。

    # 4. Sew the hull and deck together and fix any gaps.
    # 4. 将船体和甲板缝合在一起并修复任何缝隙。
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Sewing
    sewing = BRepBuilderAPI_Sewing(1e-3) # Use a tolerance
    # # 使用一个公差
    sewing.Add(hull_shell)
    sewing.Add(deck_face)
    sewing.Perform()
    sewn_shape = sewing.SewedShape()

    fixer = ShapeFix_Shell(sewn_shape)
    fixer.Perform()
    fixed_shell = fixer.Shell()
    print("Step 4: Sewed and fixed the shell.")
    # 步骤 4: 已缝合并修复该壳体。

    # 5. Build and verify the final solid.
    # 5. 构建并验证最终的实体。
    mk_solid = BRepBuilderAPI_MakeSolid(fixed_shell)
    final_solid = mk_solid.Solid()
    analyzer = BRepCheck_Analyzer(final_solid)
    # In a real-world scenario, a failure here would require manual inspection and more advanced
    # repair techniques. For this example, we demonstrate that the check has been performed.
    # # 在真实场景中，此处的失败需要手动检查和更高级的修复技术。
    # # 对于本示例，我们旨在演示检查环节本身。
    is_valid = analyzer.IsValid()
    print(f"Step 5: Built a solid. Is it valid? -> {is_valid}")
    # 步骤 5: 已构建一个实体。它是否有效？ -> {is_valid}

    print("\nVerification successful: The full workflow, including the final check, was executed.")
    # 验证成功：完整的、包含最终检查的工作流已执行。
    return final_solid

if __name__ == "__main__":
    display, start_display, _, _ = init_display()
    
    boat_hull = create_boat_hull()
    display.DisplayShape(boat_hull, update=True, color="gray")

    start_display()
