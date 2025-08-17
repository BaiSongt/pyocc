# `V3d` - 自定义视图控制与相机管理

在前面的学习中，我们主要使用 `SimpleGui` 提供的默认视图控制。第七阶段的第二个任务是深入学习 `V3d` 包，掌握如何直接控制OCCT的视图系统，实现更精细、更专业的相机控制和视图操作。

## 核心概念：OCCT视图系统架构

OCCT的视图系统采用分层架构设计：

### 1. `V3d_Viewer` - 查看器
- **作用**: 管理多个视图的顶层容器
- **功能**: 控制光照、背景、显示质量等全局设置
- **关系**: 一个查看器可以包含多个视图

### 2. `V3d_View` - 视图
- **作用**: 单个3D视图的核心控制器
- **功能**: 控制相机位置、投影模式、视图变换等
- **关系**: 每个视图对应一个渲染窗口

### 3. `Graphic3d_Camera` - 相机
- **作用**: 定义观察参数的核心对象
- **功能**: 控制视点、目标点、上方向、视野角度等
- **关系**: 每个视图包含一个相机对象

## 核心功能

### 1. 相机位置控制
```python
# 设置相机位置（视点）
view.Camera().SetEye(gp_Pnt(100, 100, 100))

# 设置观察目标点
view.Camera().SetCenter(gp_Pnt(0, 0, 0))

# 设置上方向
view.Camera().SetUp(gp_Dir(0, 0, 1))
```

### 2. 投影模式控制
```python
# 设置透视投影
view.Camera().SetProjectionType(Graphic3d_Camera.Projection_Perspective)

# 设置正交投影
view.Camera().SetProjectionType(Graphic3d_Camera.Projection_Orthographic)

# 设置视野角度（仅透视投影有效）
view.Camera().SetFOVy(math.radians(45))  # 45度视野角
```

### 3. 视图变换操作
```python
# 旋转视图
view.Rotate(delta_x, delta_y, delta_z)

# 平移视图
view.Pan(delta_x, delta_y)

# 缩放视图
view.Zoom(0, 0, zoom_factor)

# 适配所有对象
view.FitAll()
```

### 4. 预设视图方向
```python
# 前视图
view.SetProj(V3d_Yneg)

# 顶视图
view.SetProj(V3d_Zpos)

# 右视图
view.SetProj(V3d_Xpos)

# 等轴测视图
view.SetProj(V3d_XposYnegZpos)
```

## 主要类详解

### `V3d_View`
- **`Camera()`**: 获取视图的相机对象
- **`SetProj(direction)`**: 设置预设视图方向
- **`Rotate(ax, ay, az)`**: 绕指定轴旋转视图
- **`Pan(dx, dy)`**: 平移视图
- **`Zoom(x, y, factor)`**: 在指定点进行缩放
- **`FitAll()`**: 自动适配所有可见对象
- **`Redraw()`**: 重新绘制视图

### `Graphic3d_Camera`
- **`SetEye(point)`**: 设置相机位置
- **`SetCenter(point)`**: 设置观察目标
- **`SetUp(direction)`**: 设置上方向
- **`SetProjectionType(type)`**: 设置投影类型
- **`SetFOVy(angle)`**: 设置垂直视野角度

### `V3d_Viewer`
- **`SetDefaultLights()`**: 设置默认光照
- **`SetLightOn(light)`**: 开启指定光源
- **`SetLightOff(light)`**: 关闭指定光源

## 高级功能

### 1. 自定义光照系统
```python
# 创建定向光源
directional_light = V3d_DirectionalLight()
directional_light.SetDirection(gp_Dir(1, -1, -1))
viewer.AddLight(directional_light)
```

### 2. 视图动画
```python
# 平滑过渡到新的相机位置
def animate_to_position(view, target_eye, target_center, steps=30):
    current_eye = view.Camera().Eye()
    current_center = view.Camera().Center()
    
    for i in range(steps):
        t = i / (steps - 1)
        # 线性插值计算中间位置
        interp_eye = interpolate_point(current_eye, target_eye, t)
        interp_center = interpolate_point(current_center, target_center, t)
        
        view.Camera().SetEye(interp_eye)
        view.Camera().SetCenter(interp_center)
        view.Redraw()
```

### 3. 视图状态保存与恢复
```python
# 保存当前视图状态
def save_view_state(view):
    camera = view.Camera()
    return {
        'eye': camera.Eye(),
        'center': camera.Center(),
        'up': camera.Up(),
        'projection': camera.ProjectionType(),
        'fovy': camera.FOVy()
    }

# 恢复视图状态
def restore_view_state(view, state):
    camera = view.Camera()
    camera.SetEye(state['eye'])
    camera.SetCenter(state['center'])
    camera.SetUp(state['up'])
    camera.SetProjectionType(state['projection'])
    camera.SetFOVy(state['fovy'])
    view.Redraw()
```

## 实际应用场景

1. **专业CAD软件**: 提供标准的视图控制界面（前、后、左、右、顶、底视图）
2. **工程分析**: 从特定角度观察分析结果
3. **演示动画**: 创建产品展示的相机路径动画
4. **虚拟现实**: 与VR设备集成，提供沉浸式体验
5. **多视图显示**: 同时显示多个不同角度的视图

在接下来的示例中，我们将创建一个完整的自定义视图控制系统，展示如何实现专业级的相机控制功能。
