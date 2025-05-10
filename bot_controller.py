import telebot
import os
from dotenv import load_dotenv
import subprocess
import psutil
import time
import signal
import pyautogui

load_dotenv('.env')
BotToken = os.getenv('bot_token')

bot = telebot.TeleBot(BotToken)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add(telebot.types.KeyboardButton('Shutdown PC'))
    markup.add(telebot.types.KeyboardButton('Show tasklist'))
    markup.add(telebot.types.KeyboardButton('Edit process'))
    markup.add(telebot.types.KeyboardButton('Screenshot on PC'))
    markup.add(telebot.types.KeyboardButton('Open the programm'))
    bot.reply_to(message, "Hello, i'm bot created by <b>Kirwl. W</b>", parse_mode='html')
    bot.send_message(message.chat.id, 'Give me a <b>command</b> and i gonna complete it', parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Shutdown PC', 'Show tasklist', 'Edit process', 'Screenshot on PC', 'Open the programm'])
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
    elif message.text == 'Screenshot on PC':
        bot.send_message(message.chat.id, 'Please type in what screenshot name gonna be')
        bot.register_next_step_handler(message, make_screenshot)
    elif message.text == 'Open the programm':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Notepad', callback_data='notepad'))
        markup.add(telebot.types.InlineKeyboardButton('Chrome', callback_data='chrome'))
        markup.add(telebot.types.InlineKeyboardButton('Explorer', callback_data='explorer'))
        markup.add(telebot.types.InlineKeyboardButton('Telegram', callback_data='telegram'))
        markup.add(telebot.types.InlineKeyboardButton('Type myself', callback_data='user'))
        bot.send_message(message.chat.id, "Pickup your choice from menu, soon can be more", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['notepad', 'chrome', 'explorer', 'telegram', 'user'])
def open_programm(call):
    if call.data == 'notepad':
        bot.send_message(call.message.chat.id, 'Opening notepad.exe')
        os.startfile('notepad.exe')
    elif call.data == 'chrome':
        bot.send_message(call.message.chat.id, 'Opening chrome.exe')
        os.startfile('chrome.exe')
    elif call.data == 'explorer':
        bot.send_message(call.message.chat.id, 'Opening explorer.exe')
        os.startfile('explorer.exe')
    elif call.data == 'telegram':
        bot.send_message(call.message.chat.id, 'Opening Telegram.exe')
        os.startfile('e:/Telegram Desktop/Telegram.exe')
    elif call.data == 'user':
        bot_message = bot.send_message(call.message.chat.id, "Type your programm in that format to open 'D:/Path/Path/programm.exe'")
        bot.register_next_step_handler(bot_message, user_open_programm)

def user_open_programm(message):
    bot.send_message(message.chat.id, f'Opening {message.text}')
    os.startfile(f'{message.text}')

def make_screenshot(message):
    bot.send_message(message.chat.id, 'Making screenshot, please wait...')
    screenshot = pyautogui.screenshot()
    screenshot.save(f'screenshots/{message.text}.png')
    bot.send_message(message.chat.id, 'Sending you a screenshot...')
    with open(f'screenshots/{message.text}.png', 'rb') as image:
        bot.send_photo(message.chat.id, image)

@bot.callback_query_handler(func=lambda call: call.data in ['killpid', 'killname'])
def callback_data(call):
    if call.data == 'killpid':
        bot_message = bot.send_message(call.message.chat.id, 'Enter <b>PID</b> to kill process', parse_mode='html', reply_markup=None)
        bot.register_next_step_handler(bot_message, kill_pid)
    elif call.data == 'killname':
        bot_message = bot.reply_to(call.message, 'Enter <b>Name</b> to kill process', parse_mode='html')
        bot.register_next_step_handler(bot_message, kill_name)

def kill_pid(message):
    try:
        parent_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, '<b>PID must be an integer!</b>\nPlease try again', parse_mode='html')
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

bot.infinity_polling()