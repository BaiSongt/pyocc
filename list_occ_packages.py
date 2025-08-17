import pkgutil
import inspect
import importlib
import json
from pathlib import Path

def build_package_tree(module):
    """
    递归构建包/模块/类结构并返回字典
    :param module: 当前模块对象
    :return: dict  {name, type, children, classes}
    """
    node = {
        "name": module.__name__,
        "type": "package",
        "classes": [],
        "children": []
    }

    # 1. 当前包直接定义的类
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
            node["classes"].append(name)

    # 2. 遍历子包/子模块
    for finder, sub_name, is_pkg in pkgutil.iter_modules(module.__path__, module.__name__ + '.'):
        try:
            sub_mod = importlib.import_module(sub_name)
            if is_pkg:
                # 子包 -> 递归
                node["children"].append(build_package_tree(sub_mod))
            else:
                # 子模块 -> 收集类
                mod_node = {
                    "name": sub_name,
                    "type": "module",
                    "classes": [],
                    "children": []
                }
                for cls_name, cls_obj in inspect.getmembers(sub_mod, inspect.isclass):
                    if cls_obj.__module__ == sub_mod.__name__:
                        mod_node["classes"].append(cls_name)
                node["children"].append(mod_node)
        except Exception as e:
            node["children"].append({
                "name": sub_name,
                "type": "error",
                "error": str(e),
                "classes": [],
                "children": []
            })
    return node

if __name__ == '__main__':
    try:
        import OCC
        print("检测到 pythonocc-core 安装，开始生成结构...")

        tree = build_package_tree(OCC)

        out_path = Path(__file__).with_name("occ_structure.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(tree, f, ensure_ascii=False, indent=2)

        print(f"已导出到：{out_path}")
    except ImportError:
        print("错误：未检测到 pythonocc-core 安装，请先执行：pip install pythonocc-core")
