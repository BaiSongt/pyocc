# `BRepGProp` (Boundary Representation Global Properties)

`BRepGProp` 是一个非常重要的工具包，用于计算B-Rep形状的各种几何（或称“质量”）属性。当你需要知道一个零件的体积、重量、重心、表面积或转动惯量时，这个模块就是你的首选。

这些计算对于工程分析、物理仿真、成本估算和包装设计等应用至关重要。

## 核心用法

`BRepGProp` 的使用模式通常是“计算器”模式：

1.  **准备B-Rep形状**: 首先，你需要一个你想要分析的 `TopoDS_Shape`。

2.  **创建属性容器**: 实例化一个 `GProp_GProps` 对象。这个对象就像一个空的“报告单”，用于接收和存储计算结果。
    *   `properties = GProp_GProps()`

3.  **调用计算函数**: `BRepGProp` 包提供了多个静态函数，用于执行不同类型的属性计算。你需要将你的形状和刚刚创建的属性容器作为参数传给这些函数。
    *   `BRepGProp.VolumeProperties(my_solid, properties)`: 计算体积相关的属性（体积、重心、惯性矩）。这需要输入一个实体（`TopoDS_Solid`）。
    *   `BRepGProp.SurfaceProperties(my_shape, properties)`: 计算表面积相关的属性（表面积、表面重心）。可以输入任何形状。

4.  **获取结果**: 计算函数执行后，`properties` 对象会被填充上结果。你可以通过调用它的一系列方法来获取具体的数值。
    *   `volume = properties.Mass()`: 获取体积（在密度为1的情况下，质量即体积）。
    *   `center_of_mass = properties.CentreOfMass()`: 获取重心，返回一个 `gp_Pnt`。
    *   `inertia_matrix = properties.MatrixOfInertia()`: 获取惯性矩阵。

## 主要类与函数

*   **`GProp_GProps`**: 属性容器类，用于存储计算结果。它本身不执行计算。
*   **`BRepGProp`**: 包含执行计算的静态方法的工具包。
    *   `BRepGProp.VolumeProperties(...)`: 计算体积属性。
    *   `BRepGProp.SurfaceProperties(...)`: 计算表面积属性。

## 注意事项

- **输入的形状**: `VolumeProperties` 必须作用于一个或多个闭合的实体（`TopoDS_Solid`）上，否则计算出的体积没有意义。而 `SurfaceProperties` 可以作用于任何形状（如一个面或一个壳）。
- **密度**: `BRepGProp` 计算的是纯几何属性。例如，`.Mass()` 方法返回的是几何体积。如果你需要计算真实的物理质量，你需要将这个结果乘以材料的密度。

在接下来的示例中，我们将创建一个组合形状，并使用 `BRepGProp` 来计算它的体积、表面积和重心位置。
