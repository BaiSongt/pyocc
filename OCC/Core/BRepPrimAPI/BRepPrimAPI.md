# `BRepPrimAPI` (Boundary Representation Primitives API)

`BRepPrimAPI` 是一个高级API，专门用于快速、方便地创建标准的、参数化的三维几何基本体（Primitives）。如果你需要创建一个长方体、球体、圆柱体、圆锥体或圆环，这通常是你的首选工具。

这个API将底层的几何创建（`gp`）和拓扑构建（`TopoDS`）封装了起来，提供了一个非常易于使用的接口。

## 核心用法

`BRepPrimAPI` 中几乎所有的类都遵循一个共同的设计模式：

1.  **实例化 `Make...` 类**: 根据你想要创建的物体，选择对应的 `BRepPrimAPI_Make...` 类并实例化。构造函数通常需要一些几何参数，比如点、向量、半径、高度等。
    *   例如: `make_box = BRepPrimAPI_MakeBox(p1, p2)`

2.  **检查构建状态 (可选但推荐)**: 可以调用 `.IsDone()` 方法来检查构建是否成功。

3.  **获取结果**: 调用 `.Shape()` 方法来获取构建完成的 `TopoDS_Shape`。根据你创建的物体，这个Shape通常是一个 `TopoDS_Solid`。
    *   例如: `my_solid_box = make_box.Shape()`

## 主要类

以下是 `BRepPrimAPI` 中最常用的一些“制造”类：

*   **`BRepPrimAPI_MakeBox`**: 创建一个长方体。可以通过两个对角点 `gp_Pnt` 来定义，或者通过一个点和三个方向的长度来定义。

*   **`BRepPrimAPI_MakeSphere`**: 创建一个球体。通常需要一个中心点 `gp_Pnt` 和一个半径值。

*   **`BRepPrimAPI_MakeCylinder`**: 创建一个圆柱体。通常需要一个半径、一个高度，以及一个定义其位置和方向的坐标系 `gp_Ax2`。

*   **`BRepPrimAPI_MakeCone`**: 创建一个圆锥体。通常需要两个半径（底部和顶部，顶部半径为0即是圆锥尖）、一个高度和一个坐标系 `gp_Ax2`。

*   **`BRepPrimAPI_MakeTorus`**: 创建一个圆环体。需要一个大半径（环中心到管中心的距离）和一个小半径（管的半径），以及一个坐标系 `gp_Ax2`。

*   **`BRepPrimAPI_MakePrism`**: 通过拉伸一个基础形状（如一个面或线框）来创建一个棱柱。

*   **`BRepPrimAPI_MakeRevol`**: 通过旋转一个基础形状来创建一个旋转体。

在接下来的示例中，我们将演示如何使用 `BRepPrimAPI_MakeBox` 创建一个长方体，并验证生成的 `TopoDS_Shape`。
