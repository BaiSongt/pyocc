# -*- coding: utf-8 -*-

"""
OCAF Example 7.1: Custom Interaction - Selection Modes
# OCAF 示例 7.1: 自定义交互 - 选择模式

This script is an INTERACTIVE example. It demonstrates how to activate specific
selection modes (e.g., face selection) and how to query the selection status.
# 本脚本是一个交互式示例。它演示了如何激活特定的选择模式（例如，面选择）以及如何查询选择状态。

**INSTRUCTIONS:**
# **操作指南：**
1. Run the script. A window with a box will appear.
# 1. 运行脚本。一个带有盒子的窗口将会出现。
2. Click on any face of the box. The face you clicked will be highlighted.
# 2. 点击盒子的任意一个面。您点击的面将会高亮显示。
3. Go to the menu `Tools -> Check Selection`.
# 3. 前往菜单栏的 `Tools -> Check Selection`。
4. Look at the console output. It will print information about the face you selected.
# 4. 查看控制台的输出。它将打印出您所选中的面的信息。
"""

# --- Imports ---
# --- 导入 ---
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Display.SimpleGui import init_display

def check_selection(display):
    """
    This function is called when the 'Check Selection' menu item is clicked.
    It checks the interactive context for selected objects and prints info.
    # 当‘Check Selection’菜单项被点击时，此函数被调用。
    # 它会检查交互式上下文中的被选对象并打印信息。
    """
    print("\n--- Checking Selection --- ")
    # --- 正在检查选择 ---
    # The display.Context object is the AIS_InteractiveContext
    # # display.Context 对象就是 AIS_InteractiveContext
    if not display.Context.HasDetected():
        print("No object is currently selected.")
        # 当前没有对象被选中。
        return

    # To get detailed information, we ask for the detected owner
    # # 为了获取详细信息，我们请求获取被探测到的所有者
    owner = display.Context.DetectedOwner()
    print(f"Detected owner: {owner.DynamicType()}")
    # 探测到的所有者: ...

    # We can also directly get the selected shape (e.g., the TopoDS_Face)
    # # 我们也可以直接获取被选中的形状（例如 TopoDS_Face）
    selected_subshape = display.Context.DetectedShape()
    print(f"Detected sub-shape type: {selected_subshape.ShapeType()}")
    # 探测到的子形状类型: ...

    # Let's use BRepCheck_Analyzer to get more info about the face
    # # 让我们使用 BRepCheck_Analyzer 来获取关于该面的更多信息
    from OCC.Core.BRepCheck import BRepCheck_Analyzer
    analyzer = BRepCheck_Analyzer(selected_subshape)
    is_valid = analyzer.IsValid()
    print(f"Is the selected face valid? {is_valid}")
    # 被选中的面是否有效？...
    print("------------------------")

def run_selection_example():
    """
    Sets up the viewer, displays a shape, and activates face selection mode.
    # 设置查看器，显示一个形状，并激活面选择模式。
    """
    # 1. Initialize the viewer and create a shape
    # 1. 初始化查看器并创建一个形状
    display, start_display, add_menu, add_function_to_menu = init_display()
    the_box = BRepPrimAPI_MakeBox(100, 100, 100).Shape()
    ais_box = display.DisplayShape(the_box, update=False)[0] # Get the AIS_Shape
    # # 获取 AIS_Shape

    # 2. Activate Face Selection Mode for the box
    # 2. 为该盒子激活面选择模式
    # The second argument to Activate is the selection mode enum.
    # # Activate 的第二个参数是选择模式的枚举值。
    # We can use `AIS_Shape.SelectionMode(TopAbs_FACE)` or just the int value 4.
    # # 我们可以使用 `AIS_Shape.SelectionMode(TopAbs_FACE)` 或直接使用整数值 4。
    display.Context.Activate(ais_box, 4) # 4 corresponds to TopAbs_FACE
    # # 4 对应 TopAbs_FACE
    print("Face selection mode has been activated for the box.")
    # 已为该盒子激活面选择模式。

    # 3. Add a menu item to trigger the selection check
    # 3. 添加一个菜单项来触发选择检查
    add_menu("Tools")
    add_function_to_menu("Tools", lambda event: check_selection(display))

    # 4. Fit the view and start the event loop
    # 4. 适配视图并启动事件循环
    display.FitAll()
    start_display()

if __name__ == "__main__":
    print(__doc__)
    run_selection_example()
