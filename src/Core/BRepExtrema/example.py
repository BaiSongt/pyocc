# -*- coding: utf-8 -*- 

"""
This file demonstrates how to compute the minimum distance between two shapes
using the `BRepExtrema` package.
# 本文件演示了如何使用 `BRepExtrema` 包来计算两个形状之间的最短距离。
"""

import math

# --- Imports ---
# --- 导入 ---
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape

def calculate_distance_between_shapes():
    """
    Creates two spheres and calculates the minimum distance between them.
    # 创建两个球体并计算它们之间的最短距离。
    """
    print("--- Calculating Minimum Distance Between Two Shapes ---")
    # --- 正在计算两个形状之间的最短距离 ---

    # 1. Create the first shape: a sphere at the origin.
    # 1. 创建第一个形状：一个位于原点的球体。
    radius1 = 25.0
    sphere1 = BRepPrimAPI_MakeSphere(radius1).Shape()
    print(f"Created Sphere 1 at (0,0,0) with radius {radius1}.")
    # 已在 (0,0,0) 创建半径为 {radius1} 的球体1。

    # 2. Create the second shape: another sphere, translated away from the origin.
    # 2. 创建第二个形状：另一个球体，并将其平移离开原点。
    radius2 = 50.0
    center_pnt2 = gp_Pnt(200, 0, 0)
    sphere2 = BRepPrimAPI_MakeSphere(center_pnt2, radius2).Shape()
    print(f"Created Sphere 2 at (200,0,0) with radius {radius2}.")
    # 已在 (200,0,0) 创建半径为 {radius2} 的球体2。

    # 3. Perform the distance calculation.
    # 3. 执行距离计算。
    # The calculation is performed in the constructor of DistShapeShape.
    # # 计算在 DistShapeShape 的构造函数中执行。
    dist_calculator = BRepExtrema_DistShapeShape(sphere1, sphere2)
    dist_calculator.Perform()

    if not dist_calculator.IsDone():
        print("Distance calculation failed.")
        # 距离计算失败。
        return

    # 4. Retrieve and print the results.
    # 4. 提取并打印结果。
    min_distance = dist_calculator.Value()
    num_solutions = dist_calculator.NbSolution()
    point_on_s1 = dist_calculator.PointOnShape1(1) # Get the 1st solution point
    # # 获取第一个解的点
    point_on_s2 = dist_calculator.PointOnShape2(1)

    print("\n--- Measurement Report ---")
    # --- 测量报告 ---
    print(f"Minimum distance: {min_distance:.2f} mm")
    # 最短距离: ... mm
    print(f"Number of solutions: {num_solutions}")
    # 解的数量: ...
    print(f"Point on Sphere 1: (X={point_on_s1.X():.2f}, Y={point_on_s1.Y():.2f}, Z={point_on_s1.Z():.2f}) mm")
    # 球体1上的点: ...
    print(f"Point on Sphere 2: (X={point_on_s2.X():.2f}, Y={point_on_s2.Y():.2f}, Z={point_on_s2.Z():.2f}) mm")
    # 球体2上的点: ...

    # 5. Verification
    # 5. 验证
    # For two spheres, the distance is the distance between centers minus radii.
    # # 对于两个球体，表面距离 = 中心距 - 半径和。
    expected_distance = center_pnt2.Distance(gp_Pnt(0,0,0)) - radius1 - radius2
    # Use a small tolerance for floating point comparison.
    # # 对于浮点数比较，使用一个小的容差。
    assert math.isclose(min_distance, expected_distance, rel_tol=1e-5)
    print("\nVerification successful: Calculated distance matches the theoretical value.")
    # 验证成功：计算出的距离与理论值相符。

if __name__ == '__main__':
    calculate_distance_between_shapes()
