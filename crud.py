from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_path = os.path.join(app.root_path, "test.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
    
# GET /test: List all records (READ)
@app.route('/test', methods=['GET'])
def get_all_records():
    records = Test.query.all()
    return jsonify([record.to_dict() for record in records]), 200

# GET /test/<id>: List record with that id (READ)
@app.route('/test/<int:id>', methods=['GET'])
def get_record(id):
    record = Test.query.get_or_404(id)
    return jsonify(record.to_dict()), 200

# POST /todos: create new record (CREATE)
@app.route('/test', methods=['POST'])
def create_record():
    data = request.get_json()
    new_record = Test(name=data['name'], age=data.get('age', 0))
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 200

# PUT /todos/<id>: update record with that id (UPDATE)
@app.route('/test/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    record = Test.query.get_or_404(id)
    record.name = data['name']
    record.age = data['age']
    db.session.commit()
    return jsonify(record.to_dict()), 200

# DELETE /todos/<id>: delete record with that id (DELETE)
@app.route('/test/<int:id>', methods=['DELETE'])
def delete_record(id):
    record = Test.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': f'record with id {id} has been deleted'}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port='5000')
