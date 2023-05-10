from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
#from flasgger import Swagger
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from config import Config
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import request, make_response, jsonify
from analysis import dummy
import threading
from keyphrase_extraction import extract_keyphrases
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

from models import Analysis

cache = Cache()
CORS(app)

app.config['SWAGGER'] = {
    'title': 'Logora NLP',
    'description': 'A collection of tools to analyse collections of documents.',
    'version': '1.0.0',
    'uiversion': 3,
    'specs_route': '/docs/'
}
#swagger = Swagger(app)


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
  language = request.args.get('language')

  if not (uid and name):
    return make_response(jsonify({"success": False, "error": "Analysis identifier not provided"}), 422)

  documents = []
  body = request.json
  if "documents" in body:
    documents = body["documents"]
  else:
    return make_response(jsonify({"success": False, "error": "Missing documents in request body"}), 422)

  # Get or create Analysis object
  analysis = Analysis(uid=uid, name=name, status="pending", started_at=func.now())
  db.session.merge(analysis)
  db.session.commit()

  target_function = None
  args = ()

  if name == "test":
    content = dummy(request.json)
  elif name == "keyphrase_extraction":
    target_function = keyphrase_extraction_analysis
    args = (uid, documents)
  elif name == "debate_summary":
    question = request.args.get('question')
    target_function = keyphrase_extraction_analysis
    args = (uid, documents, question)
  else:
    return make_response(jsonify({"success": False, "error": "Analysis name unknown"}), 404)

  # Start analysis thread
  analysis_thread = threading.Thread(target=target_function, name="Analysis", args=args)
  analysis_thread.start()

  return jsonify({"success": True, "data": { "uid": uid, "name": name }})

def keyphrase_extraction_analysis(uid, documents):
  json_analysis = extract_keyphrases(uid, documents)

  # Store analysis result
  analysis = Analysis(uid, "keyphrase_extraction", json_analysis, "done")
  db.session.add(analysis)
  db.session.commit()
  return True

if __name__ == '__main__':
  app.run(debug=False, port=8000)