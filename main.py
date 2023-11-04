import json
import pyrogram
from pyrogram import filters
from difflib import get_close_matches

API_ID = 28153993  # Use integers, not strings
API_HASH = "976fd7cc4958ad84181a53b41919564b"
BOT_TOKEN = "6521793351:AAFENjT-HteezOsbRBTFz5cTAUEchdgCPKw"

app = pyrogram.Client(
    "chat_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Fetch the bot's information to get the bot's user ID
bot_info = None

def get_bot_info():
    global bot_info
    if bot_info is None:
        bot_info = app.get_me()
    return bot_info

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, question_list: list) -> str | None:
    matches = get_close_matches(user_question, question_list, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

@app.on_message(filters.text & ~filters.via_bot)
def chat_bot(client, message):
    if not get_bot_info():
        return
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    user_input: str = message.text.lower()  # Convert user input to lowercase for case-insensitive matching

    if user_input == '/start':
        message.reply_text("Hey! I am Emama Znash. Ask me anything.")
        return

    if user_input == 'quit':
        message.reply_text("Goodbye!")
        return

    best_match: str | None = find_best_match(user_input, [q["question"].lower() for q in knowledge_base["questions"]])

    if best_match:
        answer: str | None = get_answer_for_question(best_match, knowledge_base)
        if answer:
            message.reply_text(answer)
        else:
            message.reply_text('I don\'t know the answer. Can you teach me?')
            # You should handle teaching the bot here and then update the knowledge base.
    else:
        message.reply_text('I don\'t know the answer. Can you teach me?')
        # You should handle teaching the bot here and then update the knowledge base.


if __name__ == '__main__':  # Use __name__, not name
    app.run()
