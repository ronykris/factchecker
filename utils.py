def jsonl2json(file_path, output_path):
    """Conver Jsonl to json
    Example:
        file_path = "./data.jsonl"
        output_path = "./datasets/newfile.json"

        jsonl2json(file_path, output_path)
    
    """
    import pandas as pd
    import json
    output_data = []
    with open(file_path, "r") as input_file:
        for line in input_file:
            line = json.loads(line)
            output_data.append(line)
    data = pd.DataFrame(output_data)
    return data.to_json(output_path)

'''A function to clean tweets
ARGS:
    text: String
EXAMPLE:
    text = "This is an example text with URLs like https://t.co/iZnkdyaKS6, usernames like @username, emojis like 😊, and numbers like 12345.\n\nIt also has multiple consecutive newline characters."

    cleaned_text = clean_text(text)
    print(cleaned_text)

OUTPUT:
    this is an example text with urls like  usernames like  emojis like  and numbers like it also has multiple consecutive newline characters
'''


def clean_text(text):

    import re
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove usernames (@mentions)
    text = re.sub(r'@\S+', '', text)
    
    # Remove emojis (Unicode symbols)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove multiple consecutive newline characters
    text = re.sub(r'\n\n+', '\n', text)
    
    # Remove any remaining non-letter or non-space characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    return text