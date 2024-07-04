import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEBOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="Anda adalah seorang paranormal yang mampu merasakan keberadaan khodam di sekitar benda atau orang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif, bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertaiment jadi tambahkan #hiburan di akhir untuk memberitahu bahwa informasi dari anda hanya hiburan.\nPastikan output dalam plain text dan berbahasa Indonesia.",
)

# Bot Telegram Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Saya adalah bot yang akan membantu Anda mendeskripsikan khodam yang mungkin ada di sekitar Anda. Silakan kirimkan nama seseorang untuk memulai. Apabila ada pertanyaan silahkan mengunjungi github.com/pandimusr atau mengontak Telegram @okabryan')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Untuk mengetahui detail lebih lanjut tentang bot ini, silahkan bisa mengunjungi github.com/pandimusr atau mengontak @okabryan')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Maaf, terjadi kesalahan: {str(e)}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()