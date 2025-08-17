# -*- coding: utf-8 -*- 

"""
Phase 4 Summary Example: Analysis and Queries
# 第四阶段汇总示例：分析与查询

This script demonstrates a complete analysis workflow on a given shape:
# 本脚本演示了对一个给定形状的完整分析工作流：

1.  A source STEP file is created, simulating an external model.
    # 1. 创建一个源STEP文件，模拟一个外部模型。
2.  The model is read using `STEPControl_Reader`.
    # 2. 使用 `STEPControl_Reader` 读取该模型。
3.  Its geometric validity is checked using `BRepCheck_Analyzer`.
    # 3. 使用 `BRepCheck_Analyzer` 检查其几何有效性。
4.  Its properties (volume, area, center of mass) are computed using `BRepGProp`.
    # 4. 使用 `BRepGProp` 计算其属性（体积、面积、重心）。
5.  The shape and its center of mass are visualized using `AIS`.
    # 5. 使用 `AIS` 将形状及其重心进行可视化。
"""

import os
import math

# --- Imports ---
# --- 导入 ---
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax2
from OCC.Core.Geom import Geom_Point # Import Geom_Point for AIS visualization
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeVertex
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import AIS_Point

def create_target_step_file(file_path: str):
    """
    Creates the L-bracket from the Phase 2 summary example and saves it as a STEP file.
    # 创建第二阶段汇总示例中的L型支架，并将其另存为STEP文件。
    """
    # Base Plate - More robust, step-by-step creation
    # # 基板 - 更稳健的、分步的创建方式
    p1, p2, p3, p4 = gp_Pnt(0,0,0), gp_Pnt(100,0,0), gp_Pnt(100,80,0), gp_Pnt(0,80,0)
    e1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    e2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    e3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
    e4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()
    base_wire_builder = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)
    base_plate_profile = base_wire_builder.Wire()
    base_plate_face = BRepBuilderAPI_MakeFace(base_plate_profile, True).Face()
    base_plate_solid = BRepPrimAPI_MakePrism(base_plate_face, gp_Vec(0, 0, 15)).Shape()

    # Vertical Plate - More robust, step-by-step creation
    # # 垂直板 - 更稳健的、分步的创建方式
    vp1, vp2, vp3, vp4 = gp_Pnt(0,0,15), gp_Pnt(0,0,100), gp_Pnt(0,80,100), gp_Pnt(0,80,15)
    ve1 = BRepBuilderAPI_MakeEdge(vp1, vp2).Edge()
    ve2 = BRepBuilderAPI_MakeEdge(vp2, vp3).Edge()
    ve3 = BRepBuilderAPI_MakeEdge(vp3, vp4).Edge()
    ve4 = BRepBuilderAPI_MakeEdge(vp4, vp1).Edge()
    vert_wire_builder = BRepBuilderAPI_MakeWire(ve1, ve2, ve3, ve4)
    vert_plate_profile = vert_wire_builder.Wire()
    vert_plate_face = BRepBuilderAPI_MakeFace(vert_plate_profile, True).Face()
    vert_plate_solid = BRepPrimAPI_MakePrism(vert_plate_face, gp_Vec(15, 0, 0)).Shape()

    # Fuse plates
    # # 融合板件
    l_bracket = BRepAlgoAPI_Fuse(base_plate_solid, vert_plate_solid).Shape()

    # Cut hole
    # # 切割孔
    hole_cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(15, 40, 60), gp_Dir(1, 0, 0)), 25, 15).Shape()
    l_bracket = BRepAlgoAPI_Cut(l_bracket, hole_cylinder).Shape()

    # Add fillet
    # # 添加圆角
    mk_fillet = BRepFilletAPI_MakeFillet(l_bracket)
    edge_explorer = TopExp_Explorer(l_bracket, TopAbs_EDGE)
    while edge_explorer.More():
        an_edge = edge_explorer.Current()
        from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
        adaptor = BRepAdaptor_Curve(an_edge)
        p1_fillet, p2_fillet = adaptor.Value(adaptor.FirstParameter()), adaptor.Value(adaptor.LastParameter())
        if math.isclose(p1_fillet.X(), 15) and math.isclose(p2_fillet.X(), 15) and math.isclose(p1_fillet.Z(), 15) and math.isclose(p2_fillet.Z(), 15):
            mk_fillet.Add(10.0, an_edge)
            break
        edge_explorer.Next()
    mk_fillet.Build()
    if mk_fillet.IsDone(): l_bracket = mk_fillet.Shape()
    
    # Write to STEP file
    # # 写入STEP文件
    step_writer = STEPControl_Writer()
    step_writer.Transfer(l_bracket, STEPControl_AsIs)
    status = step_writer.Write(file_path)
    return status == IFSelect_RetDone

def run_analysis(file_path: str, display):
    """
    Runs the full analysis and visualization workflow.
    # 运行完整的分析和可视化工作流。
    """
    # 1. Read the STEP file
    # 1. 读取STEP文件
    print(f"--- Reading STEP file: {file_path} ---")
    # --- 正在读取STEP文件: {file_path} ---
    step_reader = STEPControl_Reader()
    read_status = step_reader.ReadFile(file_path)
    if read_status != IFSelect_RetDone: return
    step_reader.TransferRoots()
    the_shape = step_reader.Shape(1)

    # 2. Check for validity
    # 2. 检查有效性
    print("\n--- Checking shape validity ---")
    # --- 正在检查形状有效性 ---
    analyzer = BRepCheck_Analyzer(the_shape)
    is_valid = analyzer.IsValid()
    print(f"Shape validity status: {'Valid' if is_valid else 'Invalid'}")
    # 形状有效性状态: {'有效' if is_valid else '无效'}
    assert is_valid, "The shape is not valid, analysis aborted."

    # 3. Calculate geometric properties
    # 3. 计算几何属性
    print("\n--- Calculating geometric properties ---")
    # --- 正在计算几何属性 ---
    surf_props = GProp_GProps()
    vol_props = GProp_GProps()
    brepgprop.SurfaceProperties(the_shape, surf_props)
    brepgprop.VolumeProperties(the_shape, vol_props)
    surface_area = surf_props.Mass()
    volume = vol_props.Mass()
    center_of_mass_pnt = vol_props.CentreOfMass()

    # 4. Print the analysis report
    # 4. 打印分析报告
    print("\n--- Analysis Report ---")
    # --- 分析报告 ---
    print(f"  - Surface Area: {surface_area:.2f} mm^2")
    print(f"  - Volume:       {volume:.2f} mm^3")
    print(f"  - Center of Mass: (X={center_of_mass_pnt.X():.2f}, Y={center_of_mass_pnt.Y():.2f}, Z={center_of_mass_pnt.Z():.2f}) mm")

    # 5. Visualize the shape and its center of mass
    # 5. 可视化形状及其重心
    print("\n--- Displaying shape and center of mass ---")
    # --- 正在显示形状及其重心 ---
    display.DisplayShape(the_shape, update=False, color="gold")
    # To display a single point, we can wrap it in a TopoDS_Vertex shape
    # # 要显示一个单独的点，我们可以将其包装在一个 TopoDS_Vertex 形状中
    com_vertex = BRepBuilderAPI_MakeVertex(center_of_mass_pnt).Shape()
    display.DisplayShape(com_vertex, update=True, color="red")
    display.FitAll()

if __name__ == "__main__":
    display, start_display, _, _ = init_display()
    target_file = "analysis_target.step"

    if create_target_step_file(target_file):
        run_analysis(target_file, display)
        start_display()

    # Clean up the created file
    # # 清理创建的文件
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f"\nCleaned up temporary file: {target_file}")
        # 已清理临时文件: {target_file}
