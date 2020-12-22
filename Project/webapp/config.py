class thongso:
    server = 'localhost'
    database = 'dbmanagersoccer'
    username = 'root'
    password = 'Taonha@123'
    driver = 'utf8mb4'
class Config(object):
    #'mysql+pymysql://root:123456@localhost/saledbv1?charset=utf8'
    SQLALCHEMY_DATABASE_URI=str.format(f"mysql+pymysql://{thongso.username}:{thongso.password}@{thongso.server}/{thongso.database}?charset={thongso.driver}")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '=xx08_xe2xd6o#$%x0cxadxad'
    FLASK_ADMIN_FLUID_LAYOUT = True
    KEYPASS = "@blog"