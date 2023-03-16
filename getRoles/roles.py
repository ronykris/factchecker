import cohere
from dotenv import load_dotenv
import os

load_dotenv()

co = cohere.Client(os.getenv('cohere_key')) # This is your trial API key
response = co.generate(
  model='command-xlarge-nightly',
  prompt='Read the following sentence and output a JSON object with the entities and their type. Also, grammatically identify the relation of the entities with the subject.\n\nExample:\nsentence: \"President Biden is committed to working with Prime Minister Albanese and Prime Minister Sunak to ensure security and prosperity for decades to come.\"\nJSON: \n{\n    \"entities\": [\n      {\n        \"name\": \"President Biden\",\n        \"type\": \"person\"\n      },\n      {\n        \"name\": \"Prime Minister Albanese\",\n        \"type\": \"person\"\n      },\n      {\n        \"name\": \"Prime Minister Sunak\",\n        \"type\": \"person\"\n      }\n    ],\n    \"relation\": [\"is committed to working with\", \"to ensure security and prosperity\"],\n    \"subject\": \"President Biden\"\n}\n\n--\n\nsentence: \"On International Women\'s Day, the First Lady hosted the International Women of Courage Award for the first time at the White House. These courageous women are pursuing justice, freedom, and peace around the world.\"\nJSON:',
  max_tokens=1074,
  temperature=0.7,
  k=0,
  p=0.75,
  stop_sequences=[],
  return_likelihoods='NONE')

print('Prediction: {}'.format(response.generations[0].text))