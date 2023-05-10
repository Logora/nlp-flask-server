from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
#from flasgger import Swagger
from config import Config
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import request, make_response, jsonify
from analysis import dummy
import threading
from keyphrase_extraction import extract_keyphrases
from debate_summary import get_keyphrases
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

import models

cache = Cache()
CORS(app)

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
  analysis = models.Analysis(uid=uid, name=name, status="pending", started_at=func.now())
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
    target_function = debate_summary_analysis
    args = (uid, documents, question)
  else:
    return make_response(jsonify({"success": False, "error": "Analysis name unknown"}), 404)

  # Start analysis thread
  analysis_thread = threading.Thread(target=target_function, name="Analysis", args=args)
  analysis_thread.start()

  return jsonify({"success": True, "data": { "uid": uid, "name": name }})


def keyphrase_extraction_analysis(uid, documents):
  json_analysis = extract_keyphrases(uid, documents)
  store_analysis(uid, "keyphrase_extraction", json_analysis)
  return True


def debate_summary_analysis(uid, documents, question):
  json_analysis = get_keyphrases(uid, documents, question)
  store_analysis(uid, "debate_summary", json_analysis)
  return True


def store_analysis(uid, name, result):
  # Store analysis result
  analysis = models.Analysis(uid=uid, name=name, status="done", content=result, ended_at=func.now())
  
  with app.app_context():
    db.session.merge(analysis)
    db.session.commit()


if __name__ == '__main__':
  app.run(debug=False, port=8000)