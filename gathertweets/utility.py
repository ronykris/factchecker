import re
import pandas as pd
import json
import numpy as np
import cohere
from dotenv import load_dotenv
import os
import time

load_dotenv()
co = cohere.Client(os.getenv('cohere_key')) # This is your trial API key


def cleanup(text):
    text = re.sub('http[s]?://\S+', '', text)
    text = text.replace('\n',' ')
    text = text.replace('  ', ' ')
    text = text.encode("ascii", "ignore").decode()
    #print(text)
    return text.strip()

def jsonl2json(file_path, output_path):
    """Conver Jsonl to json
    Example:
        file_path = "./data.jsonl"
        output_path = "./datasets/newfile.json"

        jsonl2json(file_path, output_path)
    
    """    
    output_data = []
    with open(file_path, "r") as input_file:
        for line in input_file:
            line = json.loads(line)
            output_data.append(line)
    data = pd.DataFrame(output_data)
    return data.to_json(output_path)


def getEmbeddings(txt):  
  return np.concatenate(co.embed([txt]).embeddings, axis=0).tolist()  #flatten the array of array

def performSRL(txt):
    response = co.generate(
        model='command-xlarge-nightly',
        prompt='Read the following sentence and output a JSON object with the entities and their type. Also, grammatically identify the relation of the entities with the subject.\n\nExample:\nsentence: \"President Biden is committed to working with Prime Minister Albanese and Prime Minister Sunak to ensure security and prosperity for decades to come.\"\nJSON: \n{\n    \"entities\": [\n      {\n        \"name\": \"President Biden\",\n        \"type\": \"person\"\n      },\n      {\n        \"name\": \"Prime Minister Albanese\",\n        \"type\": \"person\"\n      },\n      {\n        \"name\": \"Prime Minister Sunak\",\n        \"type\": \"person\"\n      }\n    ],\n    \"relation\": [\"is committed to working with\", \"to ensure security and prosperity\"]'+','+'\n    \"subject\": \"President Biden\"\n}\n\n--\n\nsentence: \"'+txt+'\"\nJSON:',
        max_tokens=1074,
        temperature=0.7,
        k=0,
        p=0.75,
        stop_sequences=['--'],
        return_likelihoods='NONE')
    print('Prediction: {}'.format(response.generations[0].text))
    return json.loads(response.generations[0].text)
