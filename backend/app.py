from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)

with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'age' not in data or 'cpf' not in data:
        return jsonify({'message': 'Name, age and CPF are required'}), 400
    
    # Validar CPF único
    existing_user = User.query.filter_by(cpf=data['cpf']).first()
    if existing_user:
        return jsonify({'message': 'CPF already exists'}), 400
    
    new_user = User(name=data['name'], age=data['age'], cpf=data['cpf'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'age': new_user.age, 'cpf': new_user.cpf}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'age': u.age, 'cpf': u.cpf} for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'name': user.name, 'age': user.age, 'cpf': user.cpf})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if not data or 'name' not in data or 'age' not in data or 'cpf' not in data:
        return jsonify({'message': 'Name, age and CPF are required'}), 400
    
    # Validar CPF único (exceto para o próprio usuário)
    existing_user = User.query.filter_by(cpf=data['cpf']).first()
    if existing_user and existing_user.id != user_id:
        return jsonify({'message': 'CPF already exists'}), 400
    
    user.name = data['name']
    user.age = data['age']
    user.cpf = data['cpf']
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'age': user.age, 'cpf': user.cpf})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
