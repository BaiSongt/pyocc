# -*- coding: utf-8 -*-

"""
OCAF Example 3: Automated Parametric CAD Demo
# OCAF 示例 3: 自动化参数化CAD演示

This script provides a non-interactive demonstration of the parametric CAD application.
It automatically tests various parameter combinations and showcases the capabilities
of OCAF for parametric modeling.
# 本脚本提供参数化CAD应用的非交互式演示。
# 它自动测试各种参数组合，展示OCAF在参数化建模方面的能力。
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
import math

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
        self.result_attr = None
        
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
            
            result_label = self.geometry_label.FindChild(1, True)
            TDataStd_Name.Set(result_label, "Result")
            
            # Store shape using TNaming
            # 使用TNaming存储形状
            result_builder = TNaming_Builder(result_label)
            result_builder.Generated(result_shape)
            self.result_attr = result_builder.NamedShape()
            
            self.doc.CommitCommand()
            
            return result_shape
            
        except Exception as e:
            print(f"Error during geometry regeneration: {e}")
            raise
            
    def get_current_shape(self):
        """Get the current result shape."""
        if self.result_attr:
            return self.result_attr.Get()
        return None
        
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
            hole_volume = math.pi * params['hole_radius']**2 * params['depth']
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

def run_comprehensive_demo():
    """
    Run a comprehensive demonstration of the parametric CAD system.
    # 运行参数化CAD系统的综合演示。
    """
    print("="*70)
    print("OCAF PARAMETRIC CAD APPLICATION - COMPREHENSIVE DEMO")
    print("="*70)
    print("This demo showcases a complete parametric CAD application using OCAF.")
    print("Features: Multi-parameter modeling, complex geometry, real-time updates")
    print()
    
    # Create the model
    # 创建模型
    model = ParametricCADModel("ComprehensiveDemo")
    
    # Test cases with different parameter combinations
    # 不同参数组合的测试用例
    test_cases = [
        {
            "name": "Small Precision Part",
            "params": {"width": 50, "height": 40, "depth": 30, "hole_radius": 8},
            "description": "Small precision component with tight tolerances"
        },
        {
            "name": "Standard Box",
            "params": {"width": 100, "height": 80, "depth": 60, "hole_radius": 15},
            "description": "Standard sized box for general applications"
        },
        {
            "name": "Large Industrial Part",
            "params": {"width": 200, "height": 150, "depth": 100, "hole_radius": 30},
            "description": "Large industrial component"
        },
        {
            "name": "Thin Plate",
            "params": {"width": 120, "height": 80, "depth": 20, "hole_radius": 12},
            "description": "Thin plate with central hole"
        },
        {
            "name": "Square Block",
            "params": {"width": 90, "height": 90, "depth": 90, "hole_radius": 25},
            "description": "Cubic block with large central hole"
        }
    ]
    
    # Run test cases
    # 运行测试用例
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['name']} ---")
        print(f"Description: {test_case['description']}")
        
        try:
            # Initialize or update parameters
            # 初始化或更新参数
            if i == 1:
                model.initialize_parameters(**test_case['params'])
            else:
                for param_name, value in test_case['params'].items():
                    model.update_parameter(param_name, value)
            
            # Generate geometry
            # 生成几何体
            print("Generating geometry...")
            model.regenerate_geometry()
            
            # Validate model
            # 验证模型
            validation = model.validate_model()
            
            if validation["valid"]:
                params = validation["parameters"]
                print(f"✓ Success!")
                print(f"  Parameters: W={params['width']}, H={params['height']}, D={params['depth']}, R={params['hole_radius']}")
                print(f"  Volume: {validation['volume']:.1f} (Expected: {validation['expected_volume']:.1f})")
                print(f"  Error: {validation['volume_error']:.2f}")
                print(f"  Solids: {validation['solid_count']}")
            else:
                print(f"✗ Failed: {validation['error']}")
                
        except Exception as e:
            print(f"✗ Error in test case {i}: {e}")
    
    # Demonstrate parameter modification
    # 演示参数修改
    print(f"\n--- Parameter Modification Demo ---")
    print("Demonstrating real-time parameter updates...")
    
    try:
        original_params = model.get_parameters()
        print(f"Original parameters: {original_params}")
        
        # Modify width
        # 修改宽度
        new_width = original_params['width'] * 1.5
        model.update_parameter('width', new_width)
        model.regenerate_geometry()
        print(f"✓ Width updated to {new_width}")
        
        # Modify hole radius
        # 修改孔半径
        new_radius = original_params['hole_radius'] * 0.8
        model.update_parameter('hole_radius', new_radius)
        model.regenerate_geometry()
        print(f"✓ Hole radius updated to {new_radius}")
        
        # Final validation
        # 最终验证
        final_validation = model.validate_model()
        if final_validation["valid"]:
            print(f"✓ Final model valid with volume: {final_validation['volume']:.1f}")
        
    except Exception as e:
        print(f"✗ Parameter modification error: {e}")
    
    # Summary
    # 总结
    print(f"\n" + "="*70)
    print("DEMO SUMMARY")
    print("="*70)
    print("✓ OCAF document structure created and managed")
    print("✓ Multi-parameter parametric modeling demonstrated")
    print("✓ Complex geometry generation (box with hole)")
    print("✓ Real-time parameter updates")
    print("✓ Model validation and error handling")
    print("✓ Robust error handling and parameter constraints")
    print()
    print("This demo showcases the power of OCAF for building")
    print("professional parametric CAD applications!")
    print("="*70)

if __name__ == "__main__":
    run_comprehensive_demo()
