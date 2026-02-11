#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Excel数据导入脚本
"""

import os
import sys
import pandas as pd
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("开始导入Excel数据到数据库...")

# 先检查pandas是否能读取Excel文件
try:
    base_menu_path = "../基础餐单2025.xlsx"
    daily_menu_path = "../每日厨房餐单2025.xlsx"
    
    print(f"读取 {base_menu_path}...")
    base_df = pd.read_excel(base_menu_path)
    print(f"基础餐单文件读取成功，形状: {base_df.shape}")
    print(f"基础餐单列名: {list(base_df.columns)}")
    
    print(f"\n读取 {daily_menu_path}...")
    daily_df = pd.read_excel(daily_menu_path)
    print(f"每日厨房餐单文件读取成功，形状: {daily_df.shape}")
    print(f"每日厨房餐单列名: {list(daily_df.columns)}")
    
    # 提取食材和菜品名称
    ingredients_set = set()
    dishes_set = set()
    
    # 从基础餐单提取
    print("\n从基础餐单提取数据...")
    for col in base_df.columns:
        if col != '第一周':
            for item in base_df[col].dropna():
                if isinstance(item, str) and item not in ['早餐', '午餐', '晚餐', '第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天']:
                    ingredients_set.add(item)
                    dishes_set.add(item)
    
    # 从每日厨房餐单提取
    print("从每日厨房餐单提取数据...")
    for col in daily_df.columns:
        if col != 'Unnamed: 0':
            for item in daily_df[col].dropna():
                if isinstance(item, str) and item not in ['早餐', '午餐', '晚餐', '禁忌']:
                    ingredients_set.add(item)
                    dishes_set.add(item)
    
    print(f"\n提取结果:")
    print(f"食材数量: {len(ingredients_set)}")
    print(f"前10个食材: {list(ingredients_set)[:10]}")
    print(f"菜品数量: {len(dishes_set)}")
    print(f"前10个菜品: {list(dishes_set)[:10]}")
    
    print("\nExcel数据读取和提取成功！")
    
except Exception as e:
    print(f"读取Excel文件失败: {e}")
    import traceback
    traceback.print_exc()

print("脚本执行完成！")
