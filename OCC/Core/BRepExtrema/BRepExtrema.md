# `BRepExtrema` (Boundary Representation Extrema)

`BRepExtrema` 是一个用于在B-Rep形状之间或形状内部寻找极值距离（Extrema）的工具包。它最核心的功能是计算两个不相交物体之间的最短距离。

这个功能在许多高级应用中都至关重要：

- **碰撞检测 (Collision Detection)**: 如果两个物体之间的最短距离为零或负数，则意味着它们发生了碰撞或干涉。
- **装配分析 (Assembly Analysis)**: 检查零件之间的间隙是否符合设计要求。
- **机器人路径规划**: 确保运动的物体（如机械臂）与环境中的障碍物保持安全距离。

## 核心用法

`BRepExtrema` 的使用非常直接，主要围绕 `BRepExtrema_DistShapeShape` 类展开：

1.  **准备两个形状**: 首先，你需要两个你想要测量距离的 `TopoDS_Shape`。

2.  **实例化 `DistShapeShape`**: `dist_calculator = BRepExtrema_DistShapeShape(shape1, shape2)`
    *   在 `pythonocc-core` 中，这个类的构造函数会直接触发距离计算。

3.  **检查状态**: 调用 `.IsDone()` 确认计算是否成功完成。

4.  **获取结果**: 如果计算成功，可以通过该对象的一系列方法获取详细结果：
    *   `distance = dist_calculator.Value()`: 获取计算出的最短距离值。
    *   `number_of_solutions = dist_calculator.NbSolution()`: 最短距离可能存在于多对点之间，此方法返回解的数量。
    *   `point1 = dist_calculator.PointOnShape1(i)`: 获取第 `i` 个解在第一个形状上的点，返回一个 `gp_Pnt`。
    *   `point2 = dist_calculator.PointOnShape2(i)`: 获取第 `i` 个解在第二个形状上的点。

## 主要类

*   **`BRepExtrema_DistShapeShape`**: 计算两个B-Rep形状之间最短距离的核心工具。
*   **`BRepExtrema_ExtPC`**: 计算一个点和一条曲线之间的最短距离。
*   **`BRepExtrema_ExtPF`**: 计算一个点和一个曲面之间的最短距离。
*   **`BRepExtrema_ExtCC`**: 计算两条曲线之间的最短距离。
*   **`BRepExtrema_ExtCF`**: 计算一条曲线和一个曲面之间的最短距离。

## 注意事项

- **计算成本**: 这是一个相对耗时的计算，特别是对于复杂曲面。应避免在需要实时响应的循环中频繁调用。
- **结果解读**: `DistShapeShape` 找到的是几何体表面之间的最短距离。如果两个物体相交，最短距离将为0。

在接下来的示例中，我们将创建两个不相交的球体，并使用 `BRepExtrema_DistShapeShape` 来精确计算它们表面之间的最短距离。
