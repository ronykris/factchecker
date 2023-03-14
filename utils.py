def jsonl2json(file_path):
    import pandas as pd
    import json
    output_data = []
    with open(file_path, "r") as input_file:
        for line in input_file:
            line = json.loads(line)
            output_data.append(line)
    data = pd.DataFrame(output_data)
    return data.to_json("./output.json")
