# -*- coding: utf-8 -*- 

"""
Phase 3 Summary Example: Interoperability and Meshing
# 第三阶段汇总示例：数据交换与网格化

This script demonstrates a complete interoperability workflow:
# 本脚本演示了一个完整的数据交换工作流：

1.  A source shape is created and saved as a STEP file (the "input").
    # 1. 创建一个源形状并将其另存为STEP文件（“输入”）。
2.  The STEP file is read back using `STEPControl_Reader`.
    # 2. 使用 `STEPControl_Reader` 读回该STEP文件。
3.  The B-Rep shape is converted to a mesh using `BRepMesh_IncrementalMesh`.
    # 3. 使用 `BRepMesh_IncrementalMesh` 将B-Rep形状转换为网格。
4.  The resulting mesh is saved as an STL file using `StlAPI_Writer` (the "output").
    # 4. 使用 `StlAPI_Writer` 将生成的网格另存为STL文件（“输出”）。
"""

import os

# --- Imports ---
# --- 导入 ---
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.TopoDS import TopoDS_Shape

def create_source_step_file(file_path: str):
    """
    Creates a complex shape and saves it as a STEP file.
    # 创建一个复杂形状并将其另存为STEP文件。
    """
    print("--- Step 1: Creating source STEP file ---")
    # --- 步骤 1: 创建源STEP文件 ---
    box = BRepPrimAPI_MakeBox(100, 100, 100).Shape()
    sphere = BRepPrimAPI_MakeSphere(75).Shape()
    source_shape = BRepAlgoAPI_Fuse(box, sphere).Shape()

    step_writer = STEPControl_Writer()
    step_writer.Transfer(source_shape, STEPControl_AsIs)
    status = step_writer.Write(file_path)

    if status == IFSelect_RetDone:
        print(f"Successfully created source file: {file_path}")
        # 成功创建源文件：{file_path}
        return True
    else:
        print(f"Failed to create source file: {file_path}")
        # 创建源文件失败：{file_path}
        return False

def process_step_to_stl(in_step_path: str, out_stl_path: str):
    """
    Reads a STEP file, meshes the shape, and writes an STL file.
    # 读取一个STEP文件，对形状进行网格化，然后写入一个STL文件。
    """
    # --- Step 2: Read the STEP file ---
    # --- 步骤 2: 读取STEP文件 ---
    print(f"\n--- Step 2: Reading {in_step_path} ---")
    # --- 步骤 2: 正在读取 {in_step_path} ---
    step_reader = STEPControl_Reader()
    read_status = step_reader.ReadFile(in_step_path)
    if read_status != IFSelect_RetDone:
        print("Error: Could not read source STEP file.")
        # 错误：无法读取源STEP文件。
        return

    step_reader.TransferRoots()
    shape_from_step = step_reader.Shape(1)
    print("STEP file read and shape transferred successfully.")
    # STEP文件读取和形状转换成功。

    # --- Step 3: Mesh the B-Rep shape ---
    # --- 步骤 3: 对B-Rep形状进行网格化 ---
    print("\n--- Step 3: Meshing the shape ---")
    # --- 步骤 3: 正在对形状进行网格化 ---
    linear_deflection = 1.0
    BRepMesh_IncrementalMesh(shape_from_step, linear_deflection)
    print(f"Meshing complete with linear deflection {linear_deflection}.")
    # 已使用线性挠度 {linear_deflection} 完成网格化。

    # --- Step 4: Write the STL file ---
    # --- 步骤 4: 写入STL文件 ---
    print(f"\n--- Step 4: Writing mesh to {out_stl_path} ---")
    # --- 步骤 4: 正在将网格写入 {out_stl_path} ---
    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False) # Binary format
    # # 二进制格式
    write_status = stl_writer.Write(shape_from_step, out_stl_path)
    if not write_status:
        print("Error: Could not write STL file.")
        # 错误：无法写入STL文件。
        return
    
    print("STL file written successfully.")
    # STL文件写入成功。

if __name__ == "__main__":
    step_file = "source_model.step"
    stl_file = "output_mesh.stl"

    if create_source_step_file(step_file):
        process_step_to_stl(step_file, stl_file)

    # --- Clean up temporary files ---
    # --- 清理临时文件 ---
    print("\n--- Cleaning up temporary files ---")
    # --- 正在清理临时文件 ---
    for f in [step_file, stl_file]:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed: {f}")
            # 已移除：{f}

