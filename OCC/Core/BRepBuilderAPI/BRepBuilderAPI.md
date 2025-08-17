# `BRepBuilderAPI` (Boundary Representation Builder API)

`BRepBuilderAPI` 是一套核心的建模API，它提供了“自下而上”构建拓扑形状的能力。与 `BRepPrimAPI` 直接创建完整的基本体（如长方体）不同，`BRepBuilderAPI` 允许你从最基础的元素（点、边）开始，像搭积木一样，一步步地构建出更复杂的拓扑结构（线框、面、壳、实体）。

这种方法提供了极大的灵活性，是创建任何非标准、自定义形状的基础。

## 核心用法

`BRepBuilderAPI` 中的类通常遵循“收集-构建”的设计模式：

1.  **实例化 `Make...` 类**: 根据你想要创建的拓扑等级，选择对应的 `BRepBuilderAPI_Make...` 类并实例化。
    *   例如: `make_wire = BRepBuilderAPI_MakeWire()`

2.  **添加子元素**: 调用 `.Add()` 方法，将构建所需的低一级拓扑元素添加进来。
    *   例如: `make_wire.Add(my_edge1)`
    *   可以连续添加多个，`BRepBuilderAPI` 会尝试将它们正确地连接起来。

3.  **执行构建**: 调用 `.Build()` 方法来执行构建算法。

4.  **检查状态**: 调用 `.IsDone()` 确认操作是否成功完成。

5.  **获取结果**: 根据你实例化的类，调用对应的 `.Wire()` / `.Face()` / `.Solid()` 等方法来获取构建好的 `TopoDS_Shape`。

## 主要类

*   **`BRepBuilderAPI_MakeVertex`**: 在一个 `gp_Pnt` 上创建一个 `TopoDS_Vertex`。

*   **`BRepBuilderAPI_MakeEdge`**: 通过多种方式创建 `TopoDS_Edge`，例如：
    *   通过两个 `gp_Pnt` (创建直线边)。
    *   通过一个 `Geom_Curve` (如 `Geom_Circle`, `Geom_BSplineCurve`)。

*   **`BRepBuilderAPI_MakeWire`**: 将一系列的 `TopoDS_Edge` 构建成一个 `TopoDS_Wire`。

*   **`BRepBuilderAPI_MakeFace`**: 通过一个闭合的 `TopoDS_Wire` 创建一个 `TopoDS_Face`。也可以通过一个 `Geom_Surface` 和边界线框来创建。

*   **`BRepBuilderAPI_MakeShell`**: 将一系列的 `TopoDS_Face` 缝合成一个 `TopoDS_Shell`。

*   **`BRepBuilderAPI_MakeSolid`**: 通过一个或多个闭合的 `TopoDS_Shell` 创建一个 `TopoDS_Solid`。

*   **`BRepBuilderAPI_Transform`**: 对一个 `TopoDS_Shape` 应用一个 `gp_Trsf` 变换，生成一个新的、变换后的形状。

*   **`BRepBuilderAPI_Copy`**: 创建一个形状的副本，可以选择是否复制其几何体。

在接下来的示例中，我们将演示这个“自下而上”的完整流程：点 -> 边 -> 线框 -> 面。
