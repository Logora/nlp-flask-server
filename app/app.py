from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_caching import Cache
import os
from dotenv import load_dotenv
from config import Config
import psycopg2
from models import Analysis
from db import db
from analysis import dummy

load_dotenv()

app = Flask(__name__)
cache = Cache()
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def status():
    return jsonify({"status": "everything is allright"})

# Get analysis
@app.route('/analysis/<uid>', methods=['GET'])
def get_analysis(uid):
  analysis = Analysis.query.filter_by(uid=uid).first()
  if analysis is None:
    return make_response(jsonify({"success": False, "error": "Object not found"}), 404)
  else:
    return jsonify({"success": True, "data": { "uid": analysis.uid, "name": analysis.name, "content": analysis.content }})

# Create analysis
@app.route('/analysis', methods=['POST'])
def create_analysis():
  uid = request.args.get('uid')
  name = request.args.get('name')
  if uid and name:
    status = "done"
    if name == "test":
      content = dummy(request.json)
      analysis = Analysis(uid, name, content, status)
      db.session.add(analysis)
      db.session.commit()
      return jsonify({"success": True, "data": { "uid": analysis.uid, "name": analysis.name }})
    else:
      return make_response(jsonify({"success": False, "error": "Analysis name unknown"}), 404)
  else:
    return make_response(jsonify({"success": False, "error": "Analysis identifier not provided"}), 422)

if __name__ == '__main__':
  app.run(debug=True, port=8000)