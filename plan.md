# OCCT Python 学习计划 (Phased)

本项目旨在为 OCCT Python 库创建一个结构化、阶段性的学习资源。整个学习过程被划分为多个阶段，每个阶段都包含一系列核心模块的学习，并以一个总结性的示例项目结束。

---

## 第一阶段：核心概念入门

**目标**: 掌握OCCT进行基础建模和可视化的完整工作流程。

**状态**: <span style="color:green">**已完成**</span>

### 学习模块:

1.  **`gp` (Geometric Primitives)**: 学习点、向量、变换等几何基础。
2.  **`TopoDS` (Topological Data Structure)**: 理解顶点、边、面、实体的拓扑结构。
3.  **`BRepPrimAPI` (Primitives API)**: 掌握创建长方体、球、圆柱等基本几何体的方法。
4.  **`BRepAlgoAPI` (Boolean Operations)**: 学习对实体进行并、交、差等布尔运算。
5.  **`AIS` & `V3d` (Visualization)**: 学会将创建的几何模型在窗口中进行可视化展示。

### 阶段汇总示例:

- **`examples/phase_1_core_concepts.py`**: 一个完整的脚本，用于创建一个带球形孔的盒子，并在3D视图中显示它。

---

## 第二阶段：进阶边界表示建模

**目标**: 学习使用更灵活的工具来构建复杂的、非标准的几何形状，并添加常见的机械特征。

**状态**: <span style="color:orange">**待办**</span>

### 学习模块:

- **`BRepBuilderAPI`**: 学习通过点、线、面等底层拓扑元素，逐步构建起复杂的线框、表面和实体。
- **`BRepFilletAPI`**: 学习为模型的边添加圆角和倒角。
- **`BRepOffsetAPI`**: 学习抽壳（创建中空物体）、创建厚度、拔模等高级特征。
- **`BRepTools`**: 学习使用 `WireExplorer` 等工具来遍历和分析复杂的拓扑结构。

### 阶段汇总示例:

- **`examples/phase_2_advanced_modeling.py` (待创建)**: 创建一个带有圆角、通孔和中空结构的机械支架模型。

---

## 第三阶段：数据交换与网格化

**目标**: 学习如何将OCCT模型与标准的CAD文件格式（如STEP, IGES）进行交互，并学习如何生成用于3D打印或仿真分析的网格数据（如STL）。

**状态**: <span style="color:orange">**待办**</span>

### 学习模块:

- **`STEPControl`**: 学习读取和写入 `*.step` 或 `*.stp` 文件。
- **`IGESControl`**: 学习读取和写入 `*.iges` 或 `*.igs` 文件。
- **`BRepMesh`**: 学习配置参数，将B-Rep实体转换为三角网格。
- **`StlAPI`**: 学习直接读写 `*.stl` 网格文件。

### 阶段汇总示例:

- **`examples/phase_3_interoperability.py` (待创建)**: 读取一个外部的STEP文件，对其进行简化或修改，然后将其网格化并另存为STL文件。

---

## 第四阶段：分析与查询

**目标**: 学习如何从几何模型中提取有用的信息和数据。

**状态**: <span style="color:orange">**待办**</span>

### 学习模块:

- **`BRepGProp`**: 计算形状的全局属性，如体积、表面积、质心、惯性矩等。
- **`BRepExtrema`**: 计算两个形状之间或一个形状内部的最小/最大距离。
- **`BRepCheck`**: 对形状进行有效性分析，检查是否存在几何或拓扑错误。

### 阶段汇总示例:

- **`examples/phase_4_analysis.py` (待创建)**: 加载一个复杂模型，输出一份包含其体积、重心、表面积和有效性检查结果的分析报告。