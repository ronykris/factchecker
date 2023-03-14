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
