# -*- coding: utf-8 -*-

"""
This file demonstrates writing to and reading from an STL file using StlAPI.
# 本文件演示了如何使用 StlAPI 来写入和读取STL文件。

It builds upon the previous BRepMesh example. It first creates and meshes a shape,
writes the mesh to an STL file, and then reads it back for verification.
# 它基于前一个 BRepMesh 的示例。它首先创建并网格化一个形状，将网格写入STL文件，然后读回以进行验证。
"""

import os

# --- Imports ---
# --- 导入 ---
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.StlAPI import StlAPI_Writer, StlAPI_Reader
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Shell

def run_stl_example():
    """
    Runs the full mesh->write->read cycle for an STL file.
    # 运行STL文件的完整 网格化->写入->读取 循环。
    """
    print("--- STL File I/O Example ---")
    # --- STL 文件输入/输出示例 ---

    # 1. Create and mesh a shape (same as the BRepMesh example).
    # 1. 创建并网格化一个形状（与 BRepMesh 示例相同）。
    sphere_to_write = BRepPrimAPI_MakeSphere(50.0).Shape()
    BRepMesh_IncrementalMesh(sphere_to_write, 0.5)
    print("Step 1: Created and meshed a sphere.")
    # 步骤 1: 已创建并网格化一个球体。

    stl_file_path = "test_model.stl"

    # --- Part 2: Writing the STL file ---
    # --- 第2部分：写入STL文件 ---
    print(f"\n--- Writing meshed shape to {stl_file_path} ---")
    # --- 正在将网格化形状写入 {stl_file_path} ---
    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False)  # Use binary format for smaller file size
    # # 使用二进制格式以获得更小的文件体积
    
    write_status = stl_writer.Write(sphere_to_write, stl_file_path)
    assert write_status
    print(f"Successfully wrote file: {stl_file_path}")
    # 成功写入文件：{stl_file_path}

    # --- Part 3: Reading the STL file ---
    # --- 第3部分：读取STL文件 ---
    print(f"\n--- Reading shape from {stl_file_path} ---")
    # --- 正在从 {stl_file_path} 读取形状 ---
    # The reader needs an empty shape to populate.
    # # 读取器需要一个空的形状来填充数据。
    shape_to_read = TopoDS_Shape()
    stl_reader = StlAPI_Reader()
    read_status = stl_reader.Read(shape_to_read, stl_file_path)
    
    # --- Part 4: Verification ---
    # --- 第4部分：验证 ---
    print("\n--- Verifying the read shape ---")
    # --- 正在验证读取的形状 ---
    assert read_status
    assert not shape_to_read.IsNull()
    print("Verification successful: The shape was read back correctly.")
    # 验证成功：形状被正确读回。

    # --- Clean up the created file ---
    # --- 清理创建的文件 ---
    if os.path.exists(stl_file_path):
        os.remove(stl_file_path)
        print(f"\nCleaned up temporary file: {stl_file_path}")
        # 已清理临时文件：{stl_file_path}

if __name__ == '__main__':
    run_stl_example()
