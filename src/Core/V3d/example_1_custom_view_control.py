# -*- coding: utf-8 -*-

"""
OCCT Example 7.2: Custom View Control - V3d System
# OCCT 示例 7.2: 自定义视图控制 - V3d 系统

This script demonstrates advanced view control using OCCT's V3d system.
It provides custom camera controls, preset views, and projection mode switching.
# 本脚本演示了使用OCCT的V3d系统进行高级视图控制。
# 它提供了自定义相机控制、预设视图和投影模式切换功能。

**FEATURES:**
# **功能特性：**
1. Custom camera position control
# 1. 自定义相机位置控制
2. Preset view directions (Front, Top, Right, Isometric)
# 2. 预设视图方向（前视图、顶视图、右视图、等轴测视图）
3. Projection mode switching (Perspective/Orthographic)
# 3. 投影模式切换（透视/正交）
4. View state saving and restoration
# 4. 视图状态保存和恢复
5. Smooth view transitions
# 5. 平滑视图过渡
"""

# --- Imports ---
# --- 导入 ---
import math
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Vec
from OCC.Core.V3d import V3d_Xpos, V3d_Ypos, V3d_Zpos, V3d_Xneg, V3d_Yneg, V3d_Zneg, V3d_XposYnegZpos
from OCC.Core.Graphic3d import Graphic3d_Camera
from OCC.Display.SimpleGui import init_display

class CustomViewControl:
    """
    A class that provides advanced view control functionality.
    # 提供高级视图控制功能的类。
    """

    def __init__(self, display):
        """
        Initialize the custom view control system.
        # 初始化自定义视图控制系统。
        """
        self.display = display
        self.view = display.View  # Get the V3d_View object
        # # 获取 V3d_View 对象
        self.saved_states = {}  # Dictionary to store saved view states
        # # 用于存储保存的视图状态的字典

        print("Custom View Control initialized.")
        # 自定义视图控制已初始化。

    def set_camera_position(self, eye_x, eye_y, eye_z, center_x=0, center_y=0, center_z=0):
        """
        Set the camera position and target.
        # 设置相机位置和目标。
        """
        camera = self.view.Camera()
        camera.SetEye(gp_Pnt(eye_x, eye_y, eye_z))
        camera.SetCenter(gp_Pnt(center_x, center_y, center_z))
        camera.SetUp(gp_Dir(0, 0, 1))  # Set up direction to Z-axis
        # # 将上方向设置为Z轴
        self.view.Redraw()
        print(f"Camera position set to: Eye({eye_x}, {eye_y}, {eye_z}), Center({center_x}, {center_y}, {center_z})")
        # 相机位置设置为：视点(...), 中心(...)

    def set_preset_view(self, view_name):
        """
        Set a preset view direction.
        # 设置预设视图方向。
        """
        view_directions = {
            'front': V3d_Yneg,      # Front view (looking along -Y axis)
            # # 前视图（沿-Y轴观察）
            'back': V3d_Ypos,       # Back view (looking along +Y axis)
            # # 后视图（沿+Y轴观察）
            'right': V3d_Xpos,      # Right view (looking along +X axis)
            # # 右视图（沿+X轴观察）
            'left': V3d_Xneg,       # Left view (looking along -X axis)
            # # 左视图（沿-X轴观察）
            'top': V3d_Zpos,        # Top view (looking along +Z axis)
            # # 顶视图（沿+Z轴观察）
            'bottom': V3d_Zneg,     # Bottom view (looking along -Z axis)
            # # 底视图（沿-Z轴观察）
            'isometric': V3d_XposYnegZpos  # Isometric view
            # # 等轴测视图
        }

        if view_name.lower() in view_directions:
            self.view.SetProj(view_directions[view_name.lower()])
            self.view.FitAll()
            print(f"Set to {view_name} view.")
            # 设置为 {view_name} 视图。
        else:
            print(f"Unknown view: {view_name}. Available views: {list(view_directions.keys())}")
            # 未知视图：{view_name}。可用视图：...

    def set_projection_mode(self, mode):
        """
        Set the projection mode (perspective or orthographic).
        # 设置投影模式（透视或正交）。
        """
        camera = self.view.Camera()

        if mode.lower() == 'perspective':
            camera.SetProjectionType(Graphic3d_Camera.Projection_Perspective)
            camera.SetFOVy(math.radians(45))  # Set 45-degree field of view
            # # 设置45度视野角
            print("Projection mode set to: Perspective")
            # 投影模式设置为：透视
        elif mode.lower() == 'orthographic':
            camera.SetProjectionType(Graphic3d_Camera.Projection_Orthographic)
            print("Projection mode set to: Orthographic")
            # 投影模式设置为：正交
        else:
            print("Invalid projection mode. Use 'perspective' or 'orthographic'.")
            # 无效的投影模式。请使用 'perspective' 或 'orthographic'。
            return

        self.view.Redraw()

    def save_view_state(self, state_name):
        """
        Save the current view state.
        # 保存当前视图状态。
        """
        camera = self.view.Camera()
        self.saved_states[state_name] = {
            'eye': camera.Eye(),
            'center': camera.Center(),
            'up': camera.Up(),
            'projection': camera.ProjectionType(),
            'fovy': camera.FOVy()
        }
        print(f"View state '{state_name}' saved.")
        # 视图状态 '{state_name}' 已保存。

    def restore_view_state(self, state_name):
        """
        Restore a saved view state.
        # 恢复保存的视图状态。
        """
        if state_name not in self.saved_states:
            print(f"No saved state named '{state_name}'.")
            # 没有名为 '{state_name}' 的保存状态。
            return

        state = self.saved_states[state_name]
        camera = self.view.Camera()

        camera.SetEye(state['eye'])
        camera.SetCenter(state['center'])
        camera.SetUp(state['up'])
        camera.SetProjectionType(state['projection'])
        camera.SetFOVy(state['fovy'])

        self.view.Redraw()
        print(f"View state '{state_name}' restored.")
        # 视图状态 '{state_name}' 已恢复。

    def get_camera_info(self):
        """
        Print current camera information.
        # 打印当前相机信息。
        """
        camera = self.view.Camera()
        eye = camera.Eye()
        center = camera.Center()
        up = camera.Up()

        projection = "Perspective" if camera.ProjectionType() == Graphic3d_Camera.Projection_Perspective else "Orthographic"
        # # 如果是透视投影则为"Perspective"，否则为"Orthographic"

        print("\n--- Current Camera Information ---")
        # --- 当前相机信息 ---
        print(f"Eye Position: ({eye.X():.2f}, {eye.Y():.2f}, {eye.Z():.2f})")
        # 视点位置: ...
        print(f"Center Position: ({center.X():.2f}, {center.Y():.2f}, {center.Z():.2f})")
        # 中心位置: ...
        print(f"Up Direction: ({up.X():.2f}, {up.Y():.2f}, {up.Z():.2f})")
        # 上方向: ...
        print(f"Projection Mode: {projection}")
        # 投影模式: ...
        if camera.ProjectionType() == Graphic3d_Camera.Projection_Perspective:
            print(f"Field of View: {math.degrees(camera.FOVy()):.1f} degrees")
            # 视野角度: ... 度
        print("--------------------------------\n")

def create_demo_scene():
    """
    Create a demo scene with multiple objects for view control demonstration.
    # 创建一个包含多个对象的演示场景，用于视图控制演示。
    """
    # Create a base box
    # # 创建一个基础盒子
    base_box = BRepPrimAPI_MakeBox(100, 100, 20).Shape()

    # Create a cylinder to cut a hole
    # # 创建一个圆柱体来切出一个孔
    cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(50, 50, 0), gp_Dir(0, 0, 1)), 15, 20).Shape()

    # Cut the hole
    # # 切出孔
    box_with_hole = BRepAlgoAPI_Cut(base_box, cylinder).Shape()

    # Create a sphere
    # # 创建一个球体
    sphere = BRepPrimAPI_MakeSphere(gp_Pnt(150, 50, 30), 25).Shape()

    return [box_with_hole, sphere]

def setup_view_control_menu(add_menu, add_function_to_menu, view_control):
    """
    Set up the menu system for view control.
    # 设置视图控制的菜单系统。
    """
    # Add View Control menu
    # # 添加视图控制菜单
    add_menu("View Control")

    # Preset views submenu
    # # 预设视图子菜单
    add_menu("Preset Views")
    add_function_to_menu("Preset Views", lambda event: view_control.set_preset_view('front'))
    add_function_to_menu("Preset Views", lambda event: view_control.set_preset_view('top'))
    add_function_to_menu("Preset Views", lambda event: view_control.set_preset_view('right'))
    add_function_to_menu("Preset Views", lambda event: view_control.set_preset_view('isometric'))

    # Projection mode submenu
    # # 投影模式子菜单
    add_menu("Projection")
    add_function_to_menu("Projection", lambda event: view_control.set_projection_mode('perspective'))
    add_function_to_menu("Projection", lambda event: view_control.set_projection_mode('orthographic'))

    # Camera control submenu
    # # 相机控制子菜单
    add_menu("Camera")
    add_function_to_menu("Camera", lambda event: view_control.get_camera_info())
    add_function_to_menu("Camera", lambda event: view_control.save_view_state('user_view'))
    add_function_to_menu("Camera", lambda event: view_control.restore_view_state('user_view'))

def run_custom_view_example():
    """
    Main function to run the custom view control example.
    # 运行自定义视图控制示例的主函数。
    """
    # Initialize the display
    # # 初始化显示
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Create and display the demo scene
    # # 创建并显示演示场景
    shapes = create_demo_scene()
    for i, shape in enumerate(shapes):
        color = "blue" if i == 0 else "red"
        display.DisplayShape(shape, color=color, update=False)

    # Initialize custom view control
    # # 初始化自定义视图控制
    view_control = CustomViewControl(display)

    # Set up the menu system
    # # 设置菜单系统
    setup_view_control_menu(add_menu, add_function_to_menu, view_control)

    # Set initial view
    # # 设置初始视图
    view_control.set_preset_view('isometric')
    view_control.set_projection_mode('perspective')

    # Print instructions
    # # 打印操作指南
    print("\n=== Custom View Control Demo ===")
    # === 自定义视图控制演示 ===
    print("Use the menu system to:")
    # 使用菜单系统来：
    print("- Switch between preset views (Front, Top, Right, Isometric)")
    # - 在预设视图之间切换（前视图、顶视图、右视图、等轴测视图）
    print("- Change projection mode (Perspective/Orthographic)")
    # - 更改投影模式（透视/正交）
    print("- Get camera information")
    # - 获取相机信息
    print("- Save and restore view states")
    # - 保存和恢复视图状态
    print("================================\n")

    # Fit all objects and start the display
    # # 适配所有对象并启动显示
    display.FitAll()
    start_display()

if __name__ == '__main__':
    run_custom_view_example()
