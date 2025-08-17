# -*- coding: utf-8 -*-

"""
Phase 6: OCAF Parametric Modeling - Comprehensive Example
第六阶段：OCAF参数化建模 - 综合示例

This example demonstrates the complete OCAF (OpenCASCADE Application Framework)
capabilities for building parametric CAD applications. It showcases:
本示例演示了完整的OCAF（OpenCASCADE应用框架）构建参数化CAD应用的能力。它展示了：

1. OCAF Document Structure and Management
   OCAF文档结构和管理
2. Hierarchical Label Organization
   分层标签组织
3. Attribute-based Parameter Storage
   基于属性的参数存储
4. Parametric Geometry Generation
   参数化几何生成
5. Real-time Model Updates
   实时模型更新
6. Complex Boolean Operations
   复杂布尔运算
7. Model Validation and Error Handling
   模型验证和错误处理

This is the culmination of Phase 6 learning objectives.
这是第六阶段学习目标的总结。
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Real, TDataStd_Name, TDataStd_Integer
from OCC.Core.TNaming import TNaming_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
import math
import time

class ParametricCADApplication:
    """
    Complete Parametric CAD Application using OCAF
    使用OCAF的完整参数化CAD应用

    This class demonstrates all key OCAF concepts:
    这个类演示了所有关键的OCAF概念：
    - Document management and label hierarchy
      文档管理和标签层次
    - Attribute-based data storage
      基于属性的数据存储
    - Parametric geometry generation
      参数化几何生成
    - Real-time updates and validation
      实时更新和验证
    """

    def __init__(self, app_name="ParametricCAD_Phase6"):
        """Initialize the OCAF application."""
        print("="*60)
        print("PHASE 6: OCAF PARAMETRIC CAD APPLICATION")
        print("第六阶段：OCAF参数化CAD应用")
        print("="*60)

        # Create OCAF document
        # 创建OCAF文档
        self.doc = TDocStd_Document(app_name)
        self.setup_document_structure()

        # Parameter attributes (using correct API pattern)
        # 参数属性（使用正确的API模式）
        self.width_attr = None
        self.height_attr = None
        self.depth_attr = None
        self.hole_radius_attr = None
        self.model_version_attr = None

        # Geometry attributes
        # 几何属性
        self.box_shape_attr = None
        self.hole_shape_attr = None
        self.result_shape_attr = None

        # Statistics
        # 统计信息
        self.generation_count = 0
        self.last_generation_time = 0

    def setup_document_structure(self):
        """Set up the hierarchical OCAF document structure."""
        print("\n--- Setting up OCAF Document Structure ---")
        print("--- 设置OCAF文档结构 ---")

        self.doc.NewCommand()

        # Root label
        # 根标签
        self.root_label = self.doc.Main()
        TDataStd_Name.Set(self.root_label, "ParametricCAD_Root")

        # Parameters branch
        # 参数分支
        self.params_label = self.root_label.FindChild(1, True)
        TDataStd_Name.Set(self.params_label, "Parameters")

        # Geometry branch
        # 几何分支
        self.geometry_label = self.root_label.FindChild(2, True)
        TDataStd_Name.Set(self.geometry_label, "Geometry")

        # Metadata branch
        # 元数据分支
        self.metadata_label = self.root_label.FindChild(3, True)
        TDataStd_Name.Set(self.metadata_label, "Metadata")

        self.doc.CommitCommand()
        print("✓ Document structure created with hierarchical labels")
        print("✓ 创建了分层标签的文档结构")

    def initialize_parameters(self, width=120.0, height=100.0, depth=80.0, hole_radius=20.0):
        """Initialize all parameters with default values."""
        print(f"\n--- Initializing Parameters ---")
        print(f"--- 初始化参数 ---")

        self.doc.NewCommand()

        # Create parameter labels with descriptive names
        # 创建带有描述性名称的参数标签
        width_label = self.params_label.FindChild(1, True)
        height_label = self.params_label.FindChild(2, True)
        depth_label = self.params_label.FindChild(3, True)
        hole_radius_label = self.params_label.FindChild(4, True)

        # Set parameter names
        # 设置参数名称
        TDataStd_Name.Set(width_label, "Width")
        TDataStd_Name.Set(height_label, "Height")
        TDataStd_Name.Set(depth_label, "Depth")
        TDataStd_Name.Set(hole_radius_label, "HoleRadius")

        # Store parameter values using correct OCAF API pattern
        # 使用正确的OCAF API模式存储参数值
        self.width_attr = TDataStd_Real.Set(width_label, width)
        self.height_attr = TDataStd_Real.Set(height_label, height)
        self.depth_attr = TDataStd_Real.Set(depth_label, depth)
        self.hole_radius_attr = TDataStd_Real.Set(hole_radius_label, hole_radius)

        # Add metadata
        # 添加元数据
        version_label = self.metadata_label.FindChild(1, True)
        TDataStd_Name.Set(version_label, "ModelVersion")
        self.model_version_attr = TDataStd_Integer.Set(version_label, 1)

        self.doc.CommitCommand()

        print(f"✓ Parameters initialized:")
        print(f"  Width: {width}, Height: {height}, Depth: {depth}, Hole Radius: {hole_radius}")
        print(f"✓ 参数已初始化：")
        print(f"  宽度: {width}, 高度: {height}, 深度: {depth}, 孔半径: {hole_radius}")

    def get_current_parameters(self):
        """Get current parameter values using OCAF attributes."""
        if not all([self.width_attr, self.height_attr, self.depth_attr, self.hole_radius_attr]):
            raise RuntimeError("Parameters not initialized. Call initialize_parameters() first.")

        return {
            'width': self.width_attr.Get(),
            'height': self.height_attr.Get(),
            'depth': self.depth_attr.Get(),
            'hole_radius': self.hole_radius_attr.Get(),
            'version': self.model_version_attr.Get() if self.model_version_attr else 1
        }

    def update_parameter(self, param_name, value):
        """Update a specific parameter with validation."""
        if value <= 0:
            raise ValueError(f"Parameter {param_name} must be positive, got {value}")

        # Parameter validation
        # 参数验证
        if param_name == 'hole_radius':
            current_params = self.get_current_parameters()
            max_radius = min(current_params['width'], current_params['height']) / 2 - 5
            if value >= max_radius:
                raise ValueError(f"Hole radius {value} too large. Maximum allowed: {max_radius:.1f}")

        self.doc.NewCommand()

        # Update the appropriate parameter
        # 更新相应的参数
        param_map = {
            'width': self.width_attr,
            'height': self.height_attr,
            'depth': self.depth_attr,
            'hole_radius': self.hole_radius_attr
        }

        if param_name not in param_map:
            raise ValueError(f"Unknown parameter: {param_name}")

        param_map[param_name].Set(value)

        # Increment version
        # 增加版本号
        current_version = self.model_version_attr.Get()
        self.model_version_attr.Set(current_version + 1)

        self.doc.CommitCommand()

        print(f"✓ Parameter '{param_name}' updated to {value} (Version: {current_version + 1})")
        print(f"✓ 参数 '{param_name}' 已更新为 {value} (版本: {current_version + 1})")

    def generate_parametric_geometry(self):
        """
        Generate complex parametric geometry based on current parameters.
        基于当前参数生成复杂的参数化几何体。

        This demonstrates the core of parametric CAD:
        这演示了参数化CAD的核心：
        1. Read parameters from OCAF document
           从OCAF文档读取参数
        2. Generate geometry based on parameters
           基于参数生成几何体
        3. Perform complex boolean operations
           执行复杂的布尔运算
        4. Store results back in OCAF
           将结果存储回OCAF
        """
        start_time = time.time()

        print(f"\n--- Generating Parametric Geometry ---")
        print(f"--- 生成参数化几何体 ---")

        # Get current parameters
        # 获取当前参数
        params = self.get_current_parameters()
        W, H, D, R = params['width'], params['height'], params['depth'], params['hole_radius']

        try:
            # Step 1: Create the main box
            # 步骤1：创建主盒子
            print(f"Creating box: {W} × {H} × {D}")
            print(f"创建盒子: {W} × {H} × {D}")
            box = BRepPrimAPI_MakeBox(W, H, D).Shape()

            # Step 2: Create the cylindrical hole
            # 步骤2：创建圆柱孔
            print(f"Creating cylindrical hole: radius={R}, height={D*1.2}")
            print(f"创建圆柱孔: 半径={R}, 高度={D*1.2}")
            hole_center = gp_Pnt(W/2, H/2, -D/10)  # Center position
            hole_axis = gp_Ax2(hole_center, gp_Dir(0, 0, 1))  # Z-axis direction
            cylinder = BRepPrimAPI_MakeCylinder(hole_axis, R, D * 1.2).Shape()

            # Step 3: Perform boolean cut operation
            # 步骤3：执行布尔切除操作
            print("Performing boolean cut operation...")
            print("执行布尔切除操作...")
            cut_operation = BRepAlgoAPI_Cut(box, cylinder)
            cut_operation.Build()

            if not cut_operation.IsDone():
                raise RuntimeError("Boolean cut operation failed")

            result_shape = cut_operation.Shape()

            # Step 4: Store geometry in OCAF using TNaming
            # 步骤4：使用TNaming在OCAF中存储几何体
            self.doc.NewCommand()

            # Store individual components
            # 存储各个组件
            box_label = self.geometry_label.FindChild(1, True)
            hole_label = self.geometry_label.FindChild(2, True)
            result_label = self.geometry_label.FindChild(3, True)

            TDataStd_Name.Set(box_label, "MainBox")
            TDataStd_Name.Set(hole_label, "CylindricalHole")
            TDataStd_Name.Set(result_label, "FinalResult")

            # Use TNaming_Builder to store shapes
            # 使用TNaming_Builder存储形状
            box_builder = TNaming_Builder(box_label)
            box_builder.Generated(box)
            self.box_shape_attr = box_builder.NamedShape()

            hole_builder = TNaming_Builder(hole_label)
            hole_builder.Generated(cylinder)
            self.hole_shape_attr = hole_builder.NamedShape()

            result_builder = TNaming_Builder(result_label)
            result_builder.Generated(result_shape)
            self.result_shape_attr = result_builder.NamedShape()

            self.doc.CommitCommand()

            # Update statistics
            # 更新统计信息
            self.generation_count += 1
            self.last_generation_time = time.time() - start_time

            print(f"✓ Geometry generation completed successfully!")
            print(f"✓ 几何体生成成功完成！")
            print(f"  Generation #{self.generation_count}, Time: {self.last_generation_time:.3f}s")
            print(f"  生成次数 #{self.generation_count}, 时间: {self.last_generation_time:.3f}秒")

            return result_shape

        except Exception as e:
            print(f"✗ Error during geometry generation: {e}")
            print(f"✗ 几何体生成过程中出错: {e}")
            raise

    def get_current_shape(self):
        """Get the current result shape from OCAF."""
        if self.result_shape_attr:
            return self.result_shape_attr.Get()
        return None

    def validate_and_analyze_model(self):
        """
        Comprehensive model validation and analysis.
        综合模型验证和分析。
        """
        print(f"\n--- Model Validation and Analysis ---")
        print(f"--- 模型验证和分析 ---")

        shape = self.get_current_shape()
        if not shape:
            return {"valid": False, "error": "No shape available for validation"}

        try:
            # Calculate volume properties
            # 计算体积属性
            props = GProp_GProps()
            brepgprop.VolumeProperties(shape, props)
            actual_volume = props.Mass()

            # Count solid components
            # 计算实体组件数量
            solid_count = 0
            explorer = TopExp_Explorer(shape, TopAbs_SOLID)
            while explorer.More():
                solid_count += 1
                explorer.Next()

            # Calculate expected volume (box - cylinder)
            # 计算期望体积（盒子 - 圆柱）
            params = self.get_current_parameters()
            box_volume = params['width'] * params['height'] * params['depth']
            hole_volume = math.pi * params['hole_radius']**2 * params['depth']
            expected_volume = box_volume - hole_volume

            volume_error = abs(actual_volume - expected_volume)
            volume_accuracy = (1 - volume_error / expected_volume) * 100

            validation_result = {
                "valid": True,
                "actual_volume": actual_volume,
                "expected_volume": expected_volume,
                "volume_error": volume_error,
                "volume_accuracy": volume_accuracy,
                "solid_count": solid_count,
                "parameters": params,
                "generation_count": self.generation_count,
                "last_generation_time": self.last_generation_time
            }

            print(f"✓ Model validation successful:")
            print(f"  Volume: {actual_volume:.1f} (Expected: {expected_volume:.1f})")
            print(f"  Accuracy: {volume_accuracy:.2f}%")
            print(f"  Solids: {solid_count}")
            print(f"✓ 模型验证成功:")
            print(f"  体积: {actual_volume:.1f} (期望: {expected_volume:.1f})")
            print(f"  精度: {volume_accuracy:.2f}%")
            print(f"  实体数: {solid_count}")

            return validation_result

        except Exception as e:
            error_result = {"valid": False, "error": str(e)}
            print(f"✗ Model validation failed: {e}")
            print(f"✗ 模型验证失败: {e}")
            return error_result

    def print_document_structure(self):
        """Print the complete OCAF document structure."""
        print(f"\n--- OCAF Document Structure ---")
        print(f"--- OCAF文档结构 ---")

        params = self.get_current_parameters()

        print(f"Root: ParametricCAD_Root")
        print(f"├── Parameters/")
        print(f"│   ├── Width: {params['width']}")
        print(f"│   ├── Height: {params['height']}")
        print(f"│   ├── Depth: {params['depth']}")
        print(f"│   └── HoleRadius: {params['hole_radius']}")
        print(f"├── Geometry/")
        print(f"│   ├── MainBox: {self.box_shape_attr is not None}")
        print(f"│   ├── CylindricalHole: {self.hole_shape_attr is not None}")
        print(f"│   └── FinalResult: {self.result_shape_attr is not None}")
        print(f"└── Metadata/")
        print(f"    └── ModelVersion: {params['version']}")

    def run_parametric_demo(self):
        """
        Run a comprehensive demonstration of parametric CAD capabilities.
        运行参数化CAD能力的综合演示。
        """
        print(f"\n{'='*60}")
        print(f"PARAMETRIC CAD DEMONSTRATION")
        print(f"参数化CAD演示")
        print(f"{'='*60}")

        # Test scenarios
        # 测试场景
        test_scenarios = [
            {
                "name": "Default Configuration",
                "name_cn": "默认配置",
                "params": {"width": 120, "height": 100, "depth": 80, "hole_radius": 20}
            },
            {
                "name": "Large Industrial Part",
                "name_cn": "大型工业零件",
                "params": {"width": 200, "height": 150, "depth": 120, "hole_radius": 35}
            },
            {
                "name": "Compact Design",
                "name_cn": "紧凑设计",
                "params": {"width": 80, "height": 60, "depth": 40, "hole_radius": 12}
            },
            {
                "name": "Thin Plate",
                "name_cn": "薄板",
                "params": {"width": 150, "height": 100, "depth": 25, "hole_radius": 18}
            }
        ]

        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario['name']} ({scenario['name_cn']}) ---")

            try:
                # Initialize or update parameters
                # 初始化或更新参数
                if i == 1:
                    self.initialize_parameters(**scenario['params'])
                else:
                    for param_name, value in scenario['params'].items():
                        self.update_parameter(param_name, value)

                # Generate geometry
                # 生成几何体
                self.generate_parametric_geometry()

                # Validate model
                # 验证模型
                validation = self.validate_and_analyze_model()

                if validation["valid"]:
                    print(f"✓ Scenario {i} completed successfully")
                    print(f"✓ 场景 {i} 成功完成")
                else:
                    print(f"✗ Scenario {i} failed: {validation['error']}")
                    print(f"✗ 场景 {i} 失败: {validation['error']}")

            except Exception as e:
                print(f"✗ Error in scenario {i}: {e}")
                print(f"✗ 场景 {i} 出错: {e}")

        # Final summary
        # 最终总结
        print(f"\n{'='*60}")
        print(f"DEMONSTRATION SUMMARY")
        print(f"演示总结")
        print(f"{'='*60}")

        self.print_document_structure()

        final_validation = self.validate_and_analyze_model()
        if final_validation["valid"]:
            print(f"\n✓ All OCAF parametric CAD features demonstrated successfully!")
            print(f"✓ 所有OCAF参数化CAD功能演示成功！")
            print(f"  Total generations: {self.generation_count}")
            print(f"  Last generation time: {self.last_generation_time:.3f}s")
            print(f"  Final volume accuracy: {final_validation['volume_accuracy']:.2f}%")
        else:
            print(f"\n✗ Final validation failed")
            print(f"✗ 最终验证失败")

def main():
    """
    Main function demonstrating Phase 6 OCAF capabilities.
    演示第六阶段OCAF能力的主函数。
    """
    try:
        # Create and run the parametric CAD application
        # 创建并运行参数化CAD应用
        app = ParametricCADApplication()
        app.run_parametric_demo()

        print(f"\n{'='*60}")
        print(f"PHASE 6 OCAF LEARNING OBJECTIVES ACHIEVED!")
        print(f"第六阶段OCAF学习目标达成！")
        print(f"{'='*60}")
        print(f"✓ OCAF Document Structure and Management")
        print(f"✓ Hierarchical Label Organization")
        print(f"✓ Attribute-based Parameter Storage")
        print(f"✓ Parametric Geometry Generation")
        print(f"✓ Real-time Model Updates")
        print(f"✓ Complex Boolean Operations")
        print(f"✓ Model Validation and Error Handling")
        print(f"✓ Professional CAD Application Architecture")

    except Exception as e:
        print(f"\n✗ Application error: {e}")
        print(f"✗ 应用程序错误: {e}")
        raise

if __name__ == "__main__":
    main()
