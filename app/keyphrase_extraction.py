import pandas as pd
import json
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from prompts import summarize_templates, keyphrases_templates
from config import Config

def get_keyphrases(uid, documents, question, language='fr', model_name='gpt-4o-mini'):
    """
    Get the keyphrases of arguments based on documents and a given question.

    Args:
        uid (str): Unique ID.
        documents (List[str]): List of documents containing contributions.
        question (str): The debate question.
        language (str): The analysis language. Defaults to 'fr'
        model_name (str, optional): Name of the OpenAI model. Defaults to 'gpt-4o-mini'.

    Returns:
        dict: JSON keywords extraction of the most recurrent arguments.
    """
    MAX_PROMPT_LENGTH = 15000

    json_schema ={
        "title": "KeyphraseList",
        "type": "object",
        "properties": {
            "keyphrases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "keyphrase": {
                        "type": "string",
                        "description": "keyword content"
                    },
                    "occurrences": {
                        "type": "integer",
                        "description": "number of occurrences"
                    }
                },
                "required": ["keyphrase", "occurrences"]
            }
            }
        },
        "required": ["keyphrases"]
        }
    docs = [Document(page_content=content) for content in documents]

    prompt = PromptTemplate(template=keyphrases_templates.get(language), input_variables=['context', 'question'])

    llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=Config.OPENAI_API_KEY, model_kwargs={ "response_format": { "type": "json_schema", "json_schema": { "name": "argument_schema", "schema": json_schema } } })
    stuff_chain = create_stuff_documents_chain(llm, prompt)

    while True:
        formatted_input = prompt.format(context=" ".join([doc.page_content for doc in docs]),
                                        question=question)
        prompt_length = len(formatted_input)
        if prompt_length > MAX_PROMPT_LENGTH:
            docs.pop()
        else:
            break
            
    output = stuff_chain.invoke({
        "context": docs,
        "question": question
    })

    json_output = json.loads(output)
    json_analysis = build_json(json_output["keyphrases"])
    return json_analysis

    
def build_json(keyphrases):
  analysis = {}
  keyphrase_objects = []
  for i, k in enumerate(keyphrases):
    keyphrase_objects.append({ "id": i, "name": k["keyphrase"], "frequency": k["occurrences"] })
  analysis['keyphrases'] = keyphrase_objects
  return analysis