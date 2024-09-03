from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your quiz topics and questions
topics = {
    "Colors": [
        {
            "question": "How to say Red in German? 🔴",
            "options": ["der blau", "die gelb", "das rot", "der red"],
            "answer": "das rot"
        },
        {
            "question": "How to say Blue in German? 🔵",
            "options": ["der grün", "die blau", "das orange", "die bleu"],
            "answer": "die blau"
        },
        {
            "question": "How to say Green in German? 🟢",
            "options": ["der orange", "die lila", "das grün", "die stift"],
            "answer": "das grün"
        },
        {
            "question": "How to say Yellow in German? 🟡",
            "options": ["der braun", "die gelb", "das blau", "die geld"],
            "answer": "die gelb"
        },
        {
            "question": "How to say Orange in German? 🟠",
            "options": ["der pink", "die orange", "das violett", "die orango"],
            "answer": "die orange"
        },
        {
            "question": "How to say Pink in German? 🌸",
            "options": ["der lila", "die pink", "das türkis", "die pik"],
            "answer": "die pink"
        }
    ],
    "Numbers": [
        {
            "question": "How to say One in German? 1️⃣",
            "options": ["eins", "zwei", "drei", "vier"],
            "answer": "eins"
        },
        {
            "question": "How to say Two in German? 2️⃣",
            "options": ["eins", "zwei", "drei", "vier"],
            "answer": "zwei"
        },
        {
            "question": "How to say Three in German? 3️⃣",
            "options": ["eins", "zwei", "drei", "vier"],
            "answer": "drei"
        },
        {
            "question": "How to say Four in German? 4️⃣",
            "options": ["eins", "zwei", "drei", "vier"],
            "answer": "vier"
        }
    ],
    "Animals": [
        {
            "question": "How to say Dog in German? 🐶",
            "options": ["Katze", "Hund", "Maus", "Vogel"],
            "answer": "Hund"
        },
        {
            "question": "How to say Cat in German? 🐱",
            "options": ["Katze", "Hund", "Maus", "Vogel"],
            "answer": "Katze"
        },
        {
            "question": "How to say Mouse in German? 🐭",
            "options": ["Katze", "Hund", "Maus", "Vogel"],
            "answer": "Maus"
        },
        {
            "question": "How to say Bird in German? 🦜",
            "options": ["Katze", "Hund", "Maus", "Vogel"],
            "answer": "Vogel"
        }
    ]
}

articles = [
    {
        "question": "What is the article for 'Apfel' (apple)? 🍎",
        "options": ["der Apfel", "die Apfel", "das Apfel"],
        "answer": "der Apfel"
    },
    {
        "question": "What is the article for 'Banane' (banana)? 🍌",
        "options": ["der Banane", "die Banane", "das Banane"],
        "answer": "die Banane"
    },
    {
        "question": "What is the article for 'Haus' (house)? 🏠",
        "options": ["der Haus", "die Haus", "das Haus"],
        "answer": "das Haus"
    },
    {
        "question": "What is the article for 'Tisch' (table)? 🪑",
        "options": ["der Tisch", "die Tisch", "das Tisch"],
        "answer": "der Tisch"
    }
]

current_question = {}
current_topic = {}
current_section = {}
user_scores = {}  # To track user scores

def get_degree(score, total_questions):
    percentage = (score / total_questions) * 100
    if percentage == 100:
        return "🌟 Excellent 🌟"
    elif percentage >= 75:
        return "👍 Good 👍"
    elif percentage >= 50:
        return "🤔 Needs Improvement 🤔"
    else:
        return "😢 Poor 😢"

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Vocabulary", callback_data="Vocabulary")],
        [InlineKeyboardButton("Articles", callback_data="Articles")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '👋 Hi there! Welcome to the German Language Quiz! Choose a section to start.',
        reply_markup=reply_markup
    )

async def select_section(update: Update, context: CallbackContext) -> None:
    global current_section
    user_id = update.effective_user.id
    current_section[user_id] = update.callback_query.data

    if current_section[user_id] == "Vocabulary":
        keyboard = [[InlineKeyboardButton(topic, callback_data=topic)] for topic in topics.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(
            'Select a category:',
            reply_markup=reply_markup
        )
    elif current_section[user_id] == "Articles":
        current_topic[user_id] = "Articles"
        current_question[user_id] = 0
        user_scores[user_id] = 0  # Initialize score for new quiz
        await send_question(update, context)

async def select_topic(update: Update, context: CallbackContext) -> None:
    global current_topic, current_question
    user_id = update.effective_user.id
    current_topic[user_id] = update.callback_query.data
    current_question[user_id] = 0
    user_scores[user_id] = 0  # Initialize score for new quiz

    await send_question(update, context)

async def send_question(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    section = current_section.get(user_id)
    topic = current_topic.get(user_id)
    
    if section is None:
        await update.callback_query.message.reply_text("Please select a section first.")
        return
    
    if section == "Articles":
        question_data = articles[current_question[user_id]]
    else:
        question_data = topics[topic][current_question[user_id]]
    
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in question_data['options']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        f"🔍 {question_data['question']}",
        reply_markup=reply_markup
    )

async def handle_answer(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    section = current_section.get(user_id)
    topic = current_topic.get(user_id)

    if section is None:
        await update.callback_query.message.reply_text("Please select a section to start the quiz.")
        return

    if section == "Articles":
        question_data = articles[current_question[user_id]]
    else:
        question_data = topics[topic][current_question[user_id]]
    
    selected_option = update.callback_query.data

    if selected_option == question_data['answer']:
        user_scores[user_id] += 1
        await update.callback_query.message.reply_text("🎉 Correct! 🎉")
    else:
        await update.callback_query.message.reply_text("❌ Incorrect! ❌")

    current_question[user_id] += 1
    if current_question[user_id] < (len(articles) if section == "Articles" else len(topics[topic])):
        await send_question(update, context)
    else:
        score = user_scores.get(user_id, 0)
        degree = get_degree(score, len(articles) if section == "Articles" else len(topics[topic]))
        await update.callback_query.message.reply_text(
            f"🎊 Quiz completed! 🎊\n\nYou got {score}/{len(articles) if section == 'Articles' else len(topics[topic])} correct answers.\nYour degree: {degree} 🏆\n\nWould you like to try another section?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Vocabulary", callback_data="Vocabulary")],
                [InlineKeyboardButton("Articles", callback_data="Articles")]
            ])
        )
        # Optionally reset the topic and score if needed for the next quiz session
        del current_question[user_id]
        del user_scores[user_id]

def main() -> None:
    application = Application.builder().token("7319290683:AAGTWkwCFruMRywgFFAMl2baZFyhBOJRVxs").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(select_section, pattern='^(Vocabulary|Articles)$'))
    application.add_handler(CallbackQueryHandler(select_topic, pattern='^(Colors|Numbers|Animals)$'))
    application.add_handler(CallbackQueryHandler(handle_answer))

    application.run_polling()

if __name__ == '__main__':
    main()
