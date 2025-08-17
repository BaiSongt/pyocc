# -*- coding: utf-8 -*-

"""
This file demonstrates the use of the `GeomAPI` package to create a B-Spline
surface from a grid of points.
# 本文件演示了如何使用 `GeomAPI` 包从一个点阵创建B样条曲面。

It shows how to:
# 它展示了如何：
1. Create a 2D array of points in Python.
# 1. 在Python中创建一个二维点数组。
2. Transfer these points to an OCCT-specific array (`TColgp_HArray2OfPnt`).
# 2. 将这些点传输到OCCT专用的数组（`TColgp_HArray2OfPnt`）中。
3. Use `GeomAPI_PointsToBSplineSurface` to build the geometry.
# 3. 使用 `GeomAPI_PointsToBSplineSurface` 来构建几何体。
4. Convert the resulting `Geom_Surface` into a displayable `TopoDS_Face`.
# 4. 将生成的 `Geom_Surface` 转换为一个可显示的 `TopoDS_Face`。
"""

import math

# --- Imports ---
# --- 导入 ---
from OCC.Core.gp import gp_Pnt
from OCC.Core.TColgp import TColgp_HArray2OfPnt
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Display.SimpleGui import init_display

def create_bspline_surface():
    """
    Creates a B-Spline surface from a grid of points.
    # 从一个点阵创建B样条曲面。
    """
    print("--- Creating a B-Spline surface from points ---")
    # --- 正在从点创建B样条曲面 ---

    # 1. Define the grid dimensions and create points in a Python list of lists.
    # 1. 定义网格尺寸并在Python的列表的列表中创建点。
    num_points_u = 15
    num_points_v = 10
    python_points = []
    for i in range(num_points_u):
        row = []
        for j in range(num_points_v):
            # Create a wavy surface using sine functions
            # # 使用正弦函数创建一个波浪形的曲面
            x = i * 10
            y = j * 10
            z = 15 * math.sin(i / 5.0) * math.cos(j / 5.0)
            row.append(gp_Pnt(x, y, z))
        python_points.append(row)
    print(f"Step 1: Created a {num_points_u}x{num_points_v} grid of Python points.")
    # 步骤 1: 已创建一个 {num_points_u}x{num_points_v} 的Python点阵。

    # 2. Transfer the points to an OCCT HArray2.
    # 2. 将点传输到一个OCCT的HArray2中。
    # The array bounds are 1-based in OCCT.
    # # 在OCCT中，数组的边界是从1开始的。
    occt_points = TColgp_HArray2OfPnt(1, num_points_u, 1, num_points_v)
    for i in range(num_points_u):
        for j in range(num_points_v):
            occt_points.SetValue(i + 1, j + 1, python_points[i][j])
    print("Step 2: Transferred points to an OCCT HArray2.")
    # 步骤 2: 已将点传输到OCCT的HArray2中。

    # 3. Build the B-Spline surface from the points.
    # 3. 从点构建B样条曲面。
    # The calculation is done in the constructor.
    # # 计算在构造函数中完成。
    surface_builder = GeomAPI_PointsToBSplineSurface(occt_points)
    bspline_surface = surface_builder.Surface()
    print("Step 3: Built the Geom_BSplineSurface.")
    # 步骤 3: 已构建 Geom_BSplineSurface。

    # 4. Convert the geometric surface into a displayable topological face.
    # 4. 将几何曲面转换为可显示的拓扑面。
    make_face = BRepBuilderAPI_MakeFace(bspline_surface, 1e-3) # Use a tolerance
    # # 使用一个公差
    the_face = make_face.Face()
    print("Step 4: Converted the geometry to a TopoDS_Face.")
    # 步骤 4: 已将几何体转换为 TopoDS_Face。

    # 5. Verification
    # 5. 验证
    assert not the_face.IsNull()
    print("\nVerification successful: The resulting face is valid.")
    # 验证成功：生成的面是有效的。
    
    return the_face

if __name__ == '__main__':
    display, start_display, _, _ = init_display()
    
    # Create and display the surface
    # # 创建并显示曲面
    bspline_face = create_bspline_surface()
    display.DisplayShape(bspline_face, update=True, color="blue")

    start_display()
