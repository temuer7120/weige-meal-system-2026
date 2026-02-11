#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("开始测试导入...")

try:
    from app import app, db
    print("成功导入app和db")
except Exception as e:
    print(f"导入app失败: {e}")

try:
    from models.supplier import Supplier
    print("成功导入Supplier模型")
except Exception as e:
    print(f"导入Supplier模型失败: {e}")

try:
    from models.ingredient import Ingredient
    print("成功导入Ingredient模型")
except Exception as e:
    print(f"导入Ingredient模型失败: {e}")

try:
    from models.dish import Dish
    print("成功导入Dish模型")
except Exception as e:
    print(f"导入Dish模型失败: {e}")

try:
    from models.menu import Menu, MenuDish
    print("成功导入Menu和MenuDish模型")
except Exception as e:
    print(f"导入Menu模型失败: {e}")

print("测试完成!")
