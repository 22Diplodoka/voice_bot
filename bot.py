import os
import telebot
import speech_recognition
from pydub import AudioSegment
import urllib


token = '5249869623:AAHtYv73qTOnWOYrNg3ZwLcCP8uES9JXwCs'  

bot = telebot.TeleBot(token)

url = "https://drive.google.com/uc?export=view&id=1WDN5RXcYQHiUT4JVujQ2VSwr7p0XLlYX"
filename = "skillbox_sticker.webp"
urllib.request.urlretrieve(url, filename)


def oga2wav(filename):
    # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:     
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    # Скачивание файла, который прислал пользователь
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    name = message.from_user.first_name
    bot.send_message(message.chat.id, 'Ку, ' + name + '!')
    sti = open(filename, 'rb')
    bot.send_sticker(message.chat.id, sti)
    sti.close()



@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)

#@bot.message_handler(content_types=['sticker'])


# Запускаем бота. Он будет работать до тех пор, пока работает ячейка (крутится значок слева).
# Остановим ячейку - остановится бот
bot.polling()
