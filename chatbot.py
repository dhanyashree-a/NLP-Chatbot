import spacy
import json
import random

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Load chatbot responses from JSON
with open("data.json", "r") as file:
    responses = json.load(file)

def get_response(user_input):
    user_input = user_input.lower()  # Convert to lowercase
    doc = nlp(user_input)  # Process user input

    best_match = None
    highest_similarity = 0.0

    for intent, data in responses.items():
        for pattern in data["patterns"]:
            pattern_doc = nlp(pattern)  # Process each pattern
            similarity = doc.similarity(pattern_doc)  # Calculate similarity

            if similarity > highest_similarity:  # If better match found
                highest_similarity = similarity
                best_match = intent

    # If similarity is above a certain threshold, return response
    if highest_similarity > 0.6 and best_match:
        return random.choice(responses[best_match]["responses"])

    return random.choice(responses["default"]["responses"])
