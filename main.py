import json
import os
import re
import random
import locale
from difflib import get_close_matches

# Detect system language
def detect_language():
    lang = locale.getdefaultlocale()[0]
    if lang and lang.startswith("ar"):
        return "ar"
    return "en"

# Initial language mode
LANGUAGE_MODE = detect_language()
SIMILARITY_THRESHOLD = 0.6
KNOWLEDGE_FILES = {
    "en": "knowledge.json",
    "ar": "knowledge_ar.json"
}
JOKES_FILES = {
    "en": "jokes.txt",
    "ar": "jokes_ar.txt"
}

# Recognize topic-shift patterns
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
        if match and match.groups()[-1]:
            return match.groups()[-1].strip().lower()
    return None

def load_knowledge():
    file_path = KNOWLEDGE_FILES.get(LANGUAGE_MODE, "knowledge.json")
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_knowledge(knowledge):
    file_path = KNOWLEDGE_FILES.get(LANGUAGE_MODE, "knowledge.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4, ensure_ascii=False)

def get_response(user_input, knowledge):
    key = user_input.strip().lower()
    if key in knowledge:
        return knowledge[key]
    matches = get_close_matches(key, knowledge.keys(), n=1, cutoff=SIMILARITY_THRESHOLD)
    if matches:
        return knowledge[matches[0]]
    return None

def handle_translation_request(user_input):
    words = user_input.split()
    if "translate" in words and "in" in words:
        return "AI: Please translate at https://translate.google.com"
    return None

def load_jokes():
    jokes_file = JOKES_FILES.get(LANGUAGE_MODE, "jokes.txt")
    if not os.path.exists(jokes_file):
        return []
    with open(jokes_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    global LANGUAGE_MODE
    knowledge = load_knowledge()
    jokes = load_jokes()

    print("AI Assistant (type 'exit' to quit, or 'mode: ar' / 'mode: en' to switch language)")
    print(f"🌍 Language mode: {'Arabic 🇲🇦' if LANGUAGE_MODE == 'ar' else 'English 🇬🇧'}")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("AI: Goodbye! 👋" if LANGUAGE_MODE == "en" else "الذكاء الاصطناعي: إلى اللقاء! 👋")
            break

        if user_input.lower().startswith("mode:"):
            mode = user_input.lower().split(":")[1].strip()
            if mode in KNOWLEDGE_FILES:
                LANGUAGE_MODE = mode
                knowledge = load_knowledge()
                jokes = load_jokes()
                print(f"AI: Language set to {'Arabic 🇲🇦' if mode == 'ar' else 'English 🇬🇧'}")
            else:
                print("AI: ⚠️ Unknown mode. Use 'mode: ar' or 'mode: en'.")
            continue

        if user_input.lower() == "tell me a joke":
            if jokes:
                print("AI:", random.choice(jokes))
            else:
                print("AI: Sorry, I don't have jokes yet." if LANGUAGE_MODE == "en" else "عذرًا، لا يوجد نُكت حالياً 🤷‍♂️")
            continue

        topic = _extract_topic_for_redirection(user_input)
        if topic:
            matches = [v for k, v in knowledge.items() if topic in k.lower()]
            if matches:
                print("AI:", random.choice(matches))
            else:
                print(f"AI: I don't have info on '{topic}' yet." if LANGUAGE_MODE == "en" else f"الذكاء الاصطناعي: لا أملك معلومات عن '{topic}' حاليًا.")
            continue

        translation_response = handle_translation_request(user_input.lower())
        if translation_response:
            print(translation_response)
            continue

        response = get_response(user_input, knowledge)
        if response:
            print("AI:", response)
        else:
            unknown = "I don't know how to respond to that. How should I reply?" if LANGUAGE_MODE == "en" else "🤖 لا أعرف كيف أرد على ذلك. علمني الرد المناسب:"
            print(f"AI: {unknown}")
            new_response = input("Teach me: ").strip()
            if new_response:
                knowledge[user_input.strip().lower()] = new_response
                save_knowledge(knowledge)
                print("AI: Got it! I'll remember that." if LANGUAGE_MODE == "en" else "تم الحفظ! سأستخدم هذا الرد مستقبلاً ✅")

if __name__ == "__main__":
    main()
