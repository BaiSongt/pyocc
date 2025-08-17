# `StlAPI` (STL API)

`STL` (Standard Tessellation Language or STereoLithography) 是一种非常简单、被广泛使用的三维文件格式，尤其是在3D打印领域。它通过一系列的三角小平面（facets）来描述一个三维物体的表面，是连接数字模型和物理样品的关键桥梁。

`StlAPI` 模块提供了在OCCT中直接读取和写入STL文件的工具。

## STL文件格式特点

- **简单**: 它只存储了每个三角形的三个顶点坐标和法向量，没有颜色、材质、单位等额外信息。
- **无单位**: STL文件本身不包含单位信息（是毫米还是英寸）。你需要在使用它的软件中（如3D打印切片软件）来设定单位。
- **两种模式**: STL文件有ASCII（文本）和Binary（二进制）两种格式。二进制格式文件更小，读取更快，是首选格式。

## 核心用法

### 写入STL文件

写入STL文件的过程，实际上是将一个已经**网格化**的B-Rep形状的三角网格数据，提取出来并保存为STL格式。

1.  **准备网格化形状**: 你必须先有一个已经通过 `BRepMesh` 等工具生成了三角网格的 `TopoDS_Shape`。

2.  **实例化 `StlAPI_Writer`**: `stl_writer = StlAPI_Writer()`

3.  **设置模式 (可选)**: `stl_writer.SetASCIIMode(False)` # 设置为二进制模式（默认）

4.  **写入文件**: 调用 `.Write()` 方法，传入要写入的形状和文件名。
    *   `stl_writer.Write(my_meshed_shape, 'output.stl')`

### 读取STL文件

读取STL文件会创建一个由三角面片构成的 `TopoDS_Shape`，通常是一个 `TopoDS_Shell`。

1.  **实例化 `StlAPI_Reader`**: `stl_reader = StlAPI_Reader()`

2.  **读取文件**: 调用 `.Read()` 方法，传入一个空的 `TopoDS_Shape` 用于接收结果，以及文件名。
    *   `a_shell = TopoDS_Shell()`
    *   `stl_reader.Read(a_shell, 'input.stl')`
    *   读取成功后，`a_shell` 将包含从STL文件中构建的几何数据。

## 主要类

*   **`StlAPI_Writer`**: 负责将一个带有三角剖分（Triangulation）的 `TopoDS_Shape` 写入到STL文件中。
*   **`StlAPI_Reader`**: 负责从STL文件中读取三角网格数据，并构建一个 `TopoDS_Shape`。
*   **`StlAPI`**: 模块本身也提供了一些静态辅助函数，如 `StlAPI.Write(theShape, theFile)`，可以更快捷地执行写入操作。

在接下来的示例中，我们将承接上一个任务，将一个网格化后的球体写入到STL文件中，然后再读回它进行验证。
