import json
import os
from difflib import get_close_matches

KNOWLEDGE_FILE = "knowledge.json"
SIMILARITY_THRESHOLD = 0.6  # Adjust this value (0-1) to control how close a match needs to be

def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return {}
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_knowledge(knowledge):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4, ensure_ascii=False)

def get_response(user_input, knowledge):
    key = user_input.strip().lower()
    
    # First try exact match
    if key in knowledge:
        return knowledge[key]
    
    # Then try fuzzy matching
    matches = get_close_matches(key, knowledge.keys(), n=1, cutoff=SIMILARITY_THRESHOLD)
    if matches:
        closest_match = matches[0]
        return f"Did you mean '{closest_match}'? {knowledge[closest_match]}"
    
    return None

def handle_translation_request(user_input):
    words = user_input.split()
    if "translate" in words and "in" in words:
        return "AI: Please translate at https://translate.google.com"
    return None

def main():
    knowledge = load_knowledge()
    print("AI Assistant (type 'exit' to quit)")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("AI: Goodbye!")
            break

        # Check for translation request
        translation_response = handle_translation_request(user_input.lower())
        if translation_response:
            print(translation_response)
            continue

        # Get and handle response
        response = get_response(user_input, knowledge)
        if response:
            print("AI:", response)
        else:
            print("AI: I don't know how to respond to that. How should I reply?")
            new_response = input("Teach me: ").strip()
            if new_response:
                knowledge[user_input.lower()] = new_response
                save_knowledge(knowledge)
                print("AI: Got it! I'll remember that. Thank you!")

if __name__ == "__main__":
    main()
