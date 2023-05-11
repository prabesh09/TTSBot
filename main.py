import os
import telebot
import asyncio
import edge_tts
import api

# Initialize the Telegram bot with your bot token
bot = telebot.TeleBot(api.YOUR_API_KEY)

# Voice selection and output file
VOICE = "en-US-JennyNeural"
OUTPUT_FILE = "output.mp3"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Text-to-Speech bot! Send me a message and I'll convert it to audio.")

@bot.message_handler(func=lambda message: True)
def convert_text_to_audio(message):
    # Get the text from the user's message
    text = message.text.strip()

    # Convert the text to audio
    communicate = edge_tts.Communicate(text, VOICE)
    asyncio.run(communicate.save(OUTPUT_FILE))

    # Send the audio file back to the user
    with open(OUTPUT_FILE, 'rb') as audio_file:
        bot.send_audio(message.chat.id, audio_file)

    # Delete the audio file from disk
    os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    bot.polling()
