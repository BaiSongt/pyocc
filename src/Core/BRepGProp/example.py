# -*- coding: utf-8 -*-

"""
This file demonstrates how to compute global properties (e.g., volume, center of
mass, surface area) of a solid shape using the `BRepGProp` package.
# 本文件演示了如何使用 `BRepGProp` 包来计算一个实体形状的全局属性（例如，体积、重心、表面积）。
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepGProp import brepgprop # The module containing the static functions
from OCC.Core.GProp import GProp_GProps

def calculate_properties():
    """
    Creates a composite shape and calculates its geometric properties.
    # 创建一个复合形状并计算其几何属性。
    """
    print("--- Calculating Geometric Properties of a Solid ---")
    # --- 正在计算一个实体的几何属性 ---

    # 1. Create a composite shape.
    # 1. 创建一个复合形状。
    box = BRepPrimAPI_MakeBox(100, 100, 100).Shape()
    sphere = BRepPrimAPI_MakeSphere(75).Shape()
    the_shape = BRepAlgoAPI_Fuse(box, sphere).Shape()
    print("Step 1: Created a composite shape (box fused with sphere).")
    # 步骤 1: 已创建一个复合形状（盒子与球体融合）。

    # 2. Create property containers.
    # 2. 创建属性容器。
    # We need one for surface properties and one for volume properties.
    # # 我们需要一个用于表面积属性，一个用于体积属性。
    surf_props = GProp_GProps()
    vol_props = GProp_GProps()
    print("Step 2: Initialized property containers.")
    # 步骤 2: 已初始化属性容器。

    # 3. Perform the calculations.
    # 3. 执行计算。
    # The brepgprop module contains the static methods to call.
    # # brepgprop 模块包含了要调用的静态方法。
    brepgprop.SurfaceProperties(the_shape, surf_props)
    brepgprop.VolumeProperties(the_shape, vol_props)
    print("Step 3: Calculated surface and volume properties.")
    # 步骤 3: 已计算表面积和体积属性。

    # 4. Retrieve and print the results.
    # 4. 提取并打印结果。
    surface_area = surf_props.Mass()
    volume = vol_props.Mass() # For volume props, Mass() returns the volume.
    # # 对于体积属性，Mass() 返回体积。
    center_of_mass = vol_props.CentreOfMass()

    print("\n--- Analysis Report ---")
    # --- 分析报告 ---
    print(f"Surface Area: {surface_area:.2f} mm^2")
    # 表面积: ... mm^2
    print(f"Volume:       {volume:.2f} mm^3")
    # 体积: ... mm^3
    print(f"Center of Mass: (X={center_of_mass.X():.2f}, Y={center_of_mass.Y():.2f}, Z={center_of_mass.Z():.2f}) mm")
    # 重心: (X=..., Y=..., Z=...) mm

    # 5. Verification
    # 5. 验证
    assert volume > 0
    assert surface_area > 0
    print("\nVerification successful: Properties are greater than zero.")
    # 验证成功：属性值大于零。

if __name__ == '__main__':
    calculate_properties()
