# -*- coding: utf-8 -*- 

"""
This file demonstrates writing to and reading from a STEP file using STEPControl.
# 本文件演示了如何使用 STEPControl 来写入和读取STEP文件。

To make the example self-contained, it first creates a simple shape and writes it
to a STEP file. Then, it reads the same file back and verifies the content.
# 为了使示例能够独立运行，它首先创建一个简单的形状并将其写入STEP文件。然后，它会读回同一个文件并验证其内容。
"""

import os

# --- Imports for Shape Creation --- 
# --- 用于形状创建的导入 ---
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

# --- Imports for STEP file I/O ---
# --- 用于STEP文件输入/输出的导入 ---
from OCC.Core.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID

def create_test_shape():
    """
    Creates a simple box with a cylindrical hole.
    # 创建一个带有圆柱形孔的简单盒子。
    """
    box = BRepPrimAPI_MakeBox(100, 100, 50).Shape()
    cyl = BRepPrimAPI_MakeCylinder(25, 50).Shape()
    shape_to_write = BRepAlgoAPI_Cut(box, cyl).Shape()
    return shape_to_write

def run_step_example():
    """
    Runs the full write/read cycle for a STEP file.
    # 运行STEP文件的完整写入/读取循环。
    """
    print("--- STEP File I/O Example ---")
    # --- STEP 文件输入/输出示例 ---

    shape_to_write = create_test_shape()
    step_file_path = "test_model.step"

    # --- Part 1: Writing the STEP file ---
    # --- 第1部分：写入STEP文件 ---
    print(f"\n--- Writing shape to {step_file_path} ---")
    # --- 正在将形状写入 {step_file_path} ---
    step_writer = STEPControl_Writer()
    # Transfer the shape to the writer
    # # 将形状传输给写入器
    status = step_writer.Transfer(shape_to_write, STEPControl_AsIs)
    assert status == IFSelect_RetDone

    # Write the file
    # # 写入文件
    status = step_writer.Write(step_file_path)
    assert status == IFSelect_RetDone
    print(f"Successfully wrote file: {step_file_path}")
    # 成功写入文件：{step_file_path}

    # --- Part 2: Reading the STEP file ---
    # --- 第2部分：读取STEP文件 ---
    print(f"\n--- Reading shape from {step_file_path} ---")
    # --- 正在从 {step_file_path} 读取形状 ---
    step_reader = STEPControl_Reader()
    # Read the file
    # # 读取文件
    status = step_reader.ReadFile(step_file_path)
    
    if status == IFSelect_RetDone:
        print("STEP file read successfully.")
        # STEP 文件读取成功。
        # Transfer all roots from the file
        # # 从文件传输所有根实体
        step_reader.TransferRoots()
        # Get the resulting shape
        # # 获取结果形状
        read_shape = step_reader.Shape(1) # Get the first shape

        # --- Part 3: Verification ---
        # --- 第3部分：验证 ---
        print("\n--- Verifying the read shape ---")
        # --- 正在验证读取的形状 ---
        assert not read_shape.IsNull()
        
        # Count the number of solids in the read shape
        # # 计算读取的形状中实体的数量
        solid_explorer = TopExp_Explorer(read_shape, TopAbs_SOLID)
        solid_count = 0
        while solid_explorer.More():
            solid_count += 1
            solid_explorer.Next()
        
        print(f"The read shape contains {solid_count} solid(s).")
        # 读取的形状包含 {solid_count} 个实体。
        assert solid_count == 1
        print("Verification successful: Found 1 solid as expected.")
        # 验证成功：按预期找到了1个实体。
    else:
        print(f"Error: Could not read STEP file. Status: {status}")
        # 错误：无法读取STEP文件。状态：{status}

    # --- Clean up the created file ---
    # --- 清理创建的文件 ---
    if os.path.exists(step_file_path):
        os.remove(step_file_path)
        print(f"\nCleaned up temporary file: {step_file_path}")
        # 已清理临时文件：{step_file_path}

if __name__ == '__main__':
    run_step_example()
