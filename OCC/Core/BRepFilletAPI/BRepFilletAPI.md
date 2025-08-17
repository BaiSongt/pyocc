# `BRepFilletAPI` (Boundary Representation Fillet API)

`BRepFilletAPI` 是一个高级API，专门用于在形状的棱边上创建圆角（Fillets/Rounds）和倒角（Chamfers）。这些是在机械设计和产品设计中极其常见的特征，不仅为了美观，也为了分散应力、提高安全性。

这个API封装了复杂的底层几何计算，使得添加这些平滑过渡特征变得相对简单。

## 核心用法

使用 `BRepFilletAPI` 的基本流程如下：

1.  **实例化 `Make...` 类**: 根据你已有的形状（通常是一个 `TopoDS_Solid`），实例化 `BRepFilletAPI_MakeFillet` 或 `BRepFilletAPI_MakeChamfer`。
    *   `mk_fillet = BRepFilletAPI_MakeFillet(my_solid_shape)`

2.  **选择边并添加特征**: 遍历你的形状，找到你想要应用特征的 `TopoDS_Edge`，然后调用 `.Add()` 方法将其添加到构建器中。
    *   `mk_fillet.Add(radius, an_edge)`: 为指定的边 `an_edge` 添加一个半径为 `radius` 的圆角。
    *   你可以对不同的边调用多次 `.Add()`，甚至可以为不同的边设置不同的半径。

3.  **执行构建**: 调用 `.Build()` 方法来执行圆角/倒角算法。

4.  **检查状态**: 调用 `.IsDone()` 确认操作是否成功完成。

5.  **获取结果**: 调用 `.Shape()` 方法来获取添加了新特征后的 `TopoDS_Shape`。

## 主要类

*   **`BRepFilletAPI_MakeFillet`**: 用于在一条或多条棱边上创建圆角。你可以为每条边指定一个恒定的半径。

*   **`BRepFilletAPI_MakeChamfer`**: 用于在一条或多条棱边上创建倒角。你可以通过指定一个或两个距离来定义倒角的大小。

*   **`BRepFilletAPI_MakeFillet2d`**: 这是一个2D版本，用于在一个平坦的面（`TopoDS_Face`）的顶点处创建圆角，常用于处理2D轮廓。

## 注意事项

- **边的选择**: 如何准确地选择出你想要操作的边，是使用此API的关键。通常需要使用 `TopExp_Explorer` 遍历所有边，然后根据边的位置、方向或其他几何属性来筛选出目标边。
- **半径限制**: 圆角半径不是任意的。如果半径过大，可能会导致几何计算失败（例如，不同边的圆角在转角处发生冲突）。如果构建失败，尝试减小半径是一个常见的调试方法。

在接下来的示例中，我们将创建一个长方体，并为它的所有上边缘添加圆角。
