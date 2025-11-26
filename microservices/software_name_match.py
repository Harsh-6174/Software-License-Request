from rapidfuzz import process
import json

with open("microservices/softwares.json") as f:
    softwares = json.load(f)

def resolve_software_name(software_name: str):
    match = process.extract(software_name, softwares.keys(), limit=1)

    best_match, score, index = match[0]

    if score < 50:
        return None, None

    return best_match, softwares[best_match]