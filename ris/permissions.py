from flaskext.principal import RoleNeed, Permission

admin_role = RoleNeed('admin')
user_role = RoleNeed('user')

admin_permission = Permission(admin_role)
user_permission = Permission(user_role)

