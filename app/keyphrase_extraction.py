import pandas as pd
import spacy
from keyphrase_vectorizers import KeyphraseTfidfVectorizer
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from sklearn.feature_extraction.text import CountVectorizer

def get_keyphrases(uid, documents, question):
  stop_words = list(fr_stop) + ['oui', 'non']
  vectorizer = KeyphraseTfidfVectorizer(spacy_pipeline="fr_core_news_md",
                                      stop_words=stop_words,
                                      pos_pattern="<NOUN>*<ADJ>*")

  m = vectorizer.fit_transform(documents)

  phrases = get_top_keyphrases(10, vectorizer, m, question)

  keyphrase_frequency = get_keyphrase_frequency(phrases, documents)

  json_analysis = build_json(phrases, keyphrase_frequency)
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

def get_keyphrase_frequency(keyphrases, documents):
  terms = [t[0] for t in keyphrases]
  count_vectorizer = CountVectorizer(vocabulary=terms)
  m_count = count_vectorizer.fit_transform(documents)
  v_count = m_count.toarray().sum(axis=0)
  return v_count

def build_json(keyphrases, keyphrase_frequency):
  analysis = {}
  keyphrase_objects = []
  for i, k in enumerate(keyphrases):
    keyphrase_objects.append({ "id": i, "name": k[0], "frequency": int(keyphrase_frequency[i]) })
  analysis['keyphrases'] = keyphrase_objects
  return analysis