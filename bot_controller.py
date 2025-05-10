import telebot
import os
from dotenv import load_dotenv
import subprocess
import psutil
import time
import signal

load_dotenv('.env')
BotToken = os.getenv('bot_token')

bot = telebot.TeleBot(BotToken)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add(telebot.types.KeyboardButton('Shutdown PC'))
    markup.add(telebot.types.KeyboardButton('Show tasklist'))
    markup.add(telebot.types.KeyboardButton('Edit process'))
    bot.reply_to(message, "Hello, i'm bot created by <b>Kirwl. W</b>", parse_mode='html')
    bot.send_message(message.chat.id, 'Give me a <b>command</b> and i gonna complete it', parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Shutdown PC', 'Show tasklist', 'Edit process'])
def function_handler(message):
    if message.text == 'Shutdown PC':
        bot.reply_to(message, 'Turning off your pc')
        os.system('shutdown /s /t 1')
    elif message.text == 'Show tasklist':
        for process in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
            time.sleep(0.5)
            bot.send_message(message.chat.id, f'Pid: {process.info.get('pid')}\nName: {process.info.get('name', 'Unknown')}\nUsername: {process.info.get('username')}\nCpu percent: {process.info.get('cpu_percent')}')
    elif message.text == 'Edit process':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Kill process with PID', callback_data='killpid'))
        markup.add(telebot.types.InlineKeyboardButton('Kill process with Name', callback_data='killname'))
        bot.reply_to(message, 'What do you want to do?', parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda choice: True)
def callback_data(call):
    if call.data == 'killpid':
        bot_message = bot.send_message(call.message.chat.id, 'Enter <b>PID</b> to kill process', parse_mode='html', reply_markup=None)
        bot.register_next_step_handler(bot_message, kill_pid)
    elif call.data == 'killname':
        bot_message = bot.reply_to(call.message, 'Enter <b>Name</b> to kill process', parse_mode='html')
        bot.register_next_step_handler(bot_message, kill_name)

def kill_pid(message):
    parent_id = int(message.text)
    for process in psutil.process_iter(['pid', 'name']):
        if parent_id == process.info['pid']:
            bot.send_message(message.chat.id, f'Trying to kill <b>{parent_id} PID</b>', parse_mode='html')
            try:
                os.kill(parent_id, signal.SIGTERM)
            except PermissionError:
                bot.send_message(message.chat.id, 'Not enough permission to stop the process')
                break
            else:
                bot.send_message(message.chat.id, f'Successfuly killed process with <b>{parent_id} PID</b>', parse_mode='html')
                break
    bot.send_message(message.chat.id, 'Cannot define PID please try check tasklist for info')
    
def kill_name(message):
    for process in psutil.process_iter(['pid', 'name']):
        if message.text == process.info['name']:
            parent_id = process.info['pid']
            bot.send_message(message.chat.id, f'Trying to kill <b>{message.text}</b>', parse_mode='html')
            try:
                os.kill(parent_id, signal.SIGTERM)
            except PermissionError:
                bot.send_message(message.chat.id, 'Not enough permission to stop the process')
                break
            else:
                bot.send_message(message.chat.id, f'Successfuly killed process <b>{message.text}</b>', parse_mode='html')
                break
    bot.send_message(message.chat.id, f'Cannot define process {message.text} please try check tasklist for info')

bot.infinity_polling()