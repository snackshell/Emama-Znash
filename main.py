d
import json
import pyrogram
from pyrogram import filters
from pyrogram.types import User
from difflib import get_close_matches

API_ID = "28153993"
API_HASH = "976fd7cc4958ad84181a53b41919564b"
BOT_TOKEN = "6521793351:AAFENjT-HteezOsbRBTFz5cTAUEchdgCPKw"

app = pyrogram.Client(
    "chat_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

bot_info = None

def get_bot_info():
    global bot_info
    if bot_info is None:
        bot_info = app.get_me()
    return bot_info

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, question: list[str]) -> str | None:
    matches = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

@app.on_message(filters.text & ~filters.edited & ~filters.via_bot)
def chat_bot(client, message):
    if not get_bot_info():
        return

    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    user_input: str = message.text

    if user_input.lower() == '/start':
        message.reply_text("Welcome to the chat bot! You can start by asking me questions.")
        return

    if user_input.lower() == 'quit':
        message.reply_text("Goodbye!")
        return

    if is_bot_user(message.from_user):
        return

    best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        message.reply_text(answer)
    else:
        message.reply_text('I don\'t know the answer. Can you teach me?')
        new_answer: str = message.text

        if new_answer.lower() ≠ 'skip':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            message.reply_text('Thank you! I learned a new response!')

def is_bot_user(user: User) -> bool:
    return user.id == get_bot_info().id

if __name__ == '__main__':
    app.run()
