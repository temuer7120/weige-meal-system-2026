#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成测试数据并添加到数据库
按照依赖顺序：用户 → 供应商 → 食材 → 菜品 → 菜单 → 菜单菜品关联 → 员工 → 客户 → 客户菜单关联
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("开始生成测试数据...")

# 导入必要的模块
try:
    from app import app, db
    print("成功导入app和db")
except Exception as e:
    print(f"导入app失败: {e}")
    sys.exit(1)

# 导入模型
try:
    from models.user import User
    from models.supplier import Supplier
    from models.ingredient import Ingredient
    from models.dish import Dish
    from models.menu import Menu, MenuDish, CustomerMenu
    from models.employee import Employee
    from models.customer import Customer
    print("成功导入所有模型")
except Exception as e:
    print(f"导入模型失败: {e}")
    sys.exit(1)


def generate_users():
    """生成用户测试数据"""
    with app.app_context():
        # 检查是否已有用户数据
        if User.query.first():
            print("用户数据已存在，跳过生成")
            return User.query.all()
        
        # 创建用户数据
        users = [
            User(
                username="admin",
                password_hash="pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
                role="admin"
            ),
            User(
                username="employee1",
                password_hash="pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
                role="employee"
            ),
            User(
                username="customer1",
                password_hash="pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
                role="customer"
            ),
            User(
                username="customer2",
                password_hash="pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
                role="customer"
            )
        ]
        
        db.session.add_all(users)
        db.session.commit()
        print(f"成功生成 {len(users)} 个用户")
        return users


def generate_suppliers():
    """生成供应商测试数据"""
    with app.app_context():
        # 检查是否已有供应商数据
        if Supplier.query.first():
            print("供应商数据已存在，跳过生成")
            return Supplier.query.all()
        
        # 创建供应商数据
        suppliers = [
            Supplier(
                name="绿色蔬菜供应商",
                contact_person="张三",
                contact_phone="13800138001",
                address="北京市朝阳区农产品批发市场",
                products="各类新鲜蔬菜、水果"
            ),
            Supplier(
                name="肉类供应商",
                contact_person="李四",
                contact_phone="13900139001",
                address="北京市海淀区肉类市场",
                products="猪肉、牛肉、鸡肉、羊肉"
            ),
            Supplier(
                name="海鲜供应商",
                contact_person="王五",
                contact_phone="13700137001",
                address="北京市丰台区海鲜市场",
                products="各类海鲜产品"
            ),
            Supplier(
                name="粮油供应商",
                contact_person="赵六",
                contact_phone="13600136001",
                address="北京市西城区粮油批发市场",
                products="大米、面粉、食用油、调味品"
            ),
            Supplier(
                name="禽蛋供应商",
                contact_person="孙七",
                contact_phone="13500135001",
                address="北京市东城区禽蛋市场",
                products="鸡蛋、鸭蛋、鹅蛋"
            )
        ]
        
        db.session.add_all(suppliers)
        db.session.commit()
        print(f"成功生成 {len(suppliers)} 个供应商")
        return suppliers


def generate_ingredients(suppliers):
    """生成食材测试数据"""
    with app.app_context():
        # 检查是否已有食材数据
        if Ingredient.query.first():
            print("食材数据已存在，跳过生成")
            return Ingredient.query.all()
        
        # 创建食材数据
        ingredients = [
            # 蔬菜类
            Ingredient(
                name="西红柿",
                category="蔬菜",
                unit="kg",
                current_stock=50,
                minimum_stock=10,
                supplier_id=suppliers[0].id,
                price=5.5,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="鸡蛋",
                category="其他",
                unit="个",
                current_stock=200,
                minimum_stock=50,
                supplier_id=suppliers[4].id,
                price=0.8,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="猪肉",
                category="肉类",
                unit="kg",
                current_stock=15,
                minimum_stock=5,
                supplier_id=suppliers[1].id,
                price=35,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="大米",
                category="其他",
                unit="kg",
                current_stock=100,
                minimum_stock=20,
                supplier_id=suppliers[3].id,
                price=4.5,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="胡萝卜",
                category="蔬菜",
                unit="kg",
                current_stock=30,
                minimum_stock=8,
                supplier_id=suppliers[0].id,
                price=3.5,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="鸡肉",
                category="肉类",
                unit="kg",
                current_stock=20,
                minimum_stock=5,
                supplier_id=suppliers[1].id,
                price=25,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="白菜",
                category="蔬菜",
                unit="kg",
                current_stock=40,
                minimum_stock=10,
                supplier_id=suppliers[0].id,
                price=2.5,
                expiry_date=datetime(2026, 12, 31)
            ),
            Ingredient(
                name="豆腐",
                category="其他",
                unit="块",
                current_stock=50,
                minimum_stock=15,
                supplier_id=suppliers[3].id,
                price=2,
                expiry_date=datetime(2026, 12, 31)
            )
        ]
        
        db.session.add_all(ingredients)
        db.session.commit()
        print(f"成功生成 {len(ingredients)} 个食材")
        return ingredients


def generate_dishes():
    """生成菜品测试数据"""
    with app.app_context():
        # 检查是否已有菜品数据
        if Dish.query.first():
            print("菜品数据已存在，跳过生成")
            return Dish.query.all()
        
        # 创建菜品数据
        dishes = [
            # 肉菜
            Dish(
                name="麻油猪肝",
                category="肉菜",
                description="传统月子餐，有助于产后恢复",
                ingredients="猪肝、麻油、生姜",
                price=38,
                status="active"
            ),
            Dish(
                name="麻油猪肉片",
                category="肉菜",
                description="营养丰富的月子餐",
                ingredients="猪肉、麻油、生姜",
                price=35,
                status="active"
            ),
            # 蔬菜
            Dish(
                name="麻油红苋菜",
                category="蔬菜",
                description="富含铁质的蔬菜",
                ingredients="红苋菜、麻油、大蒜",
                price=25,
                status="active"
            ),
            Dish(
                name="清炒牛心菜",
                category="蔬菜",
                description="清淡爽口的蔬菜",
                ingredients="牛心菜、大蒜、食用油",
                price=20,
                status="active"
            ),
            Dish(
                name="麻油红菜头",
                category="蔬菜",
                description="营养丰富的根茎类蔬菜",
                ingredients="红菜头、麻油、生姜",
                price=22,
                status="active"
            ),
            # 汤品
            Dish(
                name="虫草花鸡汤",
                category="汤品",
                description="滋补养生汤",
                ingredients="鸡肉、虫草花、红枣",
                price=45,
                status="active"
            ),
            # 主食
            Dish(
                name="小米粥",
                category="主食",
                description="营养丰富的杂粮粥",
                ingredients="小米、水",
                price=15,
                status="active"
            ),
            Dish(
                name="南瓜百合小米粥",
                category="主食",
                description="香甜可口的养生粥",
                ingredients="南瓜、百合、小米",
                price=18,
                status="active"
            ),
            Dish(
                name="薏仁粳米粥",
                category="主食",
                description="健脾利湿的养生粥",
                ingredients="薏仁、粳米、水",
                price=16,
                status="active"
            ),
            Dish(
                name="小米粥里少放糯米",
                category="主食",
                description="适合产后食用的粥品",
                ingredients="小米、糯米、水",
                price=17,
                status="active"
            )
        ]
        
        db.session.add_all(dishes)
        db.session.commit()
        print(f"成功生成 {len(dishes)} 个菜品")
        return dishes


def generate_menus(dishes):
    """生成菜单测试数据"""
    with app.app_context():
        # 检查是否已有菜单数据
        if Menu.query.first():
            print("菜单数据已存在，跳过生成")
            return Menu.query.all(), MenuDish.query.all()
        
        # 创建菜单数据
        menus = [
            # 早餐菜单
            Menu(
                name="早餐菜单-周一",
                description="周一的早餐安排",
                type="breakfast",
                price=45,
                status="active"
            ),
            Menu(
                name="早餐菜单-周二",
                description="周二的早餐安排",
                type="breakfast",
                price=45,
                status="active"
            ),
            # 午餐菜单
            Menu(
                name="午餐菜单-周一",
                description="周一的午餐安排",
                type="lunch",
                price=68,
                status="active"
            ),
            Menu(
                name="午餐菜单-周二",
                description="周二的午餐安排",
                type="lunch",
                price=68,
                status="active"
            ),
            # 晚餐菜单
            Menu(
                name="晚餐菜单-周一",
                description="周一的晚餐安排",
                type="dinner",
                price=65,
                status="active"
            ),
            Menu(
                name="晚餐菜单-周二",
                description="周二的晚餐安排",
                type="dinner",
                price=65,
                status="active"
            )
        ]
        
        # 添加菜单
        db.session.add_all(menus)
        db.session.flush()  # 获取菜单的实际ID
        
        # 创建菜单菜品关联
        menu_dishes = []
        
        # 周一早餐
        menu_dishes.append(MenuDish(menu_id=menus[0].id, dish_id=dishes[6].id, quantity=1))  # 小米粥
        menu_dishes.append(MenuDish(menu_id=menus[0].id, dish_id=dishes[2].id, quantity=1))  # 麻油红苋菜
        
        # 周二早餐
        menu_dishes.append(MenuDish(menu_id=menus[1].id, dish_id=dishes[7].id, quantity=1))  # 南瓜百合小米粥
        menu_dishes.append(MenuDish(menu_id=menus[1].id, dish_id=dishes[4].id, quantity=1))  # 麻油红菜头
        
        # 周一午餐
        menu_dishes.append(MenuDish(menu_id=menus[2].id, dish_id=dishes[0].id, quantity=1))  # 麻油猪肝
        menu_dishes.append(MenuDish(menu_id=menus[2].id, dish_id=dishes[3].id, quantity=1))  # 清炒牛心菜
        menu_dishes.append(MenuDish(menu_id=menus[2].id, dish_id=dishes[8].id, quantity=1))  # 薏仁粳米粥
        
        # 周二午餐
        menu_dishes.append(MenuDish(menu_id=menus[3].id, dish_id=dishes[1].id, quantity=1))  # 麻油猪肉片
        menu_dishes.append(MenuDish(menu_id=menus[3].id, dish_id=dishes[3].id, quantity=1))  # 清炒牛心菜
        menu_dishes.append(MenuDish(menu_id=menus[3].id, dish_id=dishes[6].id, quantity=1))  # 小米粥
        
        # 周一晚餐
        menu_dishes.append(MenuDish(menu_id=menus[4].id, dish_id=dishes[0].id, quantity=1))  # 麻油猪肝
        menu_dishes.append(MenuDish(menu_id=menus[4].id, dish_id=dishes[2].id, quantity=1))  # 麻油红苋菜
        menu_dishes.append(MenuDish(menu_id=menus[4].id, dish_id=dishes[9].id, quantity=1))  # 小米粥里少放糯米
        
        # 周二晚餐
        menu_dishes.append(MenuDish(menu_id=menus[5].id, dish_id=dishes[1].id, quantity=1))  # 麻油猪肉片
        menu_dishes.append(MenuDish(menu_id=menus[5].id, dish_id=dishes[4].id, quantity=1))  # 麻油红菜头
        menu_dishes.append(MenuDish(menu_id=menus[5].id, dish_id=dishes[7].id, quantity=1))  # 南瓜百合小米粥
        
        # 添加菜单菜品关联
        db.session.add_all(menu_dishes)
        db.session.commit()
        print(f"成功生成 {len(menus)} 个菜单和 {len(menu_dishes)} 个菜单菜品关联")
        return menus, menu_dishes


def generate_employees(users):
    """生成员工测试数据"""
    with app.app_context():
        # 检查是否已有员工数据
        if Employee.query.first():
            print("员工数据已存在，跳过生成")
            return Employee.query.all()
        
        # 创建员工数据
        employees = [
            Employee(
                user_id=users[1].id,  # employee1
                name="张经理",
                position="经理",
                contact="13800138002",
                base_salary=8000,
                joining_date=datetime(2024, 1, 1),
                education="本科",
                work_experience="5年管理经验",
                work_performance="优秀",
                status="active"
            ),
            Employee(
                name="李厨师",
                position="厨师",
                contact="13800138003",
                base_salary=6000,
                joining_date=datetime(2024, 2, 1),
                education="中专",
                work_experience="8年烹饪经验",
                work_performance="良好",
                status="active"
            ),
            Employee(
                name="王服务员",
                position="服务员",
                contact="13800138004",
                base_salary=4000,
                joining_date=datetime(2024, 3, 1),
                education="高中",
                work_experience="2年服务经验",
                work_performance="良好",
                status="active"
            )
        ]
        
        db.session.add_all(employees)
        db.session.commit()
        print(f"成功生成 {len(employees)} 个员工")
        return employees


def generate_customers(users):
    """生成客户测试数据"""
    with app.app_context():
        # 检查是否已有客户数据
        if Customer.query.first():
            print("客户数据已存在，跳过生成")
            return Customer.query.all()
        
        # 创建客户数据
        customers = [
            Customer(
                user_id=users[2].id,  # customer1
                name="刘女士",
                age=28,
                gender="女",
                contact="13800138005",
                delivery_date=datetime(2025, 1, 1),
                check_in_date=datetime(2025, 1, 2),
                check_out_date=datetime(2025, 1, 31),
                dietary_restrictions="无",
                preferences="喜欢清淡口味",
                status="active"
            ),
            Customer(
                user_id=users[3].id,  # customer2
                name="张女士",
                age=30,
                gender="女",
                contact="13800138006",
                delivery_date=datetime(2025, 1, 5),
                check_in_date=datetime(2025, 1, 6),
                check_out_date=datetime(2025, 2, 5),
                dietary_restrictions="不吃辣",
                preferences="喜欢喝汤",
                status="active"
            ),
            Customer(
                name="王女士",
                age=26,
                gender="女",
                contact="13800138007",
                delivery_date=datetime(2025, 1, 10),
                check_in_date=datetime(2025, 1, 11),
                check_out_date=datetime(2025, 2, 10),
                dietary_restrictions="无",
                preferences="喜欢吃肉",
                status="active"
            )
        ]
        
        db.session.add_all(customers)
        db.session.commit()
        print(f"成功生成 {len(customers)} 个客户")
        return customers


def generate_customer_menus(customers, menus):
    """生成客户菜单关联测试数据"""
    with app.app_context():
        # 检查是否已有客户菜单关联数据
        if CustomerMenu.query.first():
            print("客户菜单关联数据已存在，跳过生成")
            return CustomerMenu.query.all()
        
        # 创建客户菜单关联数据
        customer_menus = []
        
        # 为每个客户创建菜单关联
        for i, customer in enumerate(customers):
            for j, menu in enumerate(menus):
                customer_menus.append(
                    CustomerMenu(
                        customer_id=customer.id,
                        menu_id=menu.id,
                        order_date=datetime(2025, 1, 1 + j),
                        status="ordered"
                    )
                )
        
        db.session.add_all(customer_menus)
        db.session.commit()
        print(f"成功生成 {len(customer_menus)} 个客户菜单关联")
        return customer_menus


def main():
    """主函数"""
    print("开始生成测试数据...")
    
    # 按照依赖顺序生成数据
    users = generate_users()
    suppliers = generate_suppliers()
    ingredients = generate_ingredients(suppliers)
    dishes = generate_dishes()
    menus, menu_dishes = generate_menus(dishes)
    employees = generate_employees(users)
    customers = generate_customers(users)
    customer_menus = generate_customer_menus(customers, menus)
    
    print("\n测试数据生成完成！")
    print(f"用户数量: {len(users)}")
    print(f"供应商数量: {len(suppliers)}")
    print(f"食材数量: {len(ingredients)}")
    print(f"菜品数量: {len(dishes)}")
    print(f"菜单数量: {len(menus)}")
    print(f"菜单菜品关联数量: {len(menu_dishes)}")
    print(f"员工数量: {len(employees)}")
    print(f"客户数量: {len(customers)}")
    print(f"客户菜单关联数量: {len(customer_menus)}")


if __name__ == "__main__":
    main()
