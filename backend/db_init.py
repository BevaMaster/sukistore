from flask import Flask
from models import db, User, Product
from auth import hash_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sukistore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password_hash=hash_password('admin123'), is_admin=True)
        db.session.add(admin)
    if not Product.query.first():
        p = Product(name='Contoh Produk', description='Produk percobaan', price=10000.0, stock=10)
        db.session.add(p)
    db.session.commit()
    print('Database init done')
