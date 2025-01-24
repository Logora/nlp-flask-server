import pandas as pd
import json
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
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

    class Keyphrase(BaseModel):
        keyphrase: str = Field(description="a keyword")
        occurrences: int = Field(description="number of occurrences")

    class KeyphraseList(BaseModel):
        keyphrases: List[Keyphrase]

    parser = JsonOutputParser(pydantic_object=KeyphraseList)
    response_format = parser.get_format_instructions()

    docs = [Document(page_content=content) for content in documents]

    prompt = PromptTemplate(template=keyphrases_templates.get(language), input_variables=['text', 'question'], partial_variables={"format_instructions": response_format})

    llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=Config.OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    stuff_chain = create_stuff_documents_chain(llm_chain=llm_chain, document_variable_name="text")

    while True:
        prompt_length = stuff_chain.prompt_length(docs,question=question, response_format=response_format)
        if prompt_length > MAX_PROMPT_LENGTH:
            docs.pop()
        else:
            break
            
    output = stuff_chain.invoke(question=question, input_documents=docs, response_format=response_format)
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