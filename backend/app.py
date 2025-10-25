from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Product, Order
from auth import verify_password, hash_password, generate_token, token_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sukistore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({'message':'username and password required'}),400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message':'username taken'}),400
    u = User(username=data['username'], password_hash=hash_password(data['password']))
    db.session.add(u)
    db.session.commit()
    token = generate_token(u)
    return jsonify({'token':token, 'username':u.username})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u = User.query.filter_by(username=data['username']).first()
    if not u or not verify_password(data['password'], u.password_hash):
        return jsonify({'message':'invalid credentials'}),401
    token = generate_token(u)
    return jsonify({'token':token, 'username':u.username})

@app.route('/api/products', methods=['GET','POST'])
@token_required
def products(current_user=None):
    if request.method == 'GET':
        items = Product.query.all()
        return jsonify([{'id':p.id,'name':p.name,'description':p.description,'price':p.price,'stock':p.stock} for p in items])
    if not current_user.is_admin:
        return jsonify({'message':'admin only'}),403
    data = request.json
    p = Product(name=data['name'], description=data['description'], price=data['price'], stock=data['stock'])
    db.session.add(p)
    db.session.commit()
    return jsonify({'message':'product created','id':p.id})

@app.route('/api/checkout', methods=['POST'])
@token_required
def checkout(current_user):
    data = request.json
    items = data.get('items', [])
    total = 0
    for i in items:
        p = Product.query.get(i['product_id'])
        if not p or p.stock < i['qty']:
            return jsonify({'message':f'not enough stock for {p.name}'}),400
        p.stock -= i['qty']
        total += p.price * i['qty']
    order = Order(user_id=current_user.id, total=total, items=str(items))
    db.session.add(order)
    db.session.commit()
    return jsonify({'message':'order placed','order_id':order.id,'total':total})

if __name__ == '__main__':
    app.run(debug=True)
