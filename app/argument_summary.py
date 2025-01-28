import pandas as pd
import json
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
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

    json_schema = {
        "title": "argumentList",
        "description": "List of summarized arguments",
        "type": "object",
        "properties": {
            "arguments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "argument": {
                            "type": "string",
                            "description": "argument content"
                        },
                        "occurrences": {
                            "type": "integer",
                            "description": "number of occurrences of the argument"
                        }
                    },
                    "required": ["argument", "occurrences"]
                }
            }
        },
        "required": ["arguments"]
    }

    docs = [Document(page_content=content) for content in documents]

    summarize_prompt = PromptTemplate(template=summarize_templates.get(language), input_variables=['context', 'question'])

    llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=Config.OPENAI_API_KEY, model_kwargs={ "response_format": { "type": "json_schema", "json_schema": { "name": "argument_schema", "schema": json_schema } } })
    stuff_chain = create_stuff_documents_chain(llm, summarize_prompt)

    while True:
        formatted_input = summarize_prompt.format(context=" ".join([doc.page_content for doc in docs]), 
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
    json_analysis = build_json(json_output["arguments"])
    return json_analysis


def build_json(arguments):
    analysis = {}
    argument_objects = []
    for i, k in enumerate(arguments):
        argument_objects.append({ "id": i, "argument": k["argument"], "weight": k["occurrences"] })
    analysis['arguments'] = argument_objects
    return analysis