# OCAF (Open CASCADE Application Framework) 完整指南

OCAF是Open CASCADE Technology的应用框架，专门为构建复杂的CAD/CAM应用而设计。它提供了一套完整的工具来管理设计数据、参数化建模和应用程序架构。

## 📚 学习路径

### 第一阶段：基础概念
**文档**: [OCAF_1_TDocStd.md](OCAF_1_TDocStd.md)  
**示例**: [example_1_document_and_attributes.py](../../src/Core/OCAF/example_1_document_and_attributes.py)

学习内容：
- OCAF文档系统的基本概念
- 标签（Label）的层次结构
- 属性（Attribute）的使用方法
- 事务管理机制

关键类：
- `TDocStd_Document` - 文档管理
- `TDF_Label` - 数据标签
- `TDataStd_Real` - 实数属性
- `TDataStd_Name` - 名称属性

### 第二阶段：参数化建模
**文档**: [OCAF_2_TNaming_TFunction.md](OCAF_2_TNaming_TFunction.md)  
**示例**: [example_2_parametric_modeling.py](../../src/Core/OCAF/example_2_parametric_modeling.py)

学习内容：
- TNaming系统的形状管理
- 参数化几何生成
- 属性引用模式的正确使用
- 几何体的存储和检索

关键类：
- `TNaming_Builder` - 形状构建器
- `TNaming_NamedShape` - 命名形状
- `BRepPrimAPI_MakeBox` - 基础几何创建
- `BRepGProp` - 几何属性计算

### 第三阶段：完整CAD应用
**文档**: [OCAF_3_Advanced_Applications.md](OCAF_3_Advanced_Applications.md)  
**示例**: [example_3_parametric_cad_app.py](../../src/Core/OCAF/example_3_parametric_cad_app.py)

学习内容：
- 复杂参数化模型的构建
- 多参数管理和验证
- 布尔运算的集成
- 交互式用户界面
- 模型验证和错误处理

关键特性：
- 多参数协调管理
- 实时几何更新
- 用户友好的交互界面
- 健壮的错误处理

## 🔧 API使用要点

### 正确的属性访问模式
```python
# ✅ 正确方式：保存属性引用
attr = TDataStd_Real.Set(label, value)
current_value = attr.Get()
attr.Set(new_value)

# ❌ 错误方式：尝试查找属性（API不存在）
# attr, found = TDataStd_Real.Find(label)  # 这个方法不存在
```

### 形状存储的正确方法
```python
# ✅ 正确方式：使用TNaming_Builder
builder = TNaming_Builder(label)
builder.Generated(shape)
shape_attr = builder.NamedShape()
retrieved_shape = shape_attr.Get()

# ❌ 错误方式：尝试直接查找形状
# shape_attr, found = TNaming_NamedShape.Find(label)  # 这个方法不存在
```

### 事务管理
```python
# 开始事务
doc.NewCommand()

# 进行数据修改
attr.Set(new_value)

# 提交事务
doc.CommitCommand()
```

## 🚀 快速开始

1. **运行基础示例**：
   ```bash
   conda activate occ
   python src/Core/OCAF/example_1_document_and_attributes.py
   ```

2. **体验参数化建模**：
   ```bash
   python src/Core/OCAF/example_2_parametric_modeling.py
   ```

3. **尝试完整CAD应用**：
   ```bash
   python src/Core/OCAF/example_3_parametric_cad_app.py
   ```

## 📋 示例功能对比

| 示例 | 功能特性 | 复杂度 | 适用场景 |
|------|----------|--------|----------|
| 示例1 | 基础属性操作 | 简单 | 学习OCAF基础概念 |
| 示例2 | 参数化盒子 | 中等 | 理解参数化建模原理 |
| 示例3 | 带孔盒子+交互界面 | 复杂 | 构建实际CAD应用 |

## 🔍 常见问题解决

### 1. 属性访问错误
**问题**: `AttributeError: type object 'TDataStd_Real' has no attribute 'Find'`  
**解决**: 使用属性引用模式，不要尝试查找属性

### 2. 几何操作失败
**问题**: 布尔运算失败或产生无效几何体  
**解决**: 添加参数验证和几何体有效性检查

### 3. 事务管理混乱
**问题**: 数据修改没有正确保存  
**解决**: 确保每次修改都在事务中进行

## 🎯 学习建议

1. **循序渐进**: 按照示例1→2→3的顺序学习
2. **动手实践**: 运行每个示例，观察输出结果
3. **修改参数**: 尝试修改示例中的参数值，观察变化
4. **阅读代码**: 仔细阅读代码注释，理解每个步骤的作用
5. **扩展功能**: 基于示例添加新的功能和特性

## 📖 相关资源

- [Open CASCADE官方文档](https://dev.opencascade.org/)
- [pythonocc-core项目](https://github.com/tpaviot/pythonocc-core)
- [OCCT源码](https://github.com/Open-Cascade-SAS/OCCT)

通过系统学习这三个阶段的内容，您将掌握使用OCAF构建专业级CAD应用的核心技能。
