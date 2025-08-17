# OCCT Python 学习库

这是一个用于学习 `pythonocc-core` 的结构化、实战驱动的资源库。本项目旨在通过系统性的文档、可运行的示例代码和阶段性的综合项目，帮助开发者从零开始，逐步掌握Open CASCADE Technology (OCCT) 在Python环境下的核心应用。

---

## ✨ 项目特点

- **系统化的学习路径**: 内容被划分为“入门”和“进阶”两个清晰的计划，每个计划又包含多个阶段，循序渐进，逻辑清晰。
- **文档与代码并行**: 每个核心模块都配有详细的Markdown中文文档 (`/OCC`) 和对应的Python示例代码 (`/src`)。
- **双语注释**: 所有示例代码均包含精准的英文和中文注释，便于理解。
- **阶段性总结**: 每个学习阶段都以一个综合性的示例项目收尾 (`/examples`)，用于巩固和串联该阶段学习的所有核心技能。

## 🚀 如何开始

### 1. 环境准备

本项目推荐使用 `conda` 来管理环境。

```bash
# 1. 克隆本项目
# git clone ...

# 2. 创建并激活conda环境 (我们此前的环境名为 occ)
conda create -n occ python=3.10
conda activate occ

# 3. 安装依赖
pip install -r requirements.txt
```

### 2. 开始学习

我们强烈建议您从阅读我们的**学习计划**开始，它为您的学习之旅提供了清晰的路线图。

- **[总学习计划 (plan.md)](./plan.md)**: 了解项目的整体分阶段学习路径。
- **[入门计划详细任务 (task_schedule.md)](./task_schedule.md)**: 查看入门阶段每个模块需要掌握的核心类与目标。
- **[进阶计划详细任务 (task_schedule_advanced.md)](./task_schedule_advanced.md)**: 为成为OCCT专家规划的后续学习路径。

### 3. 建议工作流

对于入门计划中的每一个任务（例如 `BRepGProp`）：

1.  首先，阅读位于 `/OCC/Core/BRepGProp/BRepGProp.md` 的文档，理解其核心概念和用途。
2.  然后，打开并学习位于 `/src/Core/BRepGProp/example.py` 的示例代码，理解API的实际用法。
3.  运行该示例脚本 `python src/Core/BRepGProp/example.py`，观察其输出，确保理解其执行过程。
4.  当完成一个阶段的所有任务后，打开 `/examples` 目录下对应的阶段汇总示例，学习如何综合运用所有知识点。

## 📁 仓库结构

```
pyocc/
├── .gitignore
├── OCC/                    # 存放所有OCCT包的Markdown文档
│   └── Core/
│       ├── AIS/
│       ├── BRepAlgoAPI/
│       └── ...
├── src/                    # 存放与文档对应的、可运行的示例代码
│   └── Core/
│       ├── AIS/
│       ├── BRepAlgoAPI/
│       └── ...
├── examples/               # 存放每个阶段的汇总示例项目
│   ├── phase_1_core_concepts.py
│   └── ...
├── plan.md                 # 项目总学习计划
├── prd.md                  # 项目产品需求文档
├── requirements.txt        # 项目依赖
├── task_schedule.md        # 入门计划详细任务表
└── task_schedule_advanced.md # 进阶计划详细任务表
```

---

现在，您可以正式开始您的OCCT学习之旅了！祝您学习愉快！
