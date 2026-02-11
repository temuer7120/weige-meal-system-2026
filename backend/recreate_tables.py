from app import app, db

with app.app_context():
    # 删除所有表
    print('正在删除所有表...')
    db.drop_all()
    
    # 重新创建所有表
    print('正在重新创建所有表...')
    db.create_all()
    
    # 创建默认管理员用户
    print('正在创建默认管理员用户...')
    from models.user import User
    from werkzeug.security import generate_password_hash
    
    admin_user = User(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin_user)
    db.session.commit()
    
    print('表重新创建成功，默认管理员用户创建成功: admin/admin123')
