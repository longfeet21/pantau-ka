from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
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
ma = Marshmallow(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class KA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor_ka = db.Column(db.String(10), nullable=False)
    tanggal = db.Column(db.Date, nullable=True)
    stasiun_id = db.Column(db.Integer, db.ForeignKey('stasiun.id'), nullable=True)
    stasiun_sekarang = db.relationship('Stasiun', backref=db.backref('daftarKA', lazy=True))
    masuk_stasiun = db.Column(db.Time, nullable=True)
    keluar_stasiun = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<KA %r>' % self.nomor_ka

class Stasiun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode_stasiun = db.Column(db.String(5), nullable=False, unique=True)
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


class KASchema(ma.Schema):
    class Meta:
        fields = ("nomor_ka", "tanggal", "stasiun_id", "masuk_stasiun", "keluar_stasiun", "status")

class StasiunSchema(ma.Schema):
    class Meta:
        fields = ("kode_stasiun", "nama_stasiun")

KA_schema = KASchema()
Stasiun_schema = StasiunSchema()
daftarKA_Schema = KASchema(many=True)
daftarStasiun_Schema = StasiunSchema(many=True)


@app.route("/ka", methods=['GET'])
def get_ka():
    semua_ka = KA.query.all()
    result = daftarKA_Schema.dump(semua_ka)
    return jsonify(result)

@app.route("/stasiun", methods=['GET'])
def get_stasiun():
    semua_stasiun = Stasiun.query.all()
    result = daftarStasiun_Schema.dump(semua_stasiun)
    return jsonify(result)

@app.route("/ka", methods=['POST'])
def tambah_ka():
    nomor = request.json['nomor_ka']
    # tanggal = request.json['tanggal']
    # stasiun_sekarang = request['stasiun_sekarang']
    # masuk_stasiun = request['masuk_stasiun']
    # keluar_stasiun = request['keluar_stasiun']
    status = request.json['status']
    
    ka_baru = KA(nomor_ka=nomor, status=status)

    db.session.add(ka_baru)
    db.session.commit()
    return KA_schema.jsonify(ka_baru)

@app.route("/stasiun", methods=['POST'])
def tambah_stasiun():
    kode = request.json['kode_stasiun']
    nama = request.json['nama_stasiun']
    
    stasiun_baru = Stasiun(kode_stasiun=kode, nama_stasiun=nama)

    db.session.add(stasiun_baru)
    db.session.commit()
    return Stasiun_schema.jsonify(stasiun_baru)

@app.route("/stasiun=<kode_stasiun>", methods=['GET'])
def detail_stasiun(kode_stasiun):
    stasiun = Stasiun.query.filter_by(kode_stasiun=kode_stasiun).first()
    result = Stasiun_schema.dump(stasiun)
    return jsonify(result)




@app.route("/update/id=<id>", methods=['POST'])
def ka_move(id):
    ka = KA.query.filter_by(id=id).first()

    stasiun = request.json['stasiun_id']
    tanggal = request.json['tanggal']
    masuk = request.json['masuk_stasiun']
    keluar = request.json['keluar_stasiun']

    ka.stasiun_id = stasiun
    ka.tanggal = tanggal
    ka.masuk_stasiun = masuk
    ka.keluar_stasiun = keluar

    # db.session.commit()
    return KA_schema.jsonify(ka)

# if __name__ == "__main__":
#     app.run(debug=True)
