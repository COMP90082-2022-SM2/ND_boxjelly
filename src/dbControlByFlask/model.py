from exts import db


class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __repr__(self):
        return f'#{self.id}: {self.description} -> patient {self.patient_id}'

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'patient {self.id}'


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.INTEGER, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(80), nullable=False) # shouldn't be stored like this, should be encrypted first
#
#
# class CodeCountRecord(db.Model):
#     __tablename = 'codecountrecord'
#     id = db.Column(db.INTEGER, primary_key=True)
#     count = db.Column(db.INTEGER)
#     data = db.Column(db.DATE)
#     user = db.Column(db.ForeignKey('user.id'))