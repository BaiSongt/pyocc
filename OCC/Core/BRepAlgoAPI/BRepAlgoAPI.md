# `BRepAlgoAPI` (Boundary Representation Algorithms API)

`BRepAlgoAPI` 提供了一系列强大的算法，用于对边界表示（B-Rep）的形状执行布尔运算。这是创建复杂模型的关键工具，允许你通过组合、切割和相交基本实体来生成新的、更复杂的形状。

这些操作是大多数CAD软件功能的核心。

## 核心用法

与 `BRepPrimAPI` 类似，`BRepAlgoAPI` 中的类也遵循一个通用的构建器模式：

1.  **实例化算法类**: 选择你需要的布尔运算（如 `Cut`），并使用两个或多个形状作为参数来实例化它。通常，第一个参数是“操作对象”（the object），第二个参数是“工具”（the tool）。
    *   例如: `a_cut_operation = BRepAlgoAPI_Cut(my_box, my_sphere)`

2.  **执行构建**: 调用 `.Build()` 方法来执行复杂的布尔运算计算。

3.  **检查状态**: 调用 `.IsDone()` 确认操作是否成功完成。

4.  **获取结果**: 调用 `.Shape()` 方法来获取运算后生成的新 `TopoDS_Shape`。

## 主要布尔运算类

*   **`BRepAlgoAPI_Fuse` (并集/融合)**: 将两个或多个形状融合成一个单一的形状。重叠的部分会被合并。
    *   `result = Fuse(shape1, shape2)`

*   **`BRepAlgoAPI_Cut` (差集/切割)**: 从第一个形状（对象）中减去第二个形状（工具）。
    *   `result = Cut(object_shape, tool_shape)`

*   **`BRepAlgoAPI_Common` (交集)**: 计算两个形状重叠的部分，生成它们共同拥有的体积。
    *   `result = Common(shape1, shape2)`

*   **`BRepAlgoAPI_Section` (截面)**: 计算两个形状的交集，但结果不是一个实体，而是交线（`TopoDS_Edge` 或 `TopoDS_Wire`）或交点（`TopoDS_Vertex`）。这对于分析和创建截面非常有用。

*   **`BRepAlgoAPI_Splitter`**: 使用一个“工具”形状将一个“对象”形状分割成多个部分。

## 注意事项

- **计算成本**: 布尔运算是计算密集型操作，尤其是在处理复杂曲面时。操作可能会花费较长时间，也可能因为几何上的不稳定而失败。
- **几何有效性**: 输入的形状必须是“有效”的（例如，闭合的实体）。可以使用 `BRepCheck_Analyzer` 工具来检查形状的有效性。

在接下来的示例中，我们将演示一个经典的布尔运算：从一个长方体中切割掉一个球体。
