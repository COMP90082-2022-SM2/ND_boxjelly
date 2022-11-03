
userpass = 'mysql://bcad2e6d9226f9:318b6978@us-cdbr-east-06.cleardb.net/heroku_f7c500f08d32a48'
server  = '127.0.0.1:3306'

dbname   = '/users'

socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

class Config(object):
    TESTING = False
    
# put them all together as a string that shows SQLAlchemy where the database is
class MysqlConfig(Config):
    SQLALCHEMY_DATABASE_URI  = userpass
    # SQLALCHEMY_DATABASE_URI = userpass + server + dbname # + socket
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class sqliteConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3' # sqlite3 users.sqlite3 .tables
    SQLALCHEMY_TRACK_MODIFICATIONS = False
