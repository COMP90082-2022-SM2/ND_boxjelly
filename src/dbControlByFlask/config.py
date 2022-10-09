# make sure the username, password and database name are correct
# username = 'root'
# password = ''
# userpass = 'mysql+pymysql://' + username + ':' + password + '@'
username = 'b07a134d14b738'
host = 'us-cdbr-east-06.cleardb.net'
password = 'e9e9c4c8'
database = 'heroku_7fff4db897f6863'
userpass = 'mysql://b07a134d14b738:e9e9c4c8@us-cdbr-east-06.cleardb.net/heroku_7fff4db897f6863'
# keep this as is for a hosted website
server  = '127.0.0.1:3306'
# change to YOUR database name, with a slash added as shown
dbname   = '/users'

# this socket is going to be very different on a WINDOWS computer
# try 'C:/xampp/mysql/mysql.sock'
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
