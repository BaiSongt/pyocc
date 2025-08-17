# `STEPControl` (STEP Control)

`STEP` (Standard for the Exchange of Product model data) 是在不同CAD系统之间交换三维数据的国际标准（ISO 10303）。几乎所有的主流CAD软件都支持STEP文件的导入和导出。`STEPControl` 模块就是OCCT中用于处理这种格式的官方工具。

掌握 `STEPControl` 意味着你写的程序将能够与SolidWorks, CATIA, AutoCAD, Fusion 360等专业软件进行数据交互。

## 核心用法

`STEPControl` 的使用主要围绕“读取器”（Reader）和“写入器”（Writer）两个核心类。

### 读取STEP文件

1.  **实例化 `STEPControl_Reader`**: `step_reader = STEPControl_Reader()`

2.  **读取文件**: 调用 `.ReadFile()` 方法并传入文件路径。
    *   `status = step_reader.ReadFile('my_model.step')`

3.  **检查状态**: 检查返回的状态。如果状态是 `IFSelect_RetDone`，则表示文件被成功识别和加载。

4.  **转换模型**: 调用 `.TransferRoot()` (或 `.TransferRoots()`) 将文件中的一个或所有根实体转换为OCCT的 `TopoDS_Shape`。
    *   `step_reader.TransferRoot(1)` # 转换第一个根实体

5.  **获取形状**: 调用 `.Shape()` 获取转换后的 `TopoDS_Shape`。
    *   `my_shape = step_reader.Shape(1)`

### 写入STEP文件

1.  **实例化 `STEPControl_Writer`**: `step_writer = STEPControl_Writer()`

2.  **转换形状**: 调用 `.Transfer()` 方法，将一个 `TopoDS_Shape` 转换为STEP实体。第二个参数 `STEPControl_AsIs` 表示按原样转换。
    *   `status = step_writer.Transfer(my_shape, STEPControl_AsIs)`

3.  **写入文件**: 调用 `.Write()` 方法将转换后的内容保存到文件。
    *   `status = step_writer.Write('output_model.step')`

## 主要类

*   **`STEPControl_Reader`**: 负责解析 `.step` 或 `.stp` 文件，并将其内容转换为OCCT的内部数据结构。
*   **`STEPControl_Writer`**: 负责将OCCT的 `TopoDS_Shape` 转换为STEP格式并写入文件。
*   **`STEPControl_StepModelType`**: 一个枚举类型，用于在写入时指定STEP的应用协议，如 `STEPControl_AP203` 或 `STEPControl_AP214CD`。`STEPControl_AsIs` 是最常用的，表示按原样转换。

在接下来的示例中，为了让示例可以独立运行，我们将先创建一个简单的几何体并将其**写入**到一个STEP文件中，然后再从该文件中**读取**它，并验证读取是否成功。
