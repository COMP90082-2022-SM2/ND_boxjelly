# make sure the username, password and database name are correct
username = 'root'
# project_admin
password = ''
# comp90082@@
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
# keep this as is for a hosted website
server  = '127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/test'

# this socket is going to be very different on a WINDOWS computer
# try 'C:/xampp/mysql/mysql.sock'
socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

class Config(object):
    TESTING = False
    
# put them all together as a string that shows SQLAlchemy where the database is
class MysqlConfig(Config):
    SQLALCHEMY_DATABASE_URI = userpass + server + dbname + socket
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class sqliteConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3' # sqlite3 users.sqlite3 .tables
    SQLALCHEMY_TRACK_MODIFICATIONS = False
