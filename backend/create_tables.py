#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建数据库表结构
"""

import mysql.connector
from mysql.connector import Error

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


def execute_sql_file(connection, file_path):
    """执行SQL文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()
        
        # 分割SQL命令
        commands = sql_commands.split(';')
        
        cursor = connection.cursor()
        
        for command in commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    connection.commit()
                    print(f"执行SQL成功: {command[:50]}...")
                except Error as e:
                    print(f"执行SQL失败: {e}")
                    print(f"SQL命令: {command}")
                    connection.rollback()
        
        cursor.close()
        return True
    except Exception as e:
        print(f"执行SQL文件失败: {e}")
        return False


def main():
    """主函数"""
    # 创建数据库连接
    connection = create_connection()
    if not connection:
        return
    
    try:
        # 执行SQL文件
        execute_sql_file(connection, 'simple_create_tables.sql')
        print("\n表结构创建完成！")
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            connection.close()
            print("数据库连接已关闭")


if __name__ == "__main__":
    main()