# -*- coding: utf-8 -*-

"""
OCAF Example 3: Parametric CAD Application Prototype
# OCAF 示例 3: 参数化CAD应用原型

This script demonstrates a complete parametric CAD application prototype using OCAF.
It creates a parametric model of a box with a cylindrical hole, allowing users to
modify parameters and see real-time updates.
# 本脚本演示了一个使用OCAF的完整参数化CAD应用原型。
# 它创建了一个带圆柱孔的盒子的参数化模型，允许用户修改参数并查看实时更新。

Features demonstrated:
# 演示的功能：
1. Multi-parameter parametric modeling (width, height, depth, hole_radius)
# 1. 多参数参数化建模（宽度、高度、深度、孔半径）
2. Complex geometry generation (box with hole)
# 2. 复杂几何体生成（带孔的盒子）
3. Interactive parameter modification
# 3. 交互式参数修改
4. Real-time model updates
# 4. 实时模型更新
5. Model validation and error handling
# 5. 模型验证和错误处理
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Real, TDataStd_Name
from OCC.Core.TNaming import TNaming_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
import sys

class ParametricCADModel:
    """
    A complete parametric CAD model using OCAF.
    Creates a box with a cylindrical hole through the center.
    # 使用OCAF的完整参数化CAD模型。
    # 创建一个中心有圆柱孔的盒子。
    """

    def __init__(self, doc_name="ParametricCAD"):
        # Create OCAF document
        # 创建OCAF文档
        self.doc = TDocStd_Document(doc_name)

        # Set up label structure
        # 设置标签结构
        self.root_label = self.doc.Main()
        self.params_label = self.root_label.FindChild(1, True)
        self.geometry_label = self.root_label.FindChild(2, True)

        # Add names to organize the structure
        # 添加名称来组织结构
        TDataStd_Name.Set(self.params_label, "Parameters")
        TDataStd_Name.Set(self.geometry_label, "Geometry")

        # Parameter attribute handles
        # 参数属性句柄
        self.width_attr = None
        self.height_attr = None
        self.depth_attr = None
        self.hole_radius_attr = None

        # Geometry attribute handles
        # 几何体属性句柄
        self.box_attr = None
        self.hole_attr = None
        self.result_attr = None

        # Current geometry cache
        # 当前几何体缓存
        self.current_shape = None

    def initialize_parameters(self, width=100.0, height=80.0, depth=60.0, hole_radius=15.0):
        """Initialize all parameters with default values."""
        self.doc.NewCommand()

        # Create parameter labels with descriptive names
        # 创建带有描述性名称的参数标签
        width_label = self.params_label.FindChild(1, True)
        height_label = self.params_label.FindChild(2, True)
        depth_label = self.params_label.FindChild(3, True)
        hole_radius_label = self.params_label.FindChild(4, True)

        # Set names for better organization
        # 设置名称以便更好地组织
        TDataStd_Name.Set(width_label, "Width")
        TDataStd_Name.Set(height_label, "Height")
        TDataStd_Name.Set(depth_label, "Depth")
        TDataStd_Name.Set(hole_radius_label, "HoleRadius")

        # Set parameter values and store attribute handles
        # 设置参数值并存储属性句柄
        self.width_attr = TDataStd_Real.Set(width_label, width)
        self.height_attr = TDataStd_Real.Set(height_label, height)
        self.depth_attr = TDataStd_Real.Set(depth_label, depth)
        self.hole_radius_attr = TDataStd_Real.Set(hole_radius_label, hole_radius)

        self.doc.CommitCommand()
        print(f"Parameters initialized: W={width}, H={height}, D={depth}, R={hole_radius}")

    def get_parameters(self):
        """Get current parameter values."""
        if not all([self.width_attr, self.height_attr, self.depth_attr, self.hole_radius_attr]):
            raise RuntimeError("Parameters not initialized. Call initialize_parameters() first.")

        return {
            'width': self.width_attr.Get(),
            'height': self.height_attr.Get(),
            'depth': self.depth_attr.Get(),
            'hole_radius': self.hole_radius_attr.Get()
        }

    def update_parameter(self, param_name, value):
        """Update a specific parameter."""
        if value <= 0:
            raise ValueError(f"Parameter {param_name} must be positive, got {value}")

        self.doc.NewCommand()

        param_map = {
            'width': self.width_attr,
            'height': self.height_attr,
            'depth': self.depth_attr,
            'hole_radius': self.hole_radius_attr
        }

        if param_name not in param_map:
            raise ValueError(f"Unknown parameter: {param_name}")

        # Validate hole radius doesn't exceed box dimensions
        # 验证孔半径不超过盒子尺寸
        if param_name == 'hole_radius':
            params = self.get_parameters()
            min_dimension = min(params['width'], params['height']) / 2
            if value >= min_dimension:
                raise ValueError(f"Hole radius {value} too large. Max allowed: {min_dimension:.1f}")

        param_map[param_name].Set(value)
        self.doc.CommitCommand()
        print(f"Parameter '{param_name}' updated to {value}")

    def regenerate_geometry(self):
        """
        Regenerate the complete geometry based on current parameters.
        Creates a box with a cylindrical hole through the center.
        # 基于当前参数重新生成完整几何体。
        # 创建一个中心有圆柱孔的盒子。
        """
        params = self.get_parameters()
        W, H, D, R = params['width'], params['height'], params['depth'], params['hole_radius']

        try:
            # Create the main box
            # 创建主盒子
            box = BRepPrimAPI_MakeBox(W, H, D).Shape()

            # Create the cylindrical hole
            # 创建圆柱孔
            # Position the cylinder at the center of the box, extending through its full height
            # 将圆柱定位在盒子中心，延伸穿过整个高度
            hole_center = gp_Pnt(W/2, H/2, -D/10)  # Start slightly below the box
            hole_axis = gp_Ax2(hole_center, gp_Dir(0, 0, 1))  # Z-axis direction
            cylinder = BRepPrimAPI_MakeCylinder(hole_axis, R, D * 1.2).Shape()  # Make it longer than the box

            # Cut the hole from the box
            # 从盒子中切除孔
            cut_operation = BRepAlgoAPI_Cut(box, cylinder)
            cut_operation.Build()

            if not cut_operation.IsDone():
                raise RuntimeError("Boolean cut operation failed")

            result_shape = cut_operation.Shape()

            # Store geometry in OCAF
            # 在OCAF中存储几何体
            self.doc.NewCommand()

            # Store individual components
            # 存储各个组件
            box_label = self.geometry_label.FindChild(1, True)
            hole_label = self.geometry_label.FindChild(2, True)
            result_label = self.geometry_label.FindChild(3, True)

            TDataStd_Name.Set(box_label, "Box")
            TDataStd_Name.Set(hole_label, "Hole")
            TDataStd_Name.Set(result_label, "Result")

            # Store shapes using TNaming
            # 使用TNaming存储形状
            box_builder = TNaming_Builder(box_label)
            box_builder.Generated(box)
            self.box_attr = box_builder.NamedShape()

            hole_builder = TNaming_Builder(hole_label)
            hole_builder.Generated(cylinder)
            self.hole_attr = hole_builder.NamedShape()

            result_builder = TNaming_Builder(result_label)
            result_builder.Generated(result_shape)
            self.result_attr = result_builder.NamedShape()

            self.doc.CommitCommand()

            # Cache the result
            # 缓存结果
            self.current_shape = result_shape

            print(f"Geometry regenerated: Box({W}×{H}×{D}) with hole(R={R})")
            return result_shape

        except Exception as e:
            print(f"Error during geometry regeneration: {e}")
            raise

    def get_current_shape(self):
        """Get the current result shape."""
        if self.result_attr:
            return self.result_attr.Get()
        return self.current_shape

    def validate_model(self):
        """Validate the current model and return statistics."""
        shape = self.get_current_shape()
        if not shape:
            return {"valid": False, "error": "No shape available"}

        try:
            # Calculate volume
            # 计算体积
            props = GProp_GProps()
            brepgprop.VolumeProperties(shape, props)
            volume = props.Mass()

            # Count solids
            # 计算实体数量
            solid_count = 0
            explorer = TopExp_Explorer(shape, TopAbs_SOLID)
            while explorer.More():
                solid_count += 1
                explorer.Next()

            # Calculate expected volume (box - cylinder)
            # 计算期望体积（盒子 - 圆柱）
            params = self.get_parameters()
            box_volume = params['width'] * params['height'] * params['depth']
            hole_volume = 3.14159 * params['hole_radius']**2 * params['depth']
            expected_volume = box_volume - hole_volume

            return {
                "valid": True,
                "volume": volume,
                "expected_volume": expected_volume,
                "volume_error": abs(volume - expected_volume),
                "solid_count": solid_count,
                "parameters": params
            }

        except Exception as e:
            return {"valid": False, "error": str(e)}

    def print_model_info(self):
        """Print comprehensive model information."""
        print("\n" + "="*60)
        print("PARAMETRIC CAD MODEL INFORMATION")
        print("="*60)

        validation = self.validate_model()
        if validation["valid"]:
            params = validation["parameters"]
            print(f"Parameters:")
            print(f"  Width:       {params['width']:.2f}")
            print(f"  Height:      {params['height']:.2f}")
            print(f"  Depth:       {params['depth']:.2f}")
            print(f"  Hole Radius: {params['hole_radius']:.2f}")
            print(f"\nGeometry:")
            print(f"  Volume:      {validation['volume']:.2f}")
            print(f"  Expected:    {validation['expected_volume']:.2f}")
            print(f"  Error:       {validation['volume_error']:.2f}")
            print(f"  Solids:      {validation['solid_count']}")
        else:
            print(f"Model validation failed: {validation['error']}")

        print("="*60)

def interactive_demo():
    """
    Interactive demonstration of the parametric CAD application.
    # 参数化CAD应用的交互式演示。
    """
    print("=== PARAMETRIC CAD APPLICATION DEMO ===")
    print("This demo creates a parametric box with a cylindrical hole.")
    print("You can modify parameters and see real-time updates.")
    print()

    # Create the model
    # 创建模型
    model = ParametricCADModel("InteractiveCAD")

    # Initialize with default parameters
    # 使用默认参数初始化
    model.initialize_parameters(width=120.0, height=100.0, depth=80.0, hole_radius=20.0)

    # Generate initial geometry
    # 生成初始几何体
    print("Generating initial geometry...")
    model.regenerate_geometry()
    model.print_model_info()

    # Interactive loop
    # 交互循环
    while True:
        print("\n" + "-"*50)
        print("INTERACTIVE MENU:")
        print("1. Modify Width")
        print("2. Modify Height")
        print("3. Modify Depth")
        print("4. Modify Hole Radius")
        print("5. Show Model Info")
        print("6. Regenerate Geometry")
        print("7. Reset to Defaults")
        print("0. Exit")
        print("-"*50)

        try:
            choice = input("Enter your choice (0-7): ").strip()

            if choice == '0':
                print("Exiting parametric CAD demo. Goodbye!")
                break

            elif choice == '1':
                value = float(input("Enter new width (current: {:.1f}): ".format(model.get_parameters()['width'])))
                model.update_parameter('width', value)
                model.regenerate_geometry()

            elif choice == '2':
                value = float(input("Enter new height (current: {:.1f}): ".format(model.get_parameters()['height'])))
                model.update_parameter('height', value)
                model.regenerate_geometry()

            elif choice == '3':
                value = float(input("Enter new depth (current: {:.1f}): ".format(model.get_parameters()['depth'])))
                model.update_parameter('depth', value)
                model.regenerate_geometry()

            elif choice == '4':
                current_radius = model.get_parameters()['hole_radius']
                params = model.get_parameters()
                max_radius = min(params['width'], params['height']) / 2 - 5  # Leave some margin
                value = float(input(f"Enter new hole radius (current: {current_radius:.1f}, max: {max_radius:.1f}): "))
                model.update_parameter('hole_radius', value)
                model.regenerate_geometry()

            elif choice == '5':
                model.print_model_info()

            elif choice == '6':
                print("Regenerating geometry...")
                model.regenerate_geometry()
                print("Geometry regenerated successfully!")

            elif choice == '7':
                print("Resetting to default parameters...")
                model.initialize_parameters()
                model.regenerate_geometry()
                print("Reset complete!")

            else:
                print("Invalid choice. Please enter a number between 0-7.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

def automated_demo():
    """
    Automated demonstration showing various parameter combinations.
    # 自动演示，展示各种参数组合。
    """
    print("=== AUTOMATED PARAMETRIC DEMO ===")
    print("This demo automatically tests various parameter combinations.")
    print()

    model = ParametricCADModel("AutomatedDemo")

    # Test cases: (width, height, depth, hole_radius, description)
    # 测试用例：(宽度, 高度, 深度, 孔半径, 描述)
    test_cases = [
        (100, 80, 60, 15, "Default small box"),
        (200, 150, 100, 30, "Large box"),
        (80, 80, 40, 10, "Compact square box"),
        (150, 100, 200, 25, "Tall narrow box"),
        (120, 120, 80, 35, "Wide hole test")
    ]

    for i, (w, h, d, r, desc) in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {desc} ---")
        try:
            if i == 1:
                model.initialize_parameters(w, h, d, r)
            else:
                model.update_parameter('width', w)
                model.update_parameter('height', h)
                model.update_parameter('depth', d)
                model.update_parameter('hole_radius', r)

            model.regenerate_geometry()
            validation = model.validate_model()

            if validation["valid"]:
                print(f"✓ Success: Volume = {validation['volume']:.1f}")
            else:
                print(f"✗ Failed: {validation['error']}")

        except Exception as e:
            print(f"✗ Error in test case {i}: {e}")

    print(f"\n--- Final Model State ---")
    model.print_model_info()

def run_demo():
    """Main demo function with user choice."""
    print("OCAF PARAMETRIC CAD APPLICATION")
    print("Choose demo mode:")
    print("1. Interactive Demo (modify parameters manually)")
    print("2. Automated Demo (test various configurations)")
    print("3. Both")

    try:
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            interactive_demo()
        elif choice == '2':
            automated_demo()
        elif choice == '3':
            automated_demo()
            print("\n" + "="*60)
            print("SWITCHING TO INTERACTIVE MODE")
            print("="*60)
            interactive_demo()
        else:
            print("Invalid choice. Running automated demo by default.")
            automated_demo()

    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    run_demo()
