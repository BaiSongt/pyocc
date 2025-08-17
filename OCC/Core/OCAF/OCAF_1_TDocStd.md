# OCAF  Part 1: `TDocStd` & `TDataStd` - 文档、标签与属性

OCAF (Open CASCADE Application Framework) 是一个用于开发CAD/CAM/CAE应用程序的软件框架。它提供了一套标准化的数据模型和服务，用于管理和组织应用数据，其核心思想是**文档-属性模型**。

与之前我们直接创建几何形状不同，使用OCAF时，所有的几何、参数和它们之间的关系，都被结构化地存储在一个“文档”对象中。

## OCAF核心架构

OCAF的数据结构可以理解为一颗“属性树”，由三个核心概念组成：

1.  **文档 (Document - `TDocStd_Document`)**: 这是所有数据的顶层容器。它管理着整个数据树、事务（用于撤销/重做）和数据存储/恢复。你可以把它想象成一个 `.sldprt` 或 `.catpart` 文件在内存中的表示。

2.  **标签 (Label - `TDF_Label`)**: 这是数据树中的“节点”或“目录”。标签本身不存储数据，它只是一个定位符，用于组织数据结构。所有的标签都以树状结构进行组织，有一个根标签（`doc.Main()`），其他所有标签都是根标签的子孙。

3.  **属性 (Attribute - `TDF_Attribute`)**: 这才是真正存储数据的地方。**数据被作为“属性”附加（Attach）在标签上**。每个标签可以附加多个不同类型的属性。例如，一个标签上可以同时有一个`TDataStd_Name`属性（存储其名称）和一个`TNaming_NamedShape`属性（存储一个几何形状）。

## `TDataStd` - 标准数据属性

`TDataStd` 包提供了一系列最基础、最常用的属性类型，用于在标签上存储标准数据类型。

*   **`TDataStd_Name`**: 用于给标签附加一个名称。
*   **`TDataStd_Integer`**: 用于在标签上存储一个整数值。
*   **`TDataStd_Real`**: 用于在标签上存储一个浮点数值。
*   **`TDataStd_AsciiString`**: 用于在标签上存储一个字符串。
*   **`TDataStd_RealArray`**: 用于存储一个浮点数数组。

## 核心用法

1.  **创建文档**: `doc = TDocStd_Document("MyDocument")`
2.  **获取根标签**: `root = doc.Main()`
3.  **创建子标签**: `a_label = root.FindChild(1, True)` # `True`表示如果不存在则创建
4.  **设置属性**: `TDataStd_Real.Set(a_label, 3.14)` # 在`a_label`上设置一个`TDataStd_Real`属性，值为3.14
5.  **获取属性**: 
    *   `an_attribute = TDataStd_Real()` # 创建一个空的属性对象用于接收结果
    *   `if a_label.FindAttribute(TDataStd_Real.GetID(), an_attribute):` # 查找属性
    *   `value = an_attribute.Get()` # 获取值

在接下来的示例中，我们将演示如何创建一个文档，在其中构建一个清晰的标签树来存储一组“参数”，并为每个参数设置一个浮点数值。
