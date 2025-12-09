from app import create_app
from app.extensions import db
from app.models import User, Role, Permission
from app.models import Permissions

app = create_app()
with app.app_context():
    # db.drop_all()
    # db.create_all()

    # 创建权限
    permissions = {
        'user:read':Permission(name=Permissions.USER_READ, description='读取用户信息'),
        'user:write':Permission(name=Permissions.USER_WRITE, description='修改用户信息'),
        'admin:read':Permission(name=Permissions.ADMIN_READ, description='读取管理信息'),
        'admin:write':Permission(name=Permissions.ADMIN_WRITE, description='修改管理信息')
    }
    for perm in permissions.values():
        db.session.add(perm)

    # 创建角色并关联权限
    admin_role = Role(name='admin', description='系统管理员')
    admin_role.permissions = list(permissions.values())

    user_role = Role(name='user', description='普通用户')
    user_role.permissions = [permissions['user:read']]

    db.session.add(admin_role)
    db.session.add(user_role)

    #创建测试用户
    admin_user = User(username='admin', password='')
    admin_user.password = '123456'
    admin_user.roles = [admin_role]

    test_user = User(username='test', password='')
    test_user.password = '123456'
    test_user.roles = [user_role]

    db.session.add(admin_user)
    db.session.add(test_user)

    db.session.commit()
    print('初始化数据库完成！')

