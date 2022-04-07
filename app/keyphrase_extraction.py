import pandas as pd
import spacy
from keyphrase_vectorizers import KeyphraseTfidfVectorizer

def extract_keyphrases(uid, documents):
  vectorizer = KeyphraseTfidfVectorizer(spacy_pipeline='fr_dep_news_trf',
                                        pos_pattern="<NOUN>(<ADP><DET><NOUN>|<ADP><NOUN>|<NOUN><ADJ>|<ADJ>|<NOUN>)",
                                        use_lemmatizer=True)

  vectorizer_propositions = KeyphraseTfidfVectorizer(spacy_pipeline='fr_dep_news_trf',
                                        pos_pattern="<VERB>(<DET><NOUN><ADP><NOUN>|<DET><NOUN><ADJ>|<DET><NOUN><NOUN>)",
                                        use_lemmatizer=True)

  m = vectorizer.fit_transform(documents)
  m_prop = vectorizer_propositions.fit_transform(documents)

  phrases = get_top_tfidf_phrases(10, vectorizer, m)
  propositions = get_top_tfidf_phrases(10, vectorizer_propositions, m_prop)

  json_analysis = build_json(phrases, propositions)
  return json_analysis

def get_top_tfidf_phrases(number_phrases, vectorizer, tfidf):
  return sorted(list(zip(vectorizer.get_feature_names_out(), tfidf.sum(0).getA1())), key=lambda x: x[1], reverse=True)[:number_phrases]

def build_json(phrases, propositions):
  analysis = []
  for i, k in enumerate(phrases):
    analysis.append({ "id": i, "name": k[0], "weight": k[1], "level": 1 })
  for j, p in enumerate(propositions):
    analysis.append({ "id": len(phrases) + j, "name": p[0], "weight": p[1], "level": 2 })
  return analysis