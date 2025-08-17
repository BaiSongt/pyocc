# `GeomAPI` (Geometry Application Programming Interface)

`GeomAPI` 是一个高级的、面向算法的API，用于从一组几何约束（最常见的是点集）创建纯粹的几何实体 (`Geom_Curve`, `Geom_Surface`)。

它与 `BRepBuilderAPI` 的核心区别在于：

- **`BRepBuilderAPI`** 创建的是**拓扑形状** (`TopoDS_Shape`)，这些形状“包含”几何定义。它的产出是 `TopoDS_Edge`, `TopoDS_Face` 等。
- **`GeomAPI`** 创建的是**纯粹的几何** (`Geom_Object`)，它们是形状的数学描述，不包含拓扑信息（如边界、顶点等）。它的产出是 `Geom_Curve`, `Geom_Surface` 等。

通常，`GeomAPI` 用于创建复杂的曲线和曲面，然后这些几何体会被用在 `BRepBuilderAPI` 中，来构建最终的拓扑形状。

## 核心用法

`GeomAPI` 的使用模式通常是“一步构建”：

1.  **准备输入数据**: 根据你要使用的算法，准备好输入的几何约束。例如，对于 `GeomAPI_PointsToBSplineSurface`，你需要准备一个二维的点阵。

2.  **实例化算法类**: `builder = GeomAPI_PointsToBSplineSurface(points_array, ...)`
    *   算法通常在构造函数中直接执行。

3.  **检查状态 (可选)**: 调用 `.IsDone()` 确认计算是否成功。

4.  **获取结果**: 调用 `.Curve()` 或 `.Surface()` 方法来获取构建好的 `Geom_BSplineCurve` 或 `Geom_BSplineSurface` 对象。

## 主要类

*   **`GeomAPI_PointsToBSpline`**: 通过一系列点（插值或逼近）来创建一个B样条曲线。

*   **`GeomAPI_PointsToBSplineSurface`**: 通过一个二维的点阵（插值或逼近）来创建一个B样条曲面。这是创建自由形态曲面的核心工具。

*   **`GeomAPI_Interpolate`**: 创建一条精确经过所有给定点的插值B样条曲线。

*   **`GeomAPI_ProjectPointOnCurve`**: 将一个点投影到一条曲线上，寻找最近点。

*   **`GeomAPI_ProjectPointOnSurf`**: 将一个点投影到一个曲面上，寻找最近点。

## 注意事项

- **数据结构**: 很多 `GeomAPI` 类需要OCCT特定的数组类型作为输入，例如 `TColgp_HArray1OfPnt` (一维点数组) 或 `TColgp_HArray2OfPnt` (二维点数组)。你需要先将Python列表中的 `gp_Pnt` 填入这些OCCT的数组结构中。

在接下来的示例中，我们将演示如何创建一个二维点阵，并使用 `GeomAPI_PointsToBSplineSurface` 生成一个光滑的B样条曲面，最后将这个几何曲面转换为一个可显示的面。 
