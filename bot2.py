import telebot
from config2 import TOKEN, OWNER_ID
from telebot import types
from collections import defaultdict

TOKEN = '8086683459:AAHRhwrGE86Xmou2d-mG1eJ1Vdt86h-y2zo'  # Твій токен
OWNER_ID = 5172281327  # Твій Telegram ID

bot = telebot.TeleBot(TOKEN)

users = set()
clicks = defaultdict(int)
tasks_opened = 0

partner_links = {
    "partner1": "https://t.me/partner_channel_1",
    "partner2": "https://t.me/partner_channel_2"
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    users.add(user_id)

    args = message.text.split()
    if len(args) > 1:
        ref = args[1]
        if ref in partner_links:
            clicks[ref] += 1
            bot.send_message(message.chat.id, f"🔗 Перехід до каналу: {partner_links[ref]}")
            return

    bot.send_message(
        message.chat.id,
        f"Привіт, {message.from_user.first_name}!\n\n"
        "Я PromoStarBot. Отримуй «зірки» за прості завдання:\n"
        "- Підписка на канали партнерів\n"
        "- Підписка на @SongFinderProBot\n"
        "- Коментарі в TikTok\n\n"
        "Напиши /tasks, щоб побачити завдання."
    )

@bot.message_handler(commands=['tasks'])
def send_tasks(message):
    global tasks_opened
    tasks_opened += 1

    text = "Ось завдання для отримання зірок:\n\n"
    text += "1. Підпишись на канали:\n"
    for key in partner_links:
        text += f"👉 {partner_links[key]}\n"
    text += (
        "\n2. Підпишись на @SongFinderProBot та пошукай кілька пісень 🎧\n"
        "3. Залиши 10 коментарів у TikTok з текстом:\n"
        "   Кожному по ракеті 🚀 @PromoStarBot\n"
        "4. Надішли скріншот з коментарями сюди, щоб отримати зірку ⭐\n\n"
        "⏳ Коли все буде зроблено, чекайте кілька днів для зарахування зірок.\n"
        "👍 Не забудьте лайкати свої коментарі в TikTok для кращого результату!"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['refer'])
def send_refer(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/PromoStarBot?start={user_id}"
    text = (
        f"Ось твоє персональне реферальне посилання:\n{ref_link}\n\n"
        "Запрошуй друзів і отримуй ще більше зірок ⭐!"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "🚫 Доступ заборонено.")
        return

    text = (
        f"📊 Статистика PromoStarBot:\n"
        f"👥 Унікальні користувачі: {len(users)}\n"
        f"📨 Відкрито завдань: {tasks_opened} разів\n"
        f"🔗 Переходи по каналах:\n"
    )
    for key, count in clicks.items():
        text += f" - {key}: {count} переходів\n"

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['myid'])
def get_my_id(message):
    bot.send_message(message.chat.id, f"Твій Telegram ID: {message.from_user.id}")

@bot.message_handler(content_types=['photo', 'document'])
def handle_screenshot(message):
    bot.reply_to(message,
        f"Дякую, {message.from_user.first_name}! Твій скріншот отримано, твоє завдання враховано. Зірка буде 🎉"
    )

@bot.message_handler(func=lambda m: True)
def default_handler(message):
    text = (
        "Я розумію лише команди /start, /tasks, /refer, /stats\n"
        "Або надішли мені скріншот з виконаним завданням 📸"
    )
    bot.send_message(message.chat.id, text)

print("🤖 Бот працює...")
bot.polling(none_stop=True)
