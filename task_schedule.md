# OCCT Python 学习库 - 详细任务安排表 (入门计划)

本文档为 OCCT Python 学习库项目的详细任务分解，用于指导后续阶段的开发工作。每个任务都包含需要学习的核心类和示例代码的实现目标。

---

## 第二阶段：进阶边界表示建模

**目标**: 掌握使用更灵活的工具来构建复杂的、非标准的几何形状，并添加常见的机械特征。

### 任务 2.1: `BRepBuilderAPI` - 手动构建拓扑

- **目标**: 理解如何不依赖基本体，从点、线、面等基础元素手动构建复杂的形状。
- **核心类**: 
  - `BRepBuilderAPI_MakeEdge`: 从几何曲线（如 `Geom_Line`, `Geom_Circle`）创建边。
  - `BRepBuilderAPI_MakeWire`: 将多条边连接成一条线框。
  - `BRepBuilderAPI_MakeFace`: 从一个闭合的线框创建一个面。
  - `BRepBuilderAPI_MakeShell`: 将多个面缝合成一个壳。
  - `BRepBuilderAPI_MakeSolid`: 从一个闭合的壳创建一个实体。
- **示例焦点**: 演示如何通过四个顶点创建四条边，然后将它们合成为一个线框，并最终从这个线框生成一个面（一个矩形面）。

### 任务 2.2: `BRepFilletAPI` - 创建圆角与倒角

- **目标**: 学习为模型的棱边添加平滑过渡，这是机械设计中最常见的操作之一。
- **核心类**:
  - `BRepFilletAPI_MakeFillet`: 在3D实体的边上创建半径恒定的圆角。
  - `BRepFilletAPI_MakeChamfer`: 在3D实体的边上创建倒角。
- **示例焦点**: 创建一个长方体，然后选取它的一条或多条边，为它们应用指定半径的圆角。

### 任务 2.3: `BRepOffsetAPI` - 创建偏移与中空特征

- **目标**: 学习创建具有厚度的中空物体，或对形状进行整体偏移。
- **核心类**:
  - `BRepOffsetAPI_MakeThickSolid`: 将一个实体（如盒子）变成一个中空的、有壁厚的物体。
  - `BRepOffsetAPI_MakeOffsetShape`: 对一个形状（如一个面）进行整体偏移。
  - `BRepOffsetAPI_DraftAngle`: 创建拔模特征。
- **示例焦点**: 创建一个实体，然后使用 `MakeThickSolid` 将其“掏空”，生成一个开口的盒子或一个完全封闭的中空容器。

### 阶段汇总示例 (任务 2.4)

- **目标**: 综合运用本阶段所有技术，创建一个相对完整的机械零件。
- **示例焦点 (`examples/phase_2_advanced_modeling.py`)**: 
  1. 使用 `BRepBuilderAPI` 创建一个矩形基座（面）。
  2. 使用 `BRepPrimAPI` 的 `MakePrism` 将其拉伸成一个实体。
  3. 使用 `BRepAlgoAPI_Cut` 在基座上打出几个通孔。
  4. 使用 `BRepFilletAPI_MakeFillet` 为模型的多个棱边添加圆角。
  5. 使用 `BRepOffsetAPI_MakeThickSolid` 对其进行抽壳处理。
  6. 最后，使用 `AIS` 将这个复杂的零件进行可视化。

---

## 第三阶段：数据交换与网格化

**目标**: 学习如何将OCCT模型与标准的CAD文件格式进行交互，并生成用于3D打印或仿真的网格数据。

### 任务 3.1: `STEPControl` - STEP 文件交互

- **目标**: 掌握工业标准的STEP格式的导入和导出。
- **核心类**:
  - `STEPControl_Reader`: 读取 `*.step` 或 `*.stp` 文件。
  - `STEPControl_Writer`: 将 `TopoDS_Shape` 写入 `*.step` 文件。
  - `STEPControl_StepModelType`: 定义写入STEP文件时遵循的协议（如 `AP203`, `AP214`）。
- **示例焦点**: 编写一个脚本，读取一个STEP文件，统计其中包含的实体数量，然后将其中的第一个实体重新导出为一个新的STEP文件。

### 任务 3.2: `BRepMesh` - B-Rep 网格化

- **目标**: 学习将精确的B-Rep几何模型转换为近似的三角网格模型。
- **核心类**:
  - `BRepMesh_IncrementalMesh`: 这是执行网格化的核心算法类。
- **示例焦点**: 创建一个精确的球体（`BRepPrimAPI_MakeSphere`），然后使用 `BRepMesh_IncrementalMesh` 并设置一个线性挠度（linear deflection）参数，将其转换为三角网格，并打印出生成的节点和三角形数量。

### 任务 3.3: `StlAPI` - STL 文件交互

- **目标**: 掌握对最常见的3D打印格式STL文件的读写。
- **核心类**:
  - `StlAPI_Writer`: 将一个网格化的形状写入 `*.stl` 文件。
  - `StlAPI_Reader`: 从 `*.stl` 文件中读取网格数据。
- **示例焦点**: 承接上一个任务，将 `BRepMesh` 生成的三角网格通过 `StlAPI_Writer` 保存为一个STL文件。

### 阶段汇总示例 (任务 3.4)

- **目标**: 整合本阶段的数据转换与处理能力。
- **示例焦点 (`examples/phase_3_interoperability.py`)**: 
  1. 使用 `STEPControl_Reader` 读取一个包含多个零件的复杂装配体STEP文件。
  2. 提示用户选择其中一个零件。
  3. 对选中的零件运行 `BRepMesh` 算法，生成高质量的三角网格。
  4. 将生成的网格写入STL文件，并同时在 `AIS` 视图中显示原始B-Rep模型和生成的网格模型，以供对比。

---

## 第四阶段：分析与查询

**目标**: 学习如何从几何模型中提取有用的信息和数据，进行测量和验证。

### 任务 4.1: `BRepGProp` - 质量属性计算

- **目标**: 计算实体的体积、重心、惯性矩等物理属性。
- **核心类**:
  - `GProp_GProps`: 用于存储计算结果的属性容器。
  - `BRepGProp_System`: 用于执行计算的核心类。
- **示例焦点**: 创建一个组合形状（例如，一个盒子和一个圆柱的并集），然后计算这个组合形状的总质量、重心位置和关于主轴的惯性矩。

### 任务 4.2: `BRepExtrema` - 距离查询

- **目标**: 计算点、线、面或实体之间的最小或最大距离。
- **核心类**:
  - `BRepExtrema_DistShapeShape`: 计算两个形状之间最短距离的核心工具。
- **示例焦点**: 创建两个不相交的球体，然后计算并打印出它们表面之间的最短距离，以及在每个球体上对应的最近点坐标。

### 阶段汇总示例 (任务 4.3)

- **目标**: 综合运用本阶段的分析能力，对一个模型进行全面的“体检”。
- **示例焦点 (`examples/phase_4_analysis.py`)**: 
  1. 读取一个外部的STEP或IGES文件。
  2. 使用 `BRepCheck_Analyzer` 对其进行几何有效性检查，并报告任何错误（如开缝、自交等）。
  3. 如果形状有效，则使用 `BRepGProp` 计算其详细的质量属性并打印成格式化的报告。
  4. 在 `AIS` 视图中显示该模型，并在其重心位置创建一个 `AIS_Point` 进行标记。
