from app import app, db
from models.user import User

with app.app_context():
    # 检查数据库连接
    try:
        # 尝试执行一个简单的查询
        db.session.execute('SELECT 1')
        print('数据库连接成功')
        
        # 检查用户表是否存在
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if inspector.has_table('users'):
            print('用户表存在')
            
            # 检查admin用户是否存在
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print(f'admin用户存在: {admin_user.username}, 角色: {admin_user.role}')
                
                # 测试密码验证
                from werkzeug.security import check_password_hash
                password_correct = check_password_hash(admin_user.password_hash, 'admin123')
                print(f'密码验证结果: {password_correct}')
                
                if not password_correct:
                    print('密码错误，正在重置密码...')
                    from werkzeug.security import generate_password_hash
                    admin_user.password_hash = generate_password_hash('admin123')
                    db.session.commit()
                    print('密码重置成功: admin123')
            else:
                print('admin用户不存在，正在创建...')
                from werkzeug.security import generate_password_hash
                admin_user = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()
                print('admin用户创建成功: admin/admin123')
        else:
            print('用户表不存在')
    except Exception as e:
        print(f'数据库连接失败: {e}')
