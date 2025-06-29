import json
import os
from difflib import get_close_matches
import re
import random

KNOWLEDGE_FILE = "knowledge.json"
SIMILARITY_THRESHOLD = 0.6

_TOPIC_CHANGE_PATTERNS = [
    re.compile(r"btw do u know (?:about |concerning )?(.+)\??", re.IGNORECASE),
    re.compile(r"btw do you know (?:about |concerning )?(.+)\??", re.IGNORECASE),
    re.compile(r"tell me about (.+)\??", re.IGNORECASE),
    re.compile(r"let's talk about (.+)\??", re.IGNORECASE),
    re.compile(r"what about (.+)\??", re.IGNORECASE),
    re.compile(r"speaking of (.+)\??", re.IGNORECASE),
    re.compile(r"how about (.+)\??", re.IGNORECASE),
]

def _extract_topic_for_redirection(user_input_str):
    for pattern in _TOPIC_CHANGE_PATTERNS:
        match = pattern.match(user_input_str)
        if match:
            if match.groups() and match.groups()[-1]:
                topic = match.groups()[-1].strip()
                return topic.lower()
    return None

def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return {}
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_knowledge(knowledge):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4, ensure_ascii=False)

def get_response(user_input, knowledge):
    key = user_input.strip().lower()
    
    if key in knowledge:
        return knowledge[key]
    
    matches = get_close_matches(key, knowledge.keys(), n=1, cutoff=SIMILARITY_THRESHOLD)
    if matches:
        closest_match = matches[0]
        return f"{knowledge[closest_match]}"
    
    return None

def handle_translation_request(user_input):
    words = user_input.split()
    if "translate" in words and "in" in words:
        return "AI: Please translate at https://translate.google.com"
    return None

def load_jokes():
    jokes_file = "jokes.txt"
    if not os.path.exists(jokes_file):
        return []
    with open(jokes_file, "r", encoding="utf-8") as f:
        jokes = [line.strip() for line in f if line.strip()]
    return jokes

def main():
    knowledge = load_knowledge()
    jokes = load_jokes()
    print("AI Assistant (type 'exit' to quit)")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("AI: Goodbye! 👋")
            break
        
        if not user_input:
            continue

        # Joke handling
        if user_input.lower() == "tell me a joke":
            if jokes:
                print("AI:", random.choice(jokes))
            else:
                print("AI: Sorry, I don't have any jokes right now.")
            continue

        extracted_topic = _extract_topic_for_redirection(user_input)
        
        if extracted_topic:
            relevant_responses = [
                v for k, v in knowledge.items() if extracted_topic in k.lower()
            ]
            if relevant_responses:
                print("AI:", random.choice(relevant_responses))
            else:
                print(f"AI: I don't have specific information about '{extracted_topic}' right now.")
            continue

        translation_response = handle_translation_request(user_input.lower())
        if translation_response:
            print(translation_response)
            continue

        response = get_response(user_input, knowledge)
        if response:
            print("AI:", response)
        else:
            print("AI: 🔁 *beep boop* Error:I don't know how to respond to that. How should I reply?")
            new_response = input("Teach me: ").strip()
            if new_response:
                knowledge[user_input.lower()] = new_response
                save_knowledge(knowledge)
                print("AI: Got it! I'll remember that. Thank you!")

if __name__ == "__main__":
    main()
