# -*- coding: utf-8 -*-

"""
This file demonstrates the use of the `ShapeFix` package to repair a defective shape.
# 本文件演示了如何使用 `ShapeFix` 包来修复一个有缺陷的形状。

It shows how to:
# 它展示了如何：
1. Intentionally create a defective shape (an open shell with a missing face).
# 1. 故意创建一个有缺陷的形状（一个缺少一个面的开放壳体）。
2. Show that standard tools fail to process it.
# 2. 展示标准工具无法处理它。
3. Use `ShapeFix_Solid` to automatically repair the defect and create a valid solid.
# 3. 使用 `ShapeFix_Solid` 自动修复该缺陷并创建一个有效的实体。
4. Verify the result with `BRepCheck_Analyzer`.
# 4. 使用 `BRepCheck_Analyzer` 来验证结果。
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid, BRepBuilderAPI_Sewing
from OCC.Core.ShapeFix import ShapeFix_Solid
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCC.Core.TopoDS import TopoDS_Shell, TopoDS_Compound, TopoDS_Builder
from OCC.Core.BRepCheck import BRepCheck_Analyzer

def repair_defective_shape():
    """
    Creates a defective shell and repairs it into a solid.
    # 创建一个有缺陷的壳体并将其修复成一个实体。
    """
    print("--- Repairing a Defective Shape with ShapeFix ---")
    # --- 正在使用 ShapeFix 修复一个有缺陷的形状 ---

    # 1. Create a standard box.
    # 1. 创建一个标准的盒子。
    the_box = BRepPrimAPI_MakeBox(100, 100, 100).Shape()

    # 2. Intentionally create a defective shape by removing one face.
    # 2. 通过移除一个面来故意创建一个有缺陷的形状。
    face_explorer = TopExp_Explorer(the_box, TopAbs_FACE)
    builder = TopoDS_Builder()
    defective_shell = TopoDS_Shell()
    builder.MakeShell(defective_shell)

    face_count = 0
    while face_explorer.More():
        a_face = face_explorer.Current()
        if face_count < 5: # Add only the first 5 faces
            # # 只添加前5个面
            builder.Add(defective_shell, a_face)
        face_count += 1
        face_explorer.Next()
    
    print("Step 1: Created a defective shell with 5 faces (one missing).")
    # 步骤 1: 已创建一个有5个面（缺少一个）的有缺陷的壳体。

    # 3. Attempt to create a solid with the standard tool (this should fail).
    # 3. 尝试使用标准工具创建实体（这应该会失败）。
    mk_solid = BRepBuilderAPI_MakeSolid(defective_shell)
    a_solid = mk_solid.Solid()
    # The resulting shape is not null, but it should be an invalid solid.
    # # 生成的形状不为空，但它应该是一个无效的实体。
    analyzer1 = BRepCheck_Analyzer(a_solid)
    assert not analyzer1.IsValid(), "Standard MakeSolid should produce an invalid solid from an open shell."
    print("Step 2: Confirmed that standard BRepBuilderAPI_MakeSolid produces an invalid solid.")
    # 步骤 2: 已确认标准的 BRepBuilderAPI_MakeSolid 生成了一个无效的实体。

    # 4. Use ShapeFix_Solid to repair the shell and create a solid.
    # 4. 使用 ShapeFix_Solid 来修复壳体并创建实体。
    # This tool can often infer the missing face to create a closed solid.
    # # 这个工具通常可以推断出缺失的面来创建一个闭合的实体。
    fixer = ShapeFix_Solid(a_solid)
    fixer.Perform()
    repaired_solid = fixer.Solid()
    print("Step 3: Used ShapeFix_Solid to attempt repair.")
    # 步骤 3: 已使用 ShapeFix_Solid 尝试修复。

    # 5. Verification
    # 5. 验证
    assert not repaired_solid.IsNull(), "ShapeFix should have created a valid solid."
    analyzer = BRepCheck_Analyzer(repaired_solid)
    assert analyzer.IsValid(), "The repaired solid should be valid."
    print("\nVerification successful: ShapeFix successfully repaired the shell into a valid solid.")
    # 验证成功：ShapeFix 成功地将壳体修复成一个有效的实体。

if __name__ == '__main__':
    repair_defective_shape()
