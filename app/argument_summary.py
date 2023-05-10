import pandas as pd

def get_summary(uid, documents, question):
  return []

def build_json(arguments):
  analysis = []
  for i, k in enumerate(arguments):
    analysis.append({ "id": i, "name": k[0], "weight": k[1] })
  return analysis