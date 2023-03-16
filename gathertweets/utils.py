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



#txt = "Today, @POTUS, @AlboMP, and @RishiSunak announced steps to carry forward the Australia \u2013 U.K. \u2013 U.S. Partnership.\n\nDeveloping Australia\u2019s conventionally-armed, nuclear-powered submarine capacity and our own will enhance stability in the Indo-Pacific. https://t.co/nZzWt5SbQq"
#cleanup(txt)