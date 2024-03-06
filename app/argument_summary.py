import pandas as pd
import json
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from prompts import summarize_templates
from config import Config

def get_summary(uid, documents, question, language='fr', model_name='gpt-3.5-turbo-0125'):
    """
    Get the summary of arguments based on documents and a given question.

    Args:
        uid (str): Unique ID.
        documents (List[str]): List of documents containing contributions.
        question (str): The debate question.
        language (str): The analysis language. Defaults to 'fr'
        model_name (str, optional): Name of the OpenAI model. Defaults to 'gpt-3.5-turbo-0125'.

    Returns:
        dict: JSON analysis of the most recurrent arguments.
    """
    MAX_PROMPT_LENGTH = 15000

    class Argument(BaseModel):
        argument: str = Field(description="an argument")
        occurrences: int = Field(description="number of occurrences", gt=1, le=5)

    class ArgumentList(BaseModel):
        arguments: List[Argument]

    parser = JsonOutputParser(pydantic_object=ArgumentList)
    response_format = parser.get_format_instructions()

    docs = [Document(page_content=content) for content in documents]

    summarize_prompt = PromptTemplate(template=summarize_templates.get(language), input_variables=['text', 'question'], partial_variables={"format_instructions": response_format})

    llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=Config.OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=summarize_prompt)
    
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    while True:
        prompt_length = stuff_chain.prompt_length(docs, question=question, response_format=response_format)
        if prompt_length > MAX_PROMPT_LENGTH:
            docs.pop()
        else:
            break
            
    output = stuff_chain.run(question=question, input_documents=docs, response_format=response_format)
    json_output = json.loads(output)
    json_analysis = build_json(json_output["arguments"])
    return json_analysis

def build_json(arguments):
    analysis = {}
    argument_objects = []
    for i, k in enumerate(arguments):
        argument_objects.append({ "id": i, "argument": k["argument"], "weight": k["occurrences"] })
    analysis['arguments'] = argument_objects
    return analysis