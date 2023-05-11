import pandas as pd
import spacy
from keyphrase_vectorizers import KeyphraseTfidfVectorizer
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

def get_keyphrases(uid, documents, question):
  stop_words = list(fr_stop) + ['oui', 'non']
  vectorizer = KeyphraseTfidfVectorizer(spacy_pipeline="fr_core_news_md",
                                      stop_words=stop_words,
                                      pos_pattern="<NOUN>*<ADJ>*")

  m = vectorizer.fit_transform(documents)

  phrases = get_top_keyphrases(10, vectorizer, m, question)

  json_analysis = build_json(phrases)
  return json_analysis

def get_top_keyphrases(number_phrases, vectorizer, tfidf, debate_question):
  candidate_keyphrases = sorted(list(zip(vectorizer.get_feature_names_out(), tfidf.sum(0).getA1())), key=lambda x: x[1], reverse=True)
  final_keyphrases = []

  for candidate in candidate_keyphrases:
    if len(final_keyphrases) >= number_phrases:
      break

    if candidate[0] not in debate_question.lower():
      final_keyphrases.append(candidate)

  return final_keyphrases

def build_json(keyphrases):
  analysis = {}
  keyphrase_objects = []
  for i, k in enumerate(keyphrases):
    keyphrase_objects.append({ "id": i, "name": k[0], "weight": k[1] })
  analysis['keyphrases'] = keyphrase_objects
  return analysis