from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    models.init_app(app)
    return app

# app = create_app()
app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, 'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ma = Marshmallow(app)
db = SQLAlchemy(app)


# class UserModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(10), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

class KA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor_ka = db.Column(db.String(10), nullable=False)
    tanggal = db.Column(db.Date, nullable=False, default=datetime.utcnow().today().date)
    stasiun_id = db.Column(db.Integer, db.ForeignKey('stasiun.id'), nullable=False)
    stasiun_sekarang = db.relationship('Stasiun', backref=db.backref('daftarKA', lazy=True))
    masuk_stasiun = db.Column(db.Time, nullable=False, default=datetime.utcnow().today().timetz)
    keluar_stasiun = db.Column(db.Time, nullable=True, default=datetime.utcnow().today().timetz)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<KA %r>' % self.nomor_ka

class Stasiun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode_stasiun = db.Column(db.String(5), nullable=False)
    nama_stasiun = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Stasiun %r (%r)>' %(self.kode_stasiun, self.nama_stasiun)

class HistoryRangkaian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ka_id = db.Column(db.Integer, db.ForeignKey('KA.id'), nullable=False)
    ka = db.relationship('KA', lazy=True)
    stasiun_id = db.Column(db.Integer, db.ForeignKey('stasiun.id'), nullable=False)
    stasiun = db.relationship('Stasiun', lazy=True)
    tanggal = db.Column(db.Date, nullable=False, default=datetime.utcnow().today().date)
    masuk = db.Column(db.Time, nullable=False, default=datetime.utcnow().today().timetz)
    keluar = db.Column(db.Time, nullable=False, default=datetime.utcnow().today().timetz)
    status = db.Column(db.String(10), nullable=False)


@app.route("/")
def hello():
    return ""


if __name__ == "__main__":
    app.run(debug=True)
