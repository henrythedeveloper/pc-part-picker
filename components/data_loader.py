import json

def load_components():
    with open('data/components_data.json', 'r') as f:
        data = json.load(f)
    return data
