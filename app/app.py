from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from flasgger import Swagger
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

CORS(app)

app.config['SWAGGER'] = {
    'title': 'Logora NLP',
    'description': 'A collection of tools to analyse collections of documents.',
    'version': '1.0.0',
    'uiversion': 3,
    'specs_route': '/docs/'
}
swagger = Swagger(app)

@app.route('/')
def status():
  """Status endpoint.
    ---
    tags:
      - status
    responses:
      200:
        description: A success message
        schema:
          type: object
          properties:
            name:
              type: string
              description: App name.
              example: 'Logora NLP'
            status:
              type: string
              description: Status message.
              example: 'everything is allright'
  """
  return jsonify({"name": "Logora NLP", "status": "everything is allright"})

# Get analysis
@app.route('/analysis/<uid>', methods=['GET'])
def get_analysis(uid):
  """Get analysis.
    ---
    tags:
      - analysis
    parameters:
      - name: uid
        in: path
        type: string
        required: true
    responses:
      200:
        description: Analysis content
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Success message.
              example: 'true'
            data:
              type: object
              properties:
                uid:
                  type: string
                  description: Analysis unique identifier
                  example: '146464-364346'
                name:
                  type: string
                  description: Analysis name
                  example: 'keyword_extraction'
                content:
                  type: string
                  description: Analysis content in JSON format
                  example: '{}'
  """
  analysis = Analysis.query.filter_by(uid=uid).first()
  if analysis is None:
    return make_response(jsonify({"success": False, "error": "Object not found"}), 404)
  else:
    return jsonify({"success": True, "data": { "uid": analysis.uid, "name": analysis.name, "content": analysis.content }})

# Create analysis
@app.route('/analysis', methods=['POST'])
def create_analysis():
  """Create analysis.
    ---
    tags:
      - analysis
    parameters:
      - name: uid
        in: query
        type: string
        required: true
      - name: name
        in: query
        type: string
        enum: ['test']
        required: true
    responses:
      200:
        description: Analysis content
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Success message.
              example: 'true'
            data:
              type: object
              properties:
                uid:
                  type: string
                  description: Analysis unique identifier
                  example: '146464-364346'
                name:
                  type: string
                  description: Analysis name
                  example: 'keyword_extraction'
  """
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
  app.run(debug=False, port=8000)