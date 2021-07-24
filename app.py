from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os


# Init app
app = Flask(__name__)
"""
@app.route('/',methods=['GET'])
def get():
  return jsonify({'msg': "hello world"})
"""
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Dynamixel Class/Model
class Dynamixel(db.Model):
  Motor_Key = db.Column(db.String(200), unique=True)
  Motor_Type = db.Column(db.String(100),unique =True)
  ID = db.Column(db.Integer, primary_key=True)
  PyPot_Support = db.Column(db.Boolean)
  SDK_Support = db.Column(db.Boolean)
  Wizard_Support = db.Column(db.Boolean)
  Location = db.Column(db.String(200))

  def __init__(self, Motor_Key,Motor_Type,ID,PyPot_Support,SDK_Support,Wizard_Support,Location):
    self.Motor_Key = Motor_Key
    self.Motor_Type = Motor_Type
    self.ID = ID
    self.PyPot_Support = PyPot_Support 
    self.SDK_Support =SDK_Support
    self.Wizard_Support = Wizard_Support
    self.Location = Location

# Dynamixel Schema
class DynamixelSchema(ma.Schema):
  class Meta:
    fields = ('Motor_Key', 'Motor_Type', 'ID', 'PyPot_Support', 'SDK_Support','Wizard_Support','Location')

# Init schema
dynamixel_schema = DynamixelSchema(strict=True)
dynamixels_schema = DynamixelSchema(many=True, strict=True)

# Create a entry
@app.route('/dynamixel', methods=['POST'])
def add_entry():
  Motor_Key = request.json['Motor_Key']
  Motor_Type = request.json['Motor_Type']
  ID =request.json['ID']
  PyPot_Support = request.json['PyPot_Support']
  SDK_Support = request.json['SDK_Support']
  Wizard_Support = request.json['Wizard_Support']
  Location = request.json['Location']

  new_entry = Dynamixel( Motor_Key,Motor_Type,ID,PyPot_Support,SDK_Support,Wizard_Support,Location)

  db.session.add(new_entry)
  db.session.commit()

  return dynamixel_schema.jsonify(new_entry)

# Get All Products
@app.route('/dynamixel', methods=['GET'])
def get_entrys():
  all_entrys = Dynamixel.query.all()
  result = dynamixels_schema.dump(all_entrys)
  return jsonify(result.data)


# Get Single Entry
@app.route('/dynamixel/<id>', methods=['GET'])
def get_entry(id):
  entry = Dynamixel.query.get(id)
  return dynamixel_schema.jsonify(entry)

# Update a entry
@app.route('/dynamixel/<id>', methods=['PUT'])
def update_entry(id):
  entry = Dynamixel.query.get(id)

  Motor_Key = request.json['Motor_Key']
  Motor_Type = request.json['Motor_Type']
  ID =request.json['ID']
  PyPot_Support = request.json['PyPot_Support']
  SDK_Support = request.json['SDK_Support']
  Wizard_Support = request.json['Wizard_Support']
  Location = request.json['Location']

  entry.Motor_Key = Motor_Key
  entry.Motor_Type = Motor_Type
  entry.ID = ID
  entry.PyPot_Support = PyPot_Support
  entry.SDK_Support = SDK_Support
  entry.Wizard_Support = Wizard_Support
  entry.Location = Location

  db.session.commit()

  return dynamixel_schema.jsonify(entry)



# Delete Entry
@app.route('/dynamixel/<id>', methods=['DELETE'])
def delete_entry(id):
  entry = Dynamixel.query.get(id)
  db.session.delete(entry)
  db.session.commit()

  return dynamixel_schema.jsonify(entry)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)