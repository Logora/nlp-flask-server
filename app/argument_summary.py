import pandas as pd
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain

def get_summary(uid, documents, question):
  separator = "\n\n--------------------\n\n"
  long_text = separator.join(documents)

  text_splitter = CharacterTextSplitter(        
      separator=separator,
      chunk_overlap=0
  )

  texts = text_splitter.split_text(long_text)
  docs = [Document(page_content=t) for t in texts]

  llm = OpenAI(temperature=0, model_name='text-davinci-003', batch_size=10)

  map_template = """
    Ta tâche est de résumer des contributions de personnes ayant répondu au débat suivant : {question}.
    Voici les contributions séparées par une ligne :

    {text}
    
    Résume ces contributions en affichant les trois arguments les plus récurrents. Pour chaque argument, donne aussi leur nombre d'occurrences dans les contributions.
    Ces arguments doivent être de 200 caractères maximum chacun et être classés du plus récurrent au moins récurrent.

    ARGUMENTS:"""
  map_prompt = PromptTemplate(template=map_template, input_variables=['text', 'question'])

  reduce_template = """
    Ta tâche est de résumer des arguments en réponse au débat suivant : {question}.
    Voici les arguments séparées par une ligne :

    {text}
    
    Résume ces arguments en affichant les trois arguments les plus récurrents. Pour chaque argument, ajoute aussi leur nombre d'occurrences.
    Ces arguments doivent être de 200 caractères maximum chacun et être classés du plus récurrent au moins récurrent, et sous format JSON.

    ARGUMENTS:"""
  reduce_prompt = PromptTemplate(template=reduce_template, input_variables=['text', 'question'])

  chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=map_prompt, combine_prompt=reduce_prompt)

  output = chain({"input_documents": docs, "question": question})

  arguments = json.loads(output['output_text'])
  json_analysis = build_json(arguments)
  return json_analysis

def build_json(arguments):
  analysis = {}
  argument_objects = []
  for i, k in enumerate(arguments):
    argument_objects.append({ "id": i, "argument": k["argument"], "weight": k["occurrences"] })
  analysis['arguments'] = argument_objects
  return analysis