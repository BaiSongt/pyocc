# -*- coding: utf-8 -*- 

"""
This file demonstrates the use of the `ShapeFix` package to repair a defective shape.
# 本文件演示了如何使用 `ShapeFix` 包来修复一个有缺陷的形状。

It shows how to:
# 它展示了如何：
1. Intentionally create a defective shape (a closed shell with one face reversed).
# 1. 故意创建一个有缺陷的形状（一个其中一个面被反转的闭合壳体）。
2. Show that this results in an invalid solid.
# 2. 展示这会导致一个无效的实体。
3. Use `ShapeFix_Shell` to automatically repair the face orientation.
# 3. 使用 `ShapeFix_Shell` 自动修复面的方向。
4. Create a valid solid from the repaired shell.
# 4. 从修复后的壳体创建一个有效的实体。
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
from OCC.Core.ShapeFix import ShapeFix_Shell
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import TopoDS_Shell, TopoDS_Builder
from OCC.Core.BRepCheck import BRepCheck_Analyzer

def repair_defective_shape():
    """
    Creates a shell with a reversed face and repairs it.
    # 创建一个带有反转面的壳体并将其修复。
    """
    print("--- Repairing a Shape with a Reversed Face using ShapeFix ---")
    # --- 正在使用 ShapeFix 修复一个带有反转面的形状 ---

    # 1. Create a standard box and extract its faces.
    # 1. 创建一个标准的盒子并提取其所有面。
    the_box = BRepPrimAPI_MakeBox(100, 100, 100).Shape()
    face_explorer = TopExp_Explorer(the_box, TopAbs_FACE)
    list_of_faces = []
    while face_explorer.More():
        list_of_faces.append(face_explorer.Current())
        face_explorer.Next()
    
    # 2. Intentionally create a defective shell by reversing one face.
    # 2. 通过反转一个面来故意创建一个有缺陷的壳体。
    list_of_faces[0].Reverse() # Reverse the first face
    # # 反转第一个面

    builder = TopoDS_Builder()
    defective_shell = TopoDS_Shell()
    builder.MakeShell(defective_shell)
    for a_face in list_of_faces:
        builder.Add(defective_shell, a_face)
    
    print("Step 1: Created a defective shell with one face reversed.")
    # 步骤 1: 已创建一个其中一个面被反转的有缺陷的壳体。

    # 3. Create a solid from the defective shell and verify it's invalid.
    # 3. 从有缺陷的壳体创建实体并验证其无效。
    mk_solid = BRepBuilderAPI_MakeSolid(defective_shell)
    invalid_solid = mk_solid.Solid()
    analyzer1 = BRepCheck_Analyzer(invalid_solid)
    assert not analyzer1.IsValid(), "Solid with reversed face should be invalid."
    print("Step 2: Confirmed that the solid built from the defective shell is invalid.")
    # 步骤 2: 已确认从有缺陷的壳体构建的实体是无效的。

    # 4. Use ShapeFix_Shell to repair the face orientations.
    # 4. 使用 ShapeFix_Shell 来修复面的方向。
    fixer = ShapeFix_Shell(defective_shell)
    fixer.Perform()
    repaired_shell = fixer.Shell()
    print("Step 3: Used ShapeFix_Shell to repair face orientations.")
    # 步骤 3: 已使用 ShapeFix_Shell 修复面的方向。

    # 5. Create a new solid from the REPAIRED shell and verify it's now valid.
    # 5. 从被修复的壳体创建一个新实体并验证它现在是有效的。
    mk_repaired_solid = BRepBuilderAPI_MakeSolid(repaired_shell)
    valid_solid = mk_repaired_solid.Solid()
    analyzer2 = BRepCheck_Analyzer(valid_solid)
    assert analyzer2.IsValid(), "The solid from the repaired shell should be valid."
    print("\nVerification successful: ShapeFix successfully repaired the shell, resulting in a valid solid.")
    # 验证成功：ShapeFix 成功修复了壳体，并得到了一个有效的实体。

if __name__ == '__main__':
    repair_defective_shape()