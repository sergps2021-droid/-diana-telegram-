import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен Telegram от BotFather
TELEGRAM_TOKEN = "СЮДА_ВСТАВЬ_ТВОЙ_TELEGRAM_TOKEN"
# Токен Hugging Face (твой ключ)
HF_TOKEN = "import os
HF_TOKEN = os.environ["HF_TOKEN"]
"

# Endpoint Hugging Face для Llama-3 (можно менять на другие топовые модели)
HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

def get_hf_answer(user_message):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": user_message}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    result = response.json()
    # Модели возвращают ответ в разном формате — ищем 'generated_text'
    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
        return result[0]['generated_text']
    return "Извини, я не смог получить ответ от модели."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Диана на Hugging Face Llama-3 🙂 Задавай вопросы!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        answer = get_hf_answer(user_message)
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Извини, возникла ошибка 😔")
        print(e)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
