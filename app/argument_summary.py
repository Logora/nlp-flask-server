import pandas as pd
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
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
        map_template (str): Template for the map_prompt.
        reduce_template (str): Template for the reduce_prompt.
        model_name (str, optional): Name of the OpenAI model. Defaults to 'gpt-3.5-turbo-0125'.

    Returns:
        dict: JSON analysis of the most recurrent arguments.
    """
    MAX_PROMPT_LENGTH = 15000
    docs = [Document(page_content=content) for content in documents]

    summarize_prompt = PromptTemplate(template=summarize_templates.get(language), input_variables=['text', 'question'])

    llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=Config.OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=summarize_prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    
    while True:
        prompt_length = stuff_chain.prompt_length(docs, question=question)
        if prompt_length > MAX_PROMPT_LENGTH:
            docs.pop()
        else:
            break

    output = stuff_chain.run(question=question, input_documents=docs)
    arguments = json.loads(output)['arguments']

    json_analysis = build_json(arguments)
    return json_analysis

def build_json(arguments):
    analysis = {}
    argument_objects = []
    for i, k in enumerate(arguments):
        argument_objects.append({ "id": i, "argument": k["argument"], "weight": k["occurrences"] })
    analysis['arguments'] = argument_objects
    return analysis
