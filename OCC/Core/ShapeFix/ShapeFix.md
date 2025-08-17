# `ShapeFix` (Shape Fixing)

`ShapeFix` 是OCCT中一个至关重要的“急救包”，它提供了一系列工具，用于分析和修复B-Rep模型中常见的几何与拓扑缺陷。当你处理从其他CAD系统导入的模型（尤其是通过STEP或IGES格式），或者在复杂建模操作后遇到问题时，`ShapeFix` 是你最有力的帮手。

## 常见几何问题

`ShapeFix` 可以处理多种问题，例如：

- **缝隙 (Gaps)**: 相邻的边或面之间存在微小的间隙，导致线框或壳不闭合。
- **方向错误 (Orientation)**: 面的法向不一致（有些朝外，有些朝内），或者线框中的边方向混乱。
- **退化几何 (Degenerated Geometry)**: 出现长度为零的边或面积为零的面。
- **自交 (Self-intersection)**: 形状的某些部分与自身发生了交叉。

## 核心用法

`ShapeFix` 模块包含多个针对不同拓扑层级的修复工具，但通常有一个高级的、统一的入口。

1.  **准备有问题的形状**: 首先，你需要一个可能存在问题的 `TopoDS_Shape`。

2.  **实例化修复器**: 根据问题的类型，选择合适的修复器。`ShapeFix_Shape` 是一个通用的高级修复器，它会自动调用其他低级修复器。
    *   `fixer = ShapeFix_Shape(my_problematic_shape)`

3.  **执行修复**: 调用 `.Perform()` 方法来启动分析和修复算法。
    *   `fixer.Perform()`

4.  **检查状态**: 调用 `.Status()` 方法，可以检查修复操作的结果（例如，`ShapeExtend_DONE1` 表示成功修复了某些问题）。

5.  **获取结果**: 调用 `.Shape()` 方法来获取修复后的新形状。
    *   `fixed_shape = fixer.Shape()`

## 主要类

*   **`ShapeFix_Shape`**: 一个“全能型”的修复工具，它会按顺序执行多种修复操作，尝试解决一个形状上可能存在的各种问题。

*   **`ShapeFix_Wire`**: 专门用于修复 `TopoDS_Wire`。例如，它可以连接断开的边，修正边的顺序，并使其闭合。

*   **`ShapeFix_Face`**: 修复 `TopoDS_Face` 的问题，例如重建面的内外边界。

*   **`ShapeFix_Shell`**: 修复由多个面组成的 `TopoDS_Shell`，例如修正面的方向使其一致朝外。

*   **`ShapeFix_Solid`**: 尝试从一个或多个壳（Shells）构建一个有效的实体（Solid），即使这些壳存在一些缺陷。

在接下来的示例中，我们将故意创建一个“有缺陷”的形状（一个不闭合的、由五个面组成的盒子），然后演示如何使用 `ShapeFix_Solid` 将其自动修复为一个完整、有效的实体。
