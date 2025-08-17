# OCC Core 介绍

## 核心模块目录

以下是OCCT核心功能模块的列表。我们已经为这些模块创建了详细的文档和代码示例。点击链接查看详细内容。

- **[gp](./gp/gp.md)**: 几何图元 (Geometric Primitives) - 所有几何计算的基础。
- **[TopoDS](./TopoDS/TopoDS.md)**: 拓扑数据结构 (Topological Data Structure) - 定义形状的“骨架”。
- **[BRepPrimAPI](./BRepPrimAPI/BRepPrimAPI.md)**: 基础实体建模 (Primitives API) - 用于快速创建标准三维实体。
- **[BRepBuilderAPI](./BRepBuilderAPI/BRepBuilderAPI.md)**: 手动构建拓扑 (Builder API) - “自下而上”地构建复杂形状。
- **[BRepAlgoAPI](./BRepAlgoAPI/BRepAlgoAPI.md)**: 布尔运算 (Boolean Operations) - 对实体进行并、交、差运算。
- **[BRepFilletAPI](./BRepFilletAPI/BRepFilletAPI.md)**: 圆角与倒角 (Fillet API) - 为模型的棱边添加平滑过渡。
- **[BRepOffsetAPI](./BRepOffsetAPI/BRepOffsetAPI.md)**: 偏移与中空 (Offset API) - 实现“抽壳”等高级功能。
- **[GeomAPI](./GeomAPI/GeomAPI.md)**: 高级曲线与曲面 (Geometry API) - 从点集创建自由形态的几何。
- **[ShapeFix](./ShapeFix/ShapeFix.md)**: 几何修复 (Shape Fixing) - 分析和修复有缺陷的模型。
- **[STEPControl](./STEPControl/STEPControl.md)**: STEP 文件交互 - 读取和写入工业标准的STEP格式。
- **[BRepMesh](./BRepMesh/BRepMesh.md)**: B-Rep 网格化 (Meshing) - 将精确模型转换为多边形网格。
- **[StlAPI](./StlAPI/StlAPI.md)**: STL 文件交互 - 读写3D打印中最常用的STL格式。
- **[BRepGProp](./BRepGProp/BRepGProp.md)**: 质量属性计算 (Global Properties) - 计算体积、重心、表面积等。
- **[BRepExtrema](./BRepExtrema/BRepExtrema.md)**: 距离查询 (Extrema) - 计算形状之间的最短距离。
- **[AIS](./AIS/AIS.md)**: 可视化与交互 (Application Interactive Services) - 在3D窗口中显示和操作模型。
- **[OCAF](./OCAF/OCAF_1_TDocStd.md)**: OCCT应用框架 (OpenCASCADE Application Framework) - 构建参数化CAD应用的数据基础。

---

## 概述

OCC（Open CASCADE Technology）是一个开源的 CAD/CAM/CAE 几何建模内核，OCC Core 作为其核心组件，为开发几何建模相关的应用程序提供了基础的功能和工具。

## 包含内容

1. **几何数据结构**：包含了多种基本的几何实体，如点、线、面、体等，同时也支持复杂的几何形状表示，如 NURBS（非均匀有理 B 样条）曲线和曲面。
2. **拓扑数据结构**：定义了几何实体之间的拓扑关系，如边、面、体之间的连接和邻接关系，这对于处理复杂的几何模型至关重要。
3. **算法库**：集成了丰富的几何算法，包括几何计算、几何变换、布尔运算、曲面求交等。
4. **可视化模块**：提供了基本的可视化功能，允许用户直观地查看和操作几何模型。

## 主要功能

1. **几何建模**：支持创建、编辑和分析各种几何模型，从简单的二维图形到复杂的三维实体都能处理。
2. **几何计算**：进行各种几何计算，如距离计算、面积和体积计算、曲率分析等。
3. **布尔运算**：实现实体之间的并、交、差等布尔运算，用于组合和修改几何模型。
4. **数据交换**：支持多种常见的 CAD 数据格式导入和导出，如 STEP、IGES、STL 等，方便与其他 CAD 软件进行数据交互。
5. **可视化展示**：可以将几何模型以直观的方式展示出来，支持交互操作，如旋转、缩放、平移等。

## 应用场景

OCC Core 广泛应用于机械设计、汽车制造、航空航天、建筑设计等领域，为开发专业的 CAD/CAM/CAE 软件提供了强大的技术支持。