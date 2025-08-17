# `TopoDS` (Topological Data Structure)

如果说 `gp` 包是OCCT的“数学骨架”，那么 `TopoDS` 就是OCCT的“结构骨架”。它定义了一个模型是如何由各种基本的几何元素组织和连接起来的，但它本身并不关心这些元素的具体几何形状（例如一条边是直线还是曲线）。

`TopoDS` 的核心是 `TopoDS_Shape` 类，它是所有拓扑对象的基类。

## 核心概念：拓扑层级

OCCT使用一个清晰的层级来描述一个复杂的3D模型，从最简单的顶点到最复杂的组合体。这个层级关系如下：

1.  **`TopoDS_Vertex` (顶点)**: 空间中的一个点，是拓扑结构的最基本元素。它由一个 `gp_Pnt` 来定义其几何位置。

2.  **`TopoDS_Edge` (边)**: 连接两个或多个顶点的一条曲线。它的几何形状由一条 `Geom_Curve` (如 `Geom_Line`, `Geom_Circle`) 定义。

3.  **`TopoDS_Wire` (线框)**: 一系列首尾相连的边的集合。如果线框是闭合的，它可以用来定义一个面的边界。

4.  **`TopoDS_Face` (面)**: 由一个或多个闭合的线框所界定的一块曲面。它的几何形状由一个 `Geom_Surface` (如 `Geom_Plane`, `Geom_CylindricalSurface`) 定义。

5.  **`TopoDS_Shell` (壳)**: 一系列连接在一起的面的集合。如果壳是闭合的，它可以定义一个实体的边界。

6.  **`TopoDS_Solid` (实体)**: 由一个或多个闭合的壳所界定的三维空间区域。这是我们通常理解的“三维模型”。

7.  **`TopoDS_CompSolid` (复合实体)**: 由多个实体连接而成的复合体。

8.  **`TopoDS_Compound` (组合)**: 可以包含任何类型拓扑形状的通用组合体。

## 重要工具

*   **`TopoDS` 工具类**: `TopoDS` 包本身提供了一些工具函数，例如 `TopoDS.Vertex(aShape)`，用于将一个通用的 `TopoDS_Shape` 安全地转换为一个 `TopoDS_Vertex`。如果转换失败，它会抛出异常。这种类型转换在遍历拓扑结构时非常常用。

*   **`TopExp_Explorer`**: 这是遍历拓扑结构的主要工具。你可以用它来寻找一个形状下的所有子形状，例如，寻找一个面(Face)下的所有边(Edge)，或者一个边(Edge)下的所有顶点(Vertex)。

*   **`BRepBuilderAPI`**: `TopoDS` 只定义了“结构”，而没有提供直接创建这些结构的方法。我们通常使用 `BRepBuilderAPI` 包中的类（如 `BRepBuilderAPI_MakeEdge`, `BRepBuilderAPI_MakeFace`）来实际构建这些拓扑形状。我们将在下一个学习步骤中详细介绍它。

在接下来的示例中，我们将演示如何构建一个简单的形状，并使用 `TopExp_Explorer` 来遍历它的拓扑结构。
