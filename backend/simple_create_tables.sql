-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS meal_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE meal_system;

-- 创建供应商表
CREATE TABLE IF NOT EXISTS suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(50) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    address TEXT,
    products TEXT,
    rating DECIMAL(3, 1) DEFAULT 0
);

-- 创建食材表
CREATE TABLE IF NOT EXISTS ingredients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    current_stock DECIMAL(10, 2) DEFAULT 0,
    minimum_stock DECIMAL(10, 2) DEFAULT 0,
    supplier_id INT,
    price DECIMAL(10, 2),
    expiry_date DATE,
    nutrition_info TEXT,
    calories DECIMAL(8, 2),
    restrictions TEXT,
    purchaser VARCHAR(50),
    origin TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- 创建菜品表
CREATE TABLE IF NOT EXISTS dishes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    ingredients TEXT,
    calories INT,
    price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'active'
);

-- 创建菜单表
CREATE TABLE IF NOT EXISTS menus (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,
    price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建菜单菜品关联表
CREATE TABLE IF NOT EXISTS menu_dishes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    dish_id INT NOT NULL,
    quantity INT DEFAULT 1,
    FOREIGN KEY (menu_id) REFERENCES menus(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认管理员用户
INSERT IGNORE INTO users (username, password_hash, role) VALUES ('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin');

-- 创建员工表
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    contact VARCHAR(100),
    base_salary DECIMAL(10, 2) NOT NULL,
    joining_date DATE NOT NULL,
    education TEXT,
    work_experience TEXT,
    work_performance TEXT,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建客户表
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(100),
    delivery_date DATE,
    check_in_date DATE,
    check_out_date DATE,
    dietary_restrictions TEXT,
    preferences TEXT,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建客户菜单关联表
CREATE TABLE IF NOT EXISTS customer_menus (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    menu_id INT NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'ordered',
    feedback TEXT,
    rating INT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (menu_id) REFERENCES menus(id)
);
