#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的测试数据生成脚本
直接连接数据库，不通过Flask应用
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
from datetime import datetime

print("开始生成简单测试数据...")

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySQL',
    'database': 'meal_system'
}


def create_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("成功连接到数据库")
            return connection
    except Error as e:
        print(f"连接数据库失败: {e}")
        return None


def execute_query(connection, query, data=None):
    """执行SQL查询"""
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print(f"查询执行成功: {query[:50]}...")
        return cursor
    except Error as e:
        print(f"执行查询失败: {e}")
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()


def check_table_exists(connection, table_name):
    """检查表是否存在"""
    query = f"SHOW TABLES LIKE '{table_name}'"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchone() is not None
        return result
    except Error as e:
        print(f"检查表是否存在失败: {e}")
        return False
    finally:
        if cursor:
            cursor.close()


def insert_suppliers(connection):
    """插入供应商数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM suppliers"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("供应商数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查供应商数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入供应商数据
    suppliers = [
        ("绿色蔬菜供应商", "张三", "13800138001", "北京市朝阳区农产品批发市场", "各类新鲜蔬菜、水果"),
        ("肉类供应商", "李四", "13900139001", "北京市海淀区肉类市场", "猪肉、牛肉、鸡肉、羊肉"),
        ("海鲜供应商", "王五", "13700137001", "北京市丰台区海鲜市场", "各类海鲜产品"),
        ("粮油供应商", "赵六", "13600136001", "北京市西城区粮油批发市场", "大米、面粉、食用油、调味品"),
        ("禽蛋供应商", "孙七", "13500135001", "北京市东城区禽蛋市场", "鸡蛋、鸭蛋、鹅蛋")
    ]
    
    query = """
    INSERT INTO suppliers (name, contact_person, contact_phone, address, products)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, suppliers)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个供应商")
    except Error as e:
        print(f"插入供应商数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_ingredients(connection):
    """插入食材数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM ingredients"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("食材数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查食材数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入食材数据
    ingredients = [
        ("西红柿", "蔬菜", "kg", 50, 10, 1, 5.5, "2026-12-31"),
        ("鸡蛋", "其他", "个", 200, 50, 5, 0.8, "2026-12-31"),
        ("猪肉", "肉类", "kg", 15, 5, 2, 35, "2026-12-31"),
        ("大米", "其他", "kg", 100, 20, 4, 4.5, "2026-12-31"),
        ("胡萝卜", "蔬菜", "kg", 30, 8, 1, 3.5, "2026-12-31"),
        ("鸡肉", "肉类", "kg", 20, 5, 2, 25, "2026-12-31"),
        ("白菜", "蔬菜", "kg", 40, 10, 1, 2.5, "2026-12-31"),
        ("豆腐", "其他", "块", 50, 15, 4, 2, "2026-12-31")
    ]
    
    query = """
    INSERT INTO ingredients (name, category, unit, current_stock, minimum_stock, supplier_id, price, expiry_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, ingredients)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个食材")
    except Error as e:
        print(f"插入食材数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_dishes(connection):
    """插入菜品数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM dishes"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("菜品数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查菜品数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入菜品数据
    dishes = [
        ("麻油猪肝", "肉菜", "传统月子餐，有助于产后恢复", "猪肝、麻油、生姜", 38, "active"),
        ("麻油猪肉片", "肉菜", "营养丰富的月子餐", "猪肉、麻油、生姜", 35, "active"),
        ("麻油红苋菜", "蔬菜", "富含铁质的蔬菜", "红苋菜、麻油、大蒜", 25, "active"),
        ("清炒牛心菜", "蔬菜", "清淡爽口的蔬菜", "牛心菜、大蒜、食用油", 20, "active"),
        ("麻油红菜头", "蔬菜", "营养丰富的根茎类蔬菜", "红菜头、麻油、生姜", 22, "active"),
        ("虫草花鸡汤", "汤品", "滋补养生汤", "鸡肉、虫草花、红枣", 45, "active"),
        ("小米粥", "主食", "营养丰富的杂粮粥", "小米、水", 15, "active"),
        ("南瓜百合小米粥", "主食", "香甜可口的养生粥", "南瓜、百合、小米", 18, "active"),
        ("薏仁粳米粥", "主食", "健脾利湿的养生粥", "薏仁、粳米、水", 16, "active"),
        ("小米粥里少放糯米", "主食", "适合产后食用的粥品", "小米、糯米、水", 17, "active")
    ]
    
    query = """
    INSERT INTO dishes (name, category, description, ingredients, price, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, dishes)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个菜品")
    except Error as e:
        print(f"插入菜品数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_menus(connection):
    """插入菜单数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM menus"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("菜单数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查菜单数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入菜单数据
    menus = [
        ("早餐菜单-周一", "周一的早餐安排", "breakfast", 45, "active"),
        ("早餐菜单-周二", "周二的早餐安排", "breakfast", 45, "active"),
        ("午餐菜单-周一", "周一的午餐安排", "lunch", 68, "active"),
        ("午餐菜单-周二", "周二的午餐安排", "lunch", 68, "active"),
        ("晚餐菜单-周一", "周一的晚餐安排", "dinner", 65, "active"),
        ("晚餐菜单-周二", "周二的晚餐安排", "dinner", 65, "active")
    ]
    
    query = """
    INSERT INTO menus (name, description, type, price, status)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, menus)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个菜单")
    except Error as e:
        print(f"插入菜单数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_menu_dishes(connection):
    """插入菜单菜品关联数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM menu_dishes"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("菜单菜品关联数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查菜单菜品关联数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入菜单菜品关联数据
    menu_dishes = [
        # 周一早餐
        (1, 7, 1),  # 小米粥
        (1, 3, 1),  # 麻油红苋菜
        # 周二早餐
        (2, 8, 1),  # 南瓜百合小米粥
        (2, 5, 1),  # 麻油红菜头
        # 周一午餐
        (3, 1, 1),  # 麻油猪肝
        (3, 4, 1),  # 清炒牛心菜
        (3, 9, 1),  # 薏仁粳米粥
        # 周二午餐
        (4, 2, 1),  # 麻油猪肉片
        (4, 4, 1),  # 清炒牛心菜
        (4, 7, 1),  # 小米粥
        # 周一晚餐
        (5, 1, 1),  # 麻油猪肝
        (5, 3, 1),  # 麻油红苋菜
        (5, 10, 1),  # 小米粥里少放糯米
        # 周二晚餐
        (6, 2, 1),  # 麻油猪肉片
        (6, 5, 1),  # 麻油红菜头
        (6, 8, 1)   # 南瓜百合小米粥
    ]
    
    query = """
    INSERT INTO menu_dishes (menu_id, dish_id, quantity)
    VALUES (%s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, menu_dishes)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个菜单菜品关联")
    except Error as e:
        print(f"插入菜单菜品关联数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_users(connection):
    """插入用户数据"""
    # 插入用户数据，使用IGNORE避免重复
    users = [
        ("employee1", "pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6", "employee"),
        ("customer1", "pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6", "customer"),
        ("customer2", "pbkdf2:sha256:150000$d2e3q4r5$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6", "customer")
    ]
    
    query = """
    INSERT IGNORE INTO users (username, password_hash, role)
    VALUES (%s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, users)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个用户")
    except Error as e:
        print(f"插入用户数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_employees(connection):
    """插入员工数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM employees"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("员工数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查员工数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入员工数据
    employees = [
        (None, "张经理", "经理", "13800138002", 8000, "2024-01-01", "本科", "5年管理经验", "优秀", "active"),
        (None, "李厨师", "厨师", "13800138003", 6000, "2024-02-01", "中专", "8年烹饪经验", "良好", "active"),
        (None, "王服务员", "服务员", "13800138004", 4000, "2024-03-01", "高中", "2年服务经验", "良好", "active")
    ]
    
    query = """
    INSERT INTO employees (user_id, name, position, contact, base_salary, joining_date, education, work_experience, work_performance, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, employees)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个员工")
    except Error as e:
        print(f"插入员工数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_customers(connection):
    """插入客户数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM customers"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("客户数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查客户数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 插入客户数据
    customers = [
        (None, "刘女士", 28, "女", "13800138005", "2025-01-01", "2025-01-02", "2025-01-31", "无", "喜欢清淡口味", "active"),
        (None, "张女士", 30, "女", "13800138006", "2025-01-05", "2025-01-06", "2025-02-05", "不吃辣", "喜欢喝汤", "active"),
        (None, "王女士", 26, "女", "13800138007", "2025-01-10", "2025-01-11", "2025-02-10", "无", "喜欢吃肉", "active")
    ]
    
    query = """
    INSERT INTO customers (user_id, name, age, gender, contact, delivery_date, check_in_date, check_out_date, dietary_restrictions, preferences, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, customers)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个客户")
    except Error as e:
        print(f"插入客户数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_customer_menus(connection):
    """插入客户菜单关联数据"""
    # 检查是否已有数据
    check_query = "SELECT COUNT(*) FROM customer_menus"
    cursor = connection.cursor()
    try:
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count > 0:
            print("客户菜单关联数据已存在，跳过插入")
            return
    except Error as e:
        print(f"检查客户菜单关联数据失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    # 查询实际的客户ID
    customer_ids = []
    query_customers = "SELECT id FROM customers"
    cursor = connection.cursor()
    try:
        cursor.execute(query_customers)
        customer_ids = [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"查询客户ID失败: {e}")
        return
    finally:
        if cursor:
            cursor.close()
    
    if not customer_ids:
        print("没有找到客户数据，跳过插入客户菜单关联")
        return
    
    # 插入客户菜单关联数据
    customer_menus = []
    
    # 为每个客户创建菜单关联
    for customer_id in customer_ids:
        for menu_id in range(1, 7):  # 菜单ID为1-6
            customer_menus.append((customer_id, menu_id, f"2025-01-0{menu_id}", "ordered"))
    
    query = """
    INSERT INTO customer_menus (customer_id, menu_id, order_date, status)
    VALUES (%s, %s, %s, %s)
    """
    
    cursor = connection.cursor()
    try:
        cursor.executemany(query, customer_menus)
        connection.commit()
        print(f"成功插入 {cursor.rowcount} 个客户菜单关联")
    except Error as e:
        print(f"插入客户菜单关联数据失败: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


def main():
    """主函数"""
    # 创建数据库连接
    connection = create_connection()
    if not connection:
        return
    
    try:
        # 按照依赖顺序插入数据
        insert_users(connection)
        insert_suppliers(connection)
        insert_ingredients(connection)
        insert_dishes(connection)
        insert_menus(connection)
        insert_menu_dishes(connection)
        insert_employees(connection)
        insert_customers(connection)
        insert_customer_menus(connection)
        
        print("\n测试数据生成完成！")
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            connection.close()
            print("数据库连接已关闭")


if __name__ == "__main__":
    main()
