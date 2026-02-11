#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Excel文件导入数据到数据库
"""

import os
import sys
import pandas as pd
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.supplier import Supplier
from models.ingredient import Ingredient
from models.dish import Dish
from models.menu import Menu, MenuDish
from models.customer import Customer


def import_suppliers():
    """导入供应商数据"""
    with app.app_context():
        # 检查是否已有供应商数据
        if Supplier.query.first():
            print("供应商数据已存在，跳过导入")
            return
        
        # 创建默认供应商
        suppliers = [
            Supplier(name="绿色蔬菜供应商", contact_person="张三", contact_phone="13800138001", address="北京市朝阳区", products="各类新鲜蔬菜"),
            Supplier(name="肉类供应商", contact_person="李四", contact_phone="13900139001", address="北京市海淀区", products="猪肉、牛肉、鸡肉等"),
            Supplier(name="海鲜供应商", contact_person="王五", contact_phone="13700137001", address="北京市丰台区", products="各类海鲜产品"),
            Supplier(name="粮油供应商", contact_person="赵六", contact_phone="13600136001", address="北京市西城区", products="大米、面粉、食用油等"),
            Supplier(name="禽蛋供应商", contact_person="孙七", contact_phone="13500135001", address="北京市东城区", products="鸡蛋、鸭蛋等")
        ]
        
        db.session.add_all(suppliers)
        db.session.commit()
        print(f"成功导入 {len(suppliers)} 个供应商")


def import_ingredients():
    """导入食材数据"""
    with app.app_context():
        # 检查是否已有食材数据
        if Ingredient.query.first():
            print("食材数据已存在，跳过导入")
            return
        
        # 从Excel文件中提取食材信息
        # 这里我们从餐单中提取食材名称
        base_menu_path = "../基础餐单2025.xlsx"
        daily_menu_path = "../每日厨房餐单2025.xlsx"
        
        # 读取Excel文件
        base_df = pd.read_excel(base_menu_path)
        daily_df = pd.read_excel(daily_menu_path)
        
        # 提取食材名称
        ingredients_set = set()
        
        # 从基础餐单提取
        for col in base_df.columns:
            if col != '第一周':
                for item in base_df[col].dropna():
                    if isinstance(item, str) and item not in ['早餐', '午餐', '晚餐', '第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天']:
                        # 提取食材名称（简单处理，实际可能需要更复杂的解析）
                        ingredients_set.add(item)
        
        # 从每日厨房餐单提取
        for col in daily_df.columns:
            if col != 'Unnamed: 0':
                for item in daily_df[col].dropna():
                    if isinstance(item, str) and item not in ['早餐', '午餐', '晚餐', '禁忌']:
                        ingredients_set.add(item)
        
        # 获取供应商
        suppliers = Supplier.query.all()
        if not suppliers:
            print("请先导入供应商数据")
            return
        
        # 创建食材数据
        ingredients = []
        categories = ['蔬菜', '肉类', '其他']
        
        for i, ingredient_name in enumerate(ingredients_set):
            category = categories[i % len(categories)]
            supplier = suppliers[i % len(suppliers)]
            
            ingredient = Ingredient(
                name=ingredient_name,
                category=category,
                unit="份",
                current_stock=100,
                minimum_stock=20,
                supplier_id=supplier.id,
                price=10.0,
                expiry_date=datetime(2026, 12, 31)
            )
            ingredients.append(ingredient)
        
        db.session.add_all(ingredients)
        db.session.commit()
        print(f"成功导入 {len(ingredients)} 个食材")


def import_dishes():
    """导入菜品数据"""
    with app.app_context():
        # 检查是否已有菜品数据
        if Dish.query.first():
            print("菜品数据已存在，跳过导入")
            return
        
        # 从Excel文件中提取菜品信息
        base_menu_path = "../基础餐单2025.xlsx"
        daily_menu_path = "../每日厨房餐单2025.xlsx"
        
        # 读取Excel文件
        base_df = pd.read_excel(base_menu_path)
        daily_df = pd.read_excel(daily_menu_path)
        
        # 提取菜品名称
        dishes_set = set()
        
        # 从基础餐单提取
        for col in base_df.columns:
            if col != '第一周':
                for item in base_df[col].dropna():
                    if isinstance(item, str) and item not in ['早餐', '午餐', '晚餐', '第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天']:
                        dishes_set.add(item)
        
        # 从每日厨房餐单提取
        for col in daily_df.columns:
            if col != 'Unnamed: 0':
                for item in daily_df[col].dropna():
                    if isinstance(item, str) and item not in ['早餐', '午餐', '晚餐', '禁忌']:
                        dishes_set.add(item)
        
        # 创建菜品数据
        dishes = []
        categories = ['汤品', '点心', '肉菜', '蔬菜']
        
        for i, dish_name in enumerate(dishes_set):
            category = categories[i % len(categories)]
            
            dish = Dish(
                name=dish_name,
                category=category,
                description=f"{dish_name}的描述",
                ingredients=f"{dish_name}的食材",
                price=20.0,
                status="active"
            )
            dishes.append(dish)
        
        db.session.add_all(dishes)
        db.session.commit()
        print(f"成功导入 {len(dishes)} 个菜品")


def import_menus():
    """导入菜单数据"""
    with app.app_context():
        # 检查是否已有菜单数据
        if Menu.query.first():
            print("菜单数据已存在，跳过导入")
            return
        
        # 从Excel文件中提取菜单信息
        base_menu_path = "../基础餐单2025.xlsx"
        
        # 读取Excel文件
        base_df = pd.read_excel(base_menu_path)
        
        # 获取所有菜品
        all_dishes = Dish.query.all()
        dish_dict = {dish.name: dish.id for dish in all_dishes}
        
        # 创建菜单
        menus = []
        menu_dishes = []
        
        # 从基础餐单提取菜单信息
        meal_types = ['breakfast', 'lunch', 'dinner']
        meal_type_map = {'早餐': 'breakfast', '午餐': 'lunch', '晚餐': 'dinner'}
        
        # 遍历每一列（每天）
        for col_idx, col in enumerate(base_df.columns):
            if col != '第一周':
                # 遍历每一行（每个时段的菜品）
                current_meal_type = None
                for row_idx, item in enumerate(base_df[col].dropna()):
                    if isinstance(item, str):
                        if item in ['早餐', '午餐', '晚餐']:
                            current_meal_type = meal_type_map.get(item)
                            # 创建菜单
                            menu = Menu(
                                name=f"{col}_{item}",
                                description=f"{col}的{item}",
                                type=current_meal_type,
                                price=50.0,
                                status="active"
                            )
                            menus.append(menu)
                        elif current_meal_type and item not in ['第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天']:
                            # 添加菜品到菜单
                            if item in dish_dict:
                                menu_dish = MenuDish(
                                    menu_id=len(menus),  # 临时ID，后续会自动更新
                                    dish_id=dish_dict[item],
                                    quantity=1
                                )
                                menu_dishes.append(menu_dish)
        
        # 先添加菜单
        db.session.add_all(menus)
        db.session.flush()  # 获取菜单的实际ID
        
        # 更新菜单菜品关联的menu_id
        for i, md in enumerate(menu_dishes):
            md.menu_id = menus[i // 3].id  # 假设每个菜单有3个菜品
        
        # 添加菜单菜品关联
        db.session.add_all(menu_dishes)
        db.session.commit()
        print(f"成功导入 {len(menus)} 个菜单和 {len(menu_dishes)} 个菜单菜品关联")


def main():
    """主函数"""
    print("开始导入Excel数据到数据库...")
    
    # 按照依赖顺序导入数据
    import_suppliers()
    import_ingredients()
    import_dishes()
    import_menus()
    
    print("数据导入完成！")


if __name__ == "__main__":
    main()
