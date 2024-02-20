import pandas as pd
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from prompts import map_templates, reduce_templates
from config import Config

def get_summary(uid, documents, question, language='fr', model_name='gpt-3.5-turbo-instruct'):
    """
    Get the summary of arguments based on documents and a given question.

    Args:
        uid (str): Unique ID.
        documents (List[str]): List of documents containing contributions.
        question (str): The debate question.
        language (str): The analysis language.
        map_template (str): Template for the map_prompt.
        reduce_template (str): Template for the reduce_prompt.
        model_name (str, optional): Name of the OpenAI model. Defaults to 'text-davinci-003'.

    Returns:
        dict: JSON analysis of the most recurrent arguments.
    """
    separator = "\n\n--------------------\n\n"
    long_text = separator.join(documents)

    text_splitter = CharacterTextSplitter(        
        separator=separator,
        chunk_overlap=0
    )

    texts = text_splitter.split_text(long_text)
    docs = [Document(page_content=t) for t in texts]

    llm = OpenAI(temperature=0, model_name=model_name, batch_size=10, openai_api_key=Config.OPENAI_API_KEY)

    map_prompt = PromptTemplate(template=map_templates.get(language), input_variables=['text', 'question'])
    reduce_prompt = PromptTemplate(template=reduce_templates.get(language), input_variables=['text', 'question'])

    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=map_prompt, combine_prompt=reduce_prompt)

    output = chain({"input_documents": docs, "question": question})

    output_text = output['output_text']
    points = [point.strip() for point in output_text.split("\n\n") if point.strip()]
    
    arguments = []

    for point in points:
        index, rest = point.split(".", 1)
        description, recurrence = rest.split("(Récurrence: ", 1)
        weight = recurrence.split("/")[0]
        arguments.append({
            "id": index.strip(),
            "argument": description.strip(),
            "occurrences": weight
        })

    json_analysis = build_json(arguments)
    return json_analysis

def build_json(arguments):
    analysis = {}
    argument_objects = []
    for i, k in enumerate(arguments):
        argument_objects.append({ "id": i, "argument": k["argument"], "weight": k["occurrences"] })
    analysis['arguments'] = argument_objects
    return analysis