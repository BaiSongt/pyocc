# `SelectMgr` & `AIS` - 自定义可视化与交互

到目前为止，我们都是将整个形状作为一个整体来显示和交互的。第七阶段的目标是深入 `AIS` (Application Interactive Services) 和 `SelectMgr` (Selection Manager) 的世界，学习如何实现更精细、更自定义的可视化与交互逻辑。

## 核心概念：选择模式 (Selection Mode)

默认情况下，当你在 `AIS_InteractiveContext` 中显示一个形状时，你只能选择整个形状。但是，OCCT允许你“激活”不同的**选择模式**，从而让用户能够选择一个形状的子部分。

- **选择对象**: `TopoDS_Shape` (选择整个实体，默认模式)
- **选择顶点**: `TopAbs_VERTEX`
- **选择边**: `TopAbs_EDGE`
- **选择线框**: `TopAbs_WIRE`
- **选择面**: `TopAbs_FACE`

通过激活指定的选择模式，你可以精确地控制用户能够“看到”和“点选”的拓扑层级。

## 核心用法

1.  **获取交互式上下文**: `display, start_display, ... = init_display()`，`context = display.Context`。

2.  **显示形状**: `ais_shape = display.DisplayShape(my_shape)`，获取返回的 `AIS_Shape` 对象。

3.  **激活选择模式**: 调用交互式上下文的 `.Activate()` 方法。
    *   `context.Activate(ais_shape, AIS_Shape.SelectionMode(TopAbs_FACE))`
    *   第一个参数是你要对哪个 `AIS_Shape` 对象激活模式。
    *   第二个参数是你要激活的模式，例如 `TopAbs_FACE` 表示“面选择模式”。
    *   你可以同时激活多种模式。

4.  **停用默认模式 (可选但推荐)**: 为了避免混淆，最好停用默认的整体选择模式。
    *   `context.Deactivate(ais_shape)` # 停用该ais_shape的默认（整体）选择模式

5.  **处理选择事件**: 在一个完整的GUI应用中，你会连接一个“信号”，当用户点击时，这个信号会被触发。在我们的简单脚本中，我们将创建一个菜单项，通过主动查询来获取当前被选中的对象。
    *   `context.HasDetected()`: 检查当前是否有被选中的对象。
    *   `context.DetectedOwner()`: 获取被选中的对象（它是一个 `SelectMgr_EntityOwner`）。
    *   `owner.Selectable()`: 从 `Owner` 中获取 `AIS_InteractiveObject`。
    *   `context.DetectedShape()`: 直接获取被选中的子形状（如 `TopoDS_Face`）。

## 主要类

*   **`AIS_InteractiveContext`**: 可视化与交互的总管。负责激活/停用选择模式，管理高亮和选择状态。
*   **`AIS_Shape`**: `TopoDS_Shape` 的可交互版本，可以为其单独设置选择模式。
*   **`SelectMgr_ViewerSelector`**: 选择管理器，处理来自视图的鼠标点击等事件，并确定哪个对象被选中。
*   **`SelectMgr_EntityOwner`**: 被选中对象的“所有者”，可以从中获取原始的 `AIS_` 对象以及被选中的子形状。

在接下来的示例中，我们将显示一个盒子，并激活它的“面选择”模式。然后，我们将添加一个菜单项，当用户点击它时，程序会检查并打印出当前被选中的面的信息。
