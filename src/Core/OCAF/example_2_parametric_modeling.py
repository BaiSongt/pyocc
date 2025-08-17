# -*- coding: utf-8 -*- 

"""
OCAF Example 2: Parametric Modeling (Corrected)
# OCAF 示例 2: 参数化建模（已修正）

This script demonstrates a simplified, robust approach to parametric modeling in
`pythonocc-core`, following the solution summary. It uses a custom Python class
to manage parameters and regeneration logic, avoiding the problematic TFunction API.
# 本脚本根据解决方案总结，演示了一种在`pythonocc-core`中进行参数化建模的、简化的、健壮的方法。
# 它使用一个自定义的Python类来管理参数和再生逻辑，从而避免了有问题的TFunction API。

It shows how to:
# 它展示了如何：
1. Encapsulate OCAF parameters and geometry regeneration in a class.
# 1. 将OCAF参数和几何再生逻辑封装在一个类中。
2. Store and reuse attribute handles for parameters and shapes.
# 2. 存储并复用参数和形状的属性句柄。
3. Modify a parameter and trigger a regeneration to update the geometry.
# 3. 修改一个参数并触发再生，以更新几何体。
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Real
from OCC.Core.TNaming import TNaming_Builder, TNaming_NamedShape
from OCC.Core.TDF import TDF_Label
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps

# 1. Define a custom class to manage the parametric model
# 1. 定义一个自定义类来管理参数化模型
class ParametricBoxModel:
    def __init__(self, doc: TDocStd_Document):
        # Store the document and set up the label structure
        # # 存储文档并设置标签结构
        self.doc = doc
        self.root_label = doc.Main()
        self.params_label = self.root_label.FindChild(1, True)
        self.result_label = self.root_label.FindChild(2, True)
        
        # Placeholders for attribute handles
        # # 属性句柄的占位符
        self.length_attr = None
        self.width_attr = None
        self.height_attr = None
        self.shape_attr = None

    def setup_parameters(self, length: float, width: float, height: float):
        """
        Sets the initial parameter values and stores their attribute handles.
        # 设置初始参数值并存储它们的属性句柄。
        """
        self.doc.NewCommand() # Start transaction
        # # 开始事务
        self.length_attr = TDataStd_Real.Set(self.params_label.FindChild(1, True), length)
        self.width_attr = TDataStd_Real.Set(self.params_label.FindChild(2, True), width)
        self.height_attr = TDataStd_Real.Set(self.params_label.FindChild(3, True), height)
        self.doc.CommitCommand() # Commit transaction
        # # 提交事务
        print(f"Parameters initialized: L={length}, W={width}, H={height}")
        # 参数已初始化: L=..., W=..., H=...

    def regenerate_geometry(self):
        """
        Reads the current parameter values and regenerates the box shape.
        # 读取当前参数值并重新生成盒子形状。
        """
        self.doc.NewCommand()
        # Get current values from stored handles
        # # 从已存储的句柄中获取当前值
        L = self.length_attr.Get()
        W = self.width_attr.Get()
        H = self.height_attr.Get()

        # Create the geometry
        # # 创建几何体
        box = BRepPrimAPI_MakeBox(L, W, H).Shape()

        # Store the shape using TNaming_Builder and save the handle
        # # 使用 TNaming_Builder 存储形状并保存句柄
        builder = TNaming_Builder(self.result_label)
        builder.Generated(box)
        self.shape_attr = builder.NamedShape()
        self.doc.CommitCommand()
        print(f"Geometry regenerated: Box({L}, {W}, {H})")
        # 几何已再生: Box(...)

    def get_current_shape(self):
        """
        Returns the current TopoDS_Shape from the document.
        # 从文档中返回当前的 TopoDS_Shape。
        """
        if self.shape_attr is not None:
            return self.shape_attr.Get()
        return None

def run_parametric_example():
    print("=== OCAF Parametric Modeling Example ===")
    # === OCAF 参数化建模示例 ===

    # Create the document and our model manager
    # # 创建文档和我们的模型管理器
    doc = TDocStd_Document("ocaf-doc")
    model = ParametricBoxModel(doc)

    # Set initial parameters and generate the first shape
    # # 设置初始参数并生成第一个形状
    model.setup_parameters(100.0, 80.0, 60.0)
    model.regenerate_geometry()

    # Verify the initial volume
    # # 验证初始体积
    initial_shape = model.get_current_shape()
    props = GProp_GProps()
    brepgprop.VolumeProperties(initial_shape, props)
    volume = props.Mass()
    expected_volume = 100.0 * 80.0 * 60.0
    assert abs(volume - expected_volume) < 1e-3
    print(f"Volume verification: Actual={volume:.2f}, Expected={expected_volume:.2f}")
    # 体积验证: 实际=..., 预期=...

    # --- Modify a parameter and see the model update ---
    # --- 修改一个参数并观察模型更新 ---
    print("\nParameter 'length' updated to 150.0")
    # 参数“长度”已更新为 150.0
    model.doc.NewCommand()
    model.length_attr.Set(150.0) # Directly modify the parameter using the stored handle
    # # 直接使用已存储的句柄修改参数
    model.doc.CommitCommand()

    # Regenerate the geometry after the parameter change
    # # 参数更改后重新生成几何体
    model.regenerate_geometry()

    # Verify the new volume
    # # 验证新体积
    final_shape = model.get_current_shape()
    brepgprop.VolumeProperties(final_shape, props)
    volume = props.Mass()
    expected_volume = 150.0 * 80.0 * 60.0
    assert abs(volume - expected_volume) < 1e-3
    print(f"Volume verification: Actual={volume:.2f}, Expected={expected_volume:.2f}")
    # 体积验证: 实际=..., 预期=...

    print("\nSuccess: Parametric modeling demonstration completed.")
    # 成功：参数化建模演示完成

if __name__ == "__main__":
    run_parametric_example()
