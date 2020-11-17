class thongso:
    server = 'TANDAT_2909\DBSQL2019_01'
    database = 'QLGVDBDQG'
    username = 'sa'
    password = 'root'
    driver = 'ODBC+Driver+17+for+SQL+Server'
class Config(object):
    SQLALCHEMY_DATABASE_URI=str.format(f"mssql+pyodbc://{thongso.username}:{thongso.password}@{thongso.server}/{thongso.database}?driver={thongso.driver}")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '=xx08_xe2xd6o#$%x0cxadxad'
