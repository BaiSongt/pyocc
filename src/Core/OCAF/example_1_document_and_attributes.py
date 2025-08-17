# -*- coding: utf-8 -*-

"""
OCAF Example 1: Document, Labels, and Standard Attributes (Corrected)
# OCAF 示例 1: 文档、标签与标准属性（已修正）

This script demonstrates the fundamental concepts of the OCAF framework using the
correct API patterns for attribute handling in `pythonocc-core`.
# 本脚本使用 `pythonocc-core` 中属性处理的正确API模式，演示了OCAF框架的基本概念。

Key takeaway: The attribute object returned by the `.Set()` method should be stored
and reused, avoiding the need for a subsequent `.Find()` call.
# 核心要点：由`.Set()`方法返回的属性对象应该被存储和复用，从而避免了后续的`.Find()`调用。
"""

import math

# --- Imports ---
# --- 导入 --- 
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Real
from OCC.Core.TDF import TDF_Label

def build_parameter_tree_correctly():
    """
    Builds and verifies a simple OCAF document with a parameter tree.
    # 构建并验证一个带有参数树的简单OCAF文档。
    """
    print("--- Building an OCAF Parameter Tree (Correct Method) ---")
    # --- 正在构建一个OCAF参数树（正确方法） --- 

    # 1. Create a new OCAF document.
    # 1. 创建一个新的OCAF文档。
    doc = TDocStd_Document("ocaf-doc")

    # 2. Create a transaction to wrap the modifications.
    # 2. 创建一个事务来包裹所有的修改操作。
    doc.NewCommand()

    # 3. Create labels and set attributes, storing the returned attribute object.
    # 3. 创建标签并设置属性，同时存储返回的属性对象。
    params_label = doc.Main().FindChild(1, True)
    
    length_label = params_label.FindChild(1, True)
    length_attr = TDataStd_Real.Set(length_label, 100.0)

    width_label = params_label.FindChild(2, True)
    width_attr = TDataStd_Real.Set(width_label, 80.0)

    height_label = params_label.FindChild(3, True)
    height_attr = TDataStd_Real.Set(height_label, 60.0)

    # 4. Commit the transaction.
    # 4. 提交事务。
    doc.CommitCommand()
    print("Step 1: Document structure created and transaction committed.")
    # 步骤 1: 已创建文档结构并提交事务。

    # 5. Verification: Use the stored attribute handles directly.
    # 5. 验证：直接使用已存储的属性句柄。
    print("\n--- Verifying the data using stored attribute handles ---")
    # --- 正在使用已存储的属性句柄验证数据 --- 
    
    length_val = length_attr.Get()
    print(f"Retrieved Length = {length_val}")
    # 检索到的长度 = {length_val}
    assert math.isclose(length_val, 100.0)

    width_val = width_attr.Get()
    print(f"Retrieved Width = {width_val}")
    # 检索到的宽度 = {width_val}
    assert math.isclose(width_val, 80.0)

    height_val = height_attr.Get()
    print(f"Retrieved Height = {height_val}")
    # 检索到的高度 = {height_val}
    assert math.isclose(height_val, 60.0)

    print("\nVerification successful: All parameters were set and retrieved correctly.")
    # 验证成功：所有参数都已正确设置和检索。

if __name__ == '__main__':
    build_parameter_tree_correctly()
