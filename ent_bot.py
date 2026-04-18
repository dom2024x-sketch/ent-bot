"""
ЕНТ Бот — Подготовка к ЕНТ
Установка: pip install python-telegram-bot
Запуск: python ent_bot.py
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)

# ========================
# НАСТРОЙКИ
# ========================BOT_TOKEN = "8237010247:AAEb-qzP-aVla3QmlpmWqcW79PqJDgW8VPw""  # Получить у @BotFather
FREE_LIMIT = 5  # Бесплатных вопросов
PAYMENT_TEXT = "💳 Оплатить подписку: @erdgxz"

logging.basicConfig(level=logging.INFO)

# ========================
# СОСТОЯНИЯ
# ========================
CHOOSING_SUBJECT, ANSWERING = range(2)

# ========================
# БАЗА ВОПРОСОВ
# ========================
QUESTIONS = {
    "История Казахстана": [
        {
            "q": "В каком году была принята первая Конституция независимого Казахстана?",
            "options": ["1991", "1993", "1995", "1998"],
            "answer": 1,
            "explain": "Первая Конституция РК принята 28 января 1993 года."
        },
        {
            "q": "Кто был первым президентом Казахстана?",
            "options": ["Касым-Жомарт Токаев", "Нурсултан Назарбаев", "Динмухамед Қонаев", "Имангали Тасмагамбетов"],
            "answer": 1,
            "explain": "Нурсултан Назарбаев — первый президент РК (1991–2019)."
        },
        {
            "q": "В каком году Казахстан обрёл независимость?",
            "options": ["1990", "1991", "1992", "1993"],
            "answer": 1,
            "explain": "16 декабря 1991 года — День Независимости Казахстана."
        },
        {
            "q": "Как называется столица Казахстана с 2019 года?",
            "options": ["Алматы", "Нур-Султан", "Астана", "Акмола"],
            "answer": 2,
            "explain": "В 2022 году столице возвращено историческое название — Астана."
        },
        {
            "q": "Декларация о государственном суверенитете Казахстана принята в:",
            "options": ["1989", "1990", "1991", "1992"],
            "answer": 1,
            "explain": "Декларация о суверенитете принята 25 октября 1990 года."
        },
        {
            "q": "ҚАКСР была образована в:",
            "options": ["1920", "1925", "1930", "1936"],
            "answer": 0,
            "explain": "Казакская АССР образована 26 августа 1920 года."
        },
        {
            "q": "Казахская ССР стала союзной республикой в:",
            "options": ["1920", "1925", "1936", "1940"],
            "answer": 2,
            "explain": "По Конституции СССР 1936 года КазССР получила статус союзной республики."
        },
    ],
    "Математика": [
        {
            "q": "Чему равно 15% от 200?",
            "options": ["20", "25", "30", "35"],
            "answer": 2,
            "explain": "200 × 0.15 = 30"
        },
        {
            "q": "Решите уравнение: 2x + 6 = 14",
            "options": ["x = 3", "x = 4", "x = 5", "x = 6"],
            "answer": 1,
            "explain": "2x = 14 - 6 = 8, x = 4"
        },
        {
            "q": "Площадь квадрата со стороной 7 см равна:",
            "options": ["28 см²", "42 см²", "49 см²", "56 см²"],
            "answer": 2,
            "explain": "S = a² = 7² = 49 см²"
        },
        {
            "q": "Чему равно: √144?",
            "options": ["10", "11", "12", "13"],
            "answer": 2,
            "explain": "√144 = 12, так как 12×12 = 144"
        },
        {
            "q": "Если a = 3, b = 4, то a² + b² = ?",
            "options": ["14", "20", "25", "30"],
            "answer": 2,
            "explain": "9 + 16 = 25"
        },
        {
            "q": "Периметр прямоугольника 5×3:",
            "options": ["15", "16", "17", "18"],
            "answer": 1,
            "explain": "P = 2(a+b) = 2(5+3) = 16"
        },
        {
            "q": "Сколько градусов в прямом угле?",
            "options": ["45°", "60°", "90°", "180°"],
            "answer": 2,
            "explain": "Прямой угол = 90°"
        },
    ],
    "Грамота (Казахский)": [
        {
            "q": "«Мектеп» сөзінің мағынасы қандай?",
            "options": ["Кітап", "Мұғалім", "Мектеп", "Оқушы"],
            "answer": 2,
            "explain": "«Мектеп» — орыс тіліндегі «школа» сөзінің баламасы."
        },
        {
            "q": "Қазақ алфавитінде қанша әріп бар?",
            "options": ["32", "38", "42", "44"],
            "answer": 2,
            "explain": "Қазіргі қазақ алфавитінде (кирилл) 42 әріп бар."
        },
        {
            "q": "«Жақсы» сөзінің антонимі:",
            "options": ["Керемет", "Жаман", "Тамаша", "Үздік"],
            "answer": 1,
            "explain": "«Жақсы» — жаман (хорошо — плохо)"
        },
        {
            "q": "Зат есім дегеніміз не?",
            "options": ["Іс-қимыл", "Зат пен құбылыс атауы", "Белгі-сапа", "Сан"],
            "answer": 1,
            "explain": "Зат есім — заттың, құбылыстың атын білдіреді (существительное)."
        },
        {
            "q": "«Кітап оқыдым» — бұл сөйлем түрі:",
            "options": ["Жай сөйлем", "Қос сөйлем", "Күрделі сөйлем", "Хабарлы сөйлем"],
            "answer": 3,
            "explain": "Хабар беретін сөйлем — хабарлы сөйлем деп аталады."
        },
    ]
}

# ========================
# ХРАНИЛИЩЕ ДАННЫХ
# ========================
user_data_store = {}

def get_user(user_id):
    if user_id not in user_data_store:
        user_data_store[user_id] = {
            "count": 0,      # всего вопросов пройдено
            "correct": 0,    # правильных ответов
            "q_index": 0,    # текущий вопрос в теме
            "subject": None, # выбранная тема
            "paid": False,   # оплатил ли
        }
    return user_data_store[user_id]

# ========================
# КОМАНДА /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    name = update.effective_user.first_name

    text = (
        f"👋 Сәлем, {name}!\n\n"
        f"📚 *ЕНТ-ке дайындық боты*\n\n"
        f"Мен саған ЕНТ-ке дайындалуға көмектесемін!\n"
        f"Тест сұрақтарына жауап бер және нәтижеңді бақыла.\n\n"
        f"🆓 Тегін: {FREE_LIMIT} сұрақ\n"
        f"💎 Толық қол жетімділік: 500 тг/ай\n\n"
        f"Пән таңда 👇"
    )

    keyboard = [
        [InlineKeyboardButton("📖 История Казахстана", callback_data="История Казахстана")],
        [InlineKeyboardButton("📐 Математика", callback_data="Математика")],
        [InlineKeyboardButton("🔤 Грамота (Казахский)", callback_data="Грамота (Казахский)")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    return CHOOSING_SUBJECT

# ========================
# ВЫБОР ПРЕДМЕТА
# ========================
async def choose_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user = get_user(user_id)
    data = query.data

    # Статистика
    if data == "stats":
        total = user["count"]
        correct = user["correct"]
        pct = round((correct / total * 100)) if total > 0 else 0
        text = (
            f"📊 *Твоя статистика*\n\n"
            f"✅ Правильно: {correct}\n"
            f"❌ Всего вопросов: {total}\n"
            f"🎯 Точность: {pct}%\n\n"
            f"{'🔥 Отличный результат!' if pct >= 70 else '📚 Нужно больше практики!'}"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back")]]
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSING_SUBJECT

    # Назад в меню
    if data == "back":
        keyboard = [
            [InlineKeyboardButton("📖 История Казахстана", callback_data="История Казахстана")],
            [InlineKeyboardButton("📐 Математика", callback_data="Математика")],
            [InlineKeyboardButton("🔤 Грамота (Казахский)", callback_data="Грамота (Казахский)")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
        ]
        await query.edit_message_text(
            "📚 Пән таңда 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return CHOOSING_SUBJECT

    # Проверка лимита
    if not user["paid"] and user["count"] >= FREE_LIMIT:
        text = (
            f"⛔️ Тегін лимит бітті ({FREE_LIMIT} сұрақ)\n\n"
            f"💎 Толық қол жетімділік алу үшін:\n"
            f"👉 {PAYMENT_TEXT}\n\n"
            f"📦 Тариф: 500 тг/ай — шексіз сұрақтар"
        )
        keyboard = [[InlineKeyboardButton("💳 Төлеу", url="https://t.me/your_username")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSING_SUBJECT

    # Начать тест
    subject = data
    user["subject"] = subject
    user["q_index"] = 0

    await send_question(query, user_id)
    return ANSWERING

# ========================
# ОТПРАВКА ВОПРОСА
# ========================
async def send_question(query, user_id):
    user = get_user(user_id)
    subject = user["subject"]
    q_index = user["q_index"]
    questions = QUESTIONS[subject]

    if q_index >= len(questions):
        user["q_index"] = 0
        q_index = 0

    q = questions[q_index]
    total = user["count"]
    remaining = FREE_LIMIT - total if not user["paid"] else "∞"

    text = (
        f"📚 *{subject}*\n"
        f"Сұрақ {q_index + 1}/{len(questions)} | Қалған: {remaining}\n\n"
        f"❓ {q['q']}"
    )

    keyboard = [
        [InlineKeyboardButton(f"{'🔵' if i == 0 else '🔵'} {opt}",
                              callback_data=f"ans_{i}")]
        for i, opt in enumerate(q["options"])
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Меню", callback_data="back")])

    await query.edit_message_text(text, parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup(keyboard))

# ========================
# ОБРАБОТКА ОТВЕТА
# ========================
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user = get_user(user_id)
    data = query.data

    # Назад в меню
    if data == "back":
        keyboard = [
            [InlineKeyboardButton("📖 История Казахстана", callback_data="История Казахстана")],
            [InlineKeyboardButton("📐 Математика", callback_data="Математика")],
            [InlineKeyboardButton("🔤 Грамота (Казахский)", callback_data="Грамота (Казахский)")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
        ]
        await query.edit_message_text("📚 Пән таңда 👇",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSING_SUBJECT

    # Обработка ответа
    subject = user["subject"]
    q_index = user["q_index"]
    q = QUESTIONS[subject][q_index]
    selected = int(data.split("_")[1])

    user["count"] += 1

    if selected == q["answer"]:
        user["correct"] += 1
        result = f"✅ *Дұрыс!*\n\n📝 {q['explain']}"
        emoji = "🎉"
    else:
        correct_text = q["options"][q["answer"]]
        result = f"❌ *Қате!*\n\n✔️ Дұрыс жауап: *{correct_text}*\n📝 {q['explain']}"
        emoji = "😔"

    # Проверка лимита
    if not user["paid"] and user["count"] >= FREE_LIMIT:
        text = (
            f"{result}\n\n"
            f"⛔️ Тегін лимит бітті!\n\n"
            f"💎 Жалғастыру үшін:\n{PAYMENT_TEXT}"
        )
        keyboard = [
            [InlineKeyboardButton("💳 Төлеу — 500 тг/ай", url="https://t.me/your_username")],
            [InlineKeyboardButton("⬅️ Меню", callback_data="back2")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSING_SUBJECT

    # Следующий вопрос
    user["q_index"] = (q_index + 1) % len(QUESTIONS[subject])

    keyboard = [
        [InlineKeyboardButton(f"{emoji} Следующий вопрос ➡️", callback_data=subject)],
        [InlineKeyboardButton("⬅️ Меню", callback_data="back2")],
    ]

    await query.edit_message_text(result, parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSING_SUBJECT

async def back_from_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📖 История Казахстана", callback_data="История Казахстана")],
        [InlineKeyboardButton("📐 Математика", callback_data="Математика")],
        [InlineKeyboardButton("🔤 Грамота (Казахский)", callback_data="Грамота (Казахский)")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
    ]
    await query.edit_message_text("📚 Пән таңда 👇",
                                  reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSING_SUBJECT

# ========================
# ЗАПУСК БОТА
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_SUBJECT: [
                CallbackQueryHandler(choose_subject,
                    pattern="^(История Казахстана|Математика|Грамота \(Казахский\)|stats|back)$"),
                CallbackQueryHandler(handle_answer, pattern="^ans_"),
                CallbackQueryHandler(back_from_answer, pattern="^back2$"),
            ],
            ANSWERING: [
                CallbackQueryHandler(handle_answer, pattern="^ans_"),
                CallbackQueryHandler(choose_subject,
                    pattern="^(История Казахстана|Математика|Грамота \(Казахский\)|stats|back)$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv)

    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
