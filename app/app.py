from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from flasgger import Swagger
from config import Config
import psycopg
import time
from flask_sqlalchemy import SQLAlchemy
from flask import request, make_response, jsonify
from analysis import dummy
import threading
from keyphrase_extraction import get_keyphrases
from argument_summary import get_summary
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

import models

cache = Cache()
CORS(app)

swagger = Swagger(app)

@app.route('/')
def status():
  """Status endpoint.
    ---
    tags:
      - Status
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
              example: 'everything is alright'
  """
  return jsonify({"name": "Logora NLP", "status": "everything is alright"})

# Get analysis
@app.route('/analysis/<uid>', methods=['GET'])
def get_analysis(uid):
  """Get analysis.
    ---
    tags:
      - Analysis
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
                  example: 'keyphrase_extraction'
                content:
                  type: string
                  description: Analysis content in JSON format
                  example: '{}'
  """
  analysis = db.session.query(models.Analysis).filter_by(uid=uid).first()
  if analysis is None:
    return make_response(jsonify({"success": False, "error": "Object not found"}), 404)
  else:
    return jsonify({"success": True, "data": analysis.as_dict()})

# Create analysis
@app.route('/analysis', methods=['POST'])
def create_analysis():
  """Create analysis.
    ---
    tags:
      - Analysis
    parameters:
      - name: uid
        in: query
        type: string
        required: true
      - name: name
        in: query
        type: string
        enum: ['test', 'keyphrase_extraction', 'argument_summary']
        required: true
      - name: question
        in: query
        type: string
        required: false
      - name: language
        in: query
        type: string
        required: false
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
                  example: 'keyphrase_extraction'
  """
  uid = request.args.get('uid')
  name = request.args.get('name')
  language = request.args.get('language') or "fr"

  if not (uid and name):
    return make_response(jsonify({"success": False, "error": "Analysis identifier not provided"}), 422)

  documents = []
  body = request.json
  if "documents" in body:
    documents = body["documents"]
  else:
    return make_response(jsonify({"success": False, "error": "Missing documents in request body"}), 422)

  # Get or create Analysis object
  analysis = models.Analysis(uid=uid, name=name, status="pending", started_at=func.now())
  db.session.merge(analysis)
  db.session.commit()

  target_function = None
  args = ()

  if name == "test":
    content = dummy(request.json)
  elif name == "keyphrase_extraction":
    question = request.args.get('question')
    target_function = keyphrase_extraction_analysis
    args = (uid, documents, question)
  elif name == "argument_summary":
    question = request.args.get('question')
    target_function = argument_summary_analysis
    args = (uid, documents, question, language)
  else:
    return make_response(jsonify({"success": False, "error": "Analysis name unknown"}), 404)

  # Start analysis thread
  analysis_thread = threading.Thread(target=target_function, name="Analysis", args=args)
  analysis_thread.start()

  return jsonify({"success": True, "data": { "uid": uid, "name": name }})


def keyphrase_extraction_analysis(uid, documents, question):
  json_analysis = get_keyphrases(uid, documents, question)
  store_analysis(uid, "keyphrase_extraction", json_analysis)
  return True


def argument_summary_analysis(uid, documents, question, language):
  json_analysis = get_summary(uid, documents, question, language)
  store_analysis(uid, "argument_summary", json_analysis)
  return True


def store_analysis(uid, name, result):
  # Store analysis result
  analysis = models.Analysis(uid=uid, name=name, status="done", content=result, ended_at=func.now())
  
  with app.app_context():
    db.session.merge(analysis)
    db.session.commit()


if __name__ == '__main__':
  app.run(debug=False, port=8000)