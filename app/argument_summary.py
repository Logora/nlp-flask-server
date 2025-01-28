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
from prompts import summarize_templates
from config import Config

def get_summary(uid, documents, question, language='fr', model_name='gpt-4o-mini'):
    """
    Get the summary of arguments based on documents and a given question.

    Args:
        uid (str): Unique ID.
        documents (List[str]): List of documents containing contributions.
        question (str): The debate question.
        language (str): The analysis language. Defaults to 'fr'
        model_name (str, optional): Name of the OpenAI model. Defaults to 'gpt-4o-mini'.

    Returns:
        dict: JSON analysis of the most recurrent arguments.
    """
    MAX_PROMPT_LENGTH = 15000

    class Argument(BaseModel):
        argument: str = Field(description="an argument")
        occurrences: int = Field(description="number of occurrences")

    class ArgumentList(BaseModel):
        arguments: List[Argument]

    parser = JsonOutputParser(pydantic_object=ArgumentList)
    response_format = parser.get_format_instructions()

    docs = [Document(page_content=content) for content in documents]

    summarize_prompt = PromptTemplate(template=summarize_templates.get(language), input_variables=['text', 'question'], partial_variables={"format_instructions": response_format})

    llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=Config.OPENAI_API_KEY)
    llm_with_structured_output = llm.with_structured_output(ArgumentList)
    stuff_chain = create_stuff_documents_chain(llm_with_structured_output, summarize_prompt)

    while True:
        formatted_input = summarize_prompt.format(context=" ".join([doc.page_content for doc in docs]), 
                                          question=question,
                                          response_format=response_format)
        prompt_length = len(formatted_input)
        if prompt_length > MAX_PROMPT_LENGTH:
            docs.pop()
        else:
            break
            
    output = stuff_chain.invoke({
    "context": docs, 
    "question": question, 
    "response_format": response_format
    })

    print("the output"+output)


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