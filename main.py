import json
import os

KNOWLEDGE_FILE = "knowledge.json"

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
    return knowledge.get(key)

def main():
    knowledge = load_knowledge()
    print("AI Assistant (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            print("AI: Goodbye!")
            break

        # Check for "translate" and "in" in any order
        words = user_input.split()
        if all(word in words for word in ["translate", "in"]):
            print("AI: Please translate at https://translate.google.com")
            continue

        response = get_response(user_input, knowledge)
        if response:
            print("AI:", response)
        else:
            print("AI: I don't know how to respond to that. How should I reply?")
            new_response = input("Teach me: ").strip()
            if new_response:
                knowledge[user_input] = new_response
                save_knowledge(knowledge)
                print("AI: Got it! I'll remember that. Thank you!")

if __name__ == "__main__":
    main()
