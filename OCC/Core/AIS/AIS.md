# `AIS` & `V3d` (Application Interactive Services & 3D View)

到目前为止，我们创建的所有形状都只存在于内存中。`AIS` 和 `V3d` 这两个包的使命就是将这些抽象的几何模型渲染到屏幕上，并允许用户与之交互。

可以把可视化过程理解为搭建一个“虚拟摄影棚”：

1.  **演员 (`TopoDS_Shape`)**: 这是我们之前通过 `BRepPrimAPI` 或 `BRepAlgoAPI` 创建的模型。
2.  **给演员穿上戏服 (`AIS_Shape`)**: `TopoDS_Shape` 本身是不可显示的。我们需要用 `AIS_Shape` 或其他 `AIS_` 开头的类（如 `AIS_Point`）把它包装起来，变成一个“可交互对象”（Interactive Object）。包装后，我们可以设置它的颜色、显示模式（如线框、着色）、透明度等。
3.  **舞台 (`AIS_InteractiveContext`)**: 这是一个“交互式上下文”，是所有可交互对象的管理者。你可以把多个“演员”放进这个“舞台”进行集中管理。
4.  **相机 (`V3d_View`)**: 这是观察舞台的“相机”，它定义了你从哪个角度、以何种方式（正交、透视）来观察场景。
5.  **显示器 (Viewer Window)**: 这是最终呈现画面的窗口。`pythonocc-core` 提供了一个基于Qt的简单查看器 `OCC.Display.SimpleGui`，它已经为我们封装好了窗口、相机和交互式上下文的创建和关联，极大地简化了可视化流程。

## 可视化流程

使用 `OCC.Display.SimpleGui` 的基本流程如下：

1.  **导入 `init_display`**: 从 `OCC.Display.SimpleGui` 导入这个关键的初始化函数。

2.  **创建模型**: 使用我们之前学过的方法创建你的 `TopoDS_Shape`。

3.  **初始化显示**: 调用 `init_display()`。它会返回几个核心对象，最重要的是 `display` 对象，它封装了 `AIS_InteractiveContext` 和 `V3d_View`。
    *   `display, start_display, add_menu, add_function_to_menu = init_display()`

4.  **显示对象**: 调用 `display.DisplayShape(your_shape, ...)`。这个方法会自动将你的 `TopoDS_Shape` 包装成 `AIS_Shape` 并添加到交互式上下文中。你可以通过参数设置颜色、透明度等。

5.  **启动查看器**: 调用 `start_display()`。这将启动Qt事件循环，弹出图形窗口，然后你就可以通过鼠标来旋转、平移和缩放你的模型了。

在接下来的示例中，我们将把第四步创建的“带洞的盒子”在窗口中显示出来。
