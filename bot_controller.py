import telebot
import os
from dotenv import load_dotenv
import shutil
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
    markup.add(telebot.types.KeyboardButton('Edit files'))
    bot.reply_to(message, "Hello, i'm bot created by <b>Kirwl. W</b>", parse_mode='html')
    bot.send_message(message.chat.id, 'Give me a <b>command</b> and i gonna complete it', parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Shutdown PC', 'Show tasklist', 'Edit process', 'Screenshot on PC', 'Open the programm', 'Edit files'])
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
    elif message.text == 'Edit files':
        bot.send_message(message.chat.id, f'What disk gonna edit? {', '.join(os.listdrives())}')
        bot.register_next_step_handler(message, change_disk)

def change_disk(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(telebot.types.InlineKeyboardButton('Show disks', callback_data='disks'))
    markup.add(telebot.types.InlineKeyboardButton('Show directories on that disk', callback_data='directories'))
    markup.add(telebot.types.InlineKeyboardButton('Change disk', callback_data='cd'))
    markup.add(telebot.types.InlineKeyboardButton('Change directory', callback_data='chdir_1'))
    markup.add(telebot.types.InlineKeyboardButton('Edit directory or file on that path', callback_data='edit_1'))
    global disk
    disk = message.text
    os.system(f'cd {disk}')
    global current_path
    current_path = disk.upper()
    bot.send_message(message.chat.id, f'Changed disk to <b>{current_path}</b>', parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['disks', 'directories', 'cd', 'chdir_1', 'chdir_2', 'chdir_3', 'chdir_4', 'edit_1', 'edit_2', 'edit_3', 'edit_4'])
def switch(call):
    global current_path
    if call.data == 'disks':
        bot.send_message(call.message.chat.id, f'There is all of disks on your PC: {', '.join(os.listdrives())}')
    elif call.data == 'directories':
        try:
            bot.send_message(call.message.chat.id, f'There is all of directories on that disk')
            bot.send_message(call.message.chat.id, f'{'\n'.join(os.listdir(f'{current_path}'))}')
        except PermissionError:
            bot.send_message(call.message.chat.id, "Don't have enough permission to do something with that disk or directory")
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, f'Cannot define path: {current_path}')
    elif call.data == 'cd':
        bot_message = bot.send_message(call.message.chat.id, 'Enter disk to change, you can watch all\ndisks with functions like disks')
        bot.clear_step_handler(bot_message)
        bot.register_next_step_handler(bot_message, change_disk)
    elif call.data == 'chdir_1' or call.data == 'chdir_2' or call.data == 'chdir_3' or call.data == 'chdir_4':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Previous', callback_data='previous'))
        markup.add(telebot.types.InlineKeyboardButton('To the start', callback_data='start'))
        bot_message = bot.send_message(call.message.chat.id, 'Please enter directory, you can watch them\n with a function change directory', reply_markup=markup)
        bot.clear_step_handler(bot_message)
        bot.register_next_step_handler(bot_message, change_directory)
    elif call.data == 'edit_1' or call.data == 'edit_2' or call.data == 'edit_3' or call.data == 'edit_4':
        bot_message = bot.send_message(call.message.chat.id, 'Please enter a name of file or a directory to edit')
        bot.clear_step_handler(bot_message)
        bot.register_next_step_handler(bot_message, edit_file)

def edit_file(message):
    global current_path
    global file
    file = message.text
    if os.path.isdir(f'{current_path}/{file}'):
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Rename', callback_data='rename_folder'))
        markup.add(telebot.types.InlineKeyboardButton('Delete', callback_data='delete_folder'))
        bot.send_message(message.chat.id, f'Path to the folder: {current_path}/{file}\nSum of files: {len([f for f in os.listdir(f'{current_path}/{file}') if os.path.isfile(os.path.join(f'{current_path}/{file}', f))])}\nSum of folders: {len([d for d in os.listdir(f'{current_path}/{file}') if os.path.isdir(os.path.join(f'{current_path}/{file}', d))])}', reply_markup=markup)
    elif os.path.isfile(f'{current_path}/{file}'):
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Rename', callback_data='rename_file'))
        markup.add(telebot.types.InlineKeyboardButton('Delete', callback_data='delete_file'))
        bot.send_message(message.chat.id, f'Path to the file: {current_path}/{file}\nSize of the file: {os.path.getsize(f'{current_path}/{file}')}', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['rename_folder', 'delete_folder', 'rename_file', 'delete_file'])
def file_callback(call):
    global current_path
    global file
    if call.data == 'rename_folder':
        bot_message = bot.send_message(call.message.chat.id, f"Type in new name of a folder '{file}'")
        bot.clear_step_handler(bot_message)
        bot.register_next_step_handler(bot_message, rename_folder)
    elif call.data == 'delete_folder':
        bot.send_message(call.message.chat.id, '<b>Trying to delete a folder...</b>', parse_mode='html')
        shutil.rmtree(f'{current_path}/{file}')
        bot.send_message(call.message.chat.id, f"Successfully deleted a folder '{file}'")
    elif call.data == 'rename_file':
        bot_message = bot.send_message(call.message.chat.id, f"Type in new name of file '{file}'")
        bot.clear_step_handler(bot_message)
        bot.register_next_step_handler(bot_message, rename_file)
    elif call.data == 'delete_file':
        bot.send_message(call.message.chat.id, '<b>Trying to delete a file...</b>', parse_mode='html')
        os.remove(f'{current_path}/{file}')
        bot.send_message(call.message.chat.id, f"Successfully deleted a file '{file}'")

def rename_folder(message):
    global current_path
    global file
    bot.send_message(message.chat.id, 'Renaming your folder...')
    os.rename(f'{current_path}/{file}', f'{current_path}/{message.text}')
    bot.send_message(message.chat.id, f"Successfully renamed folder '{file} to '{message.text}''")

def rename_file(message):
    global current_path
    global file
    bot.send_message(message.chat.id, 'Renaming your file...')
    os.rename(f'{current_path}/{file}', f'{current_path}/{message.text}')
    bot.send_message(message.chat.id, f"Successfully renamed file '{file} to '{message.text}''")

def change_directory(message):
    global current_path
    path = message.text
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(telebot.types.InlineKeyboardButton('Show disks', callback_data='disks'))
    markup.add(telebot.types.InlineKeyboardButton('Show directories on that disk', callback_data='directories'))
    markup.add(telebot.types.InlineKeyboardButton('Change disk', callback_data='cd'))
    markup.add(telebot.types.InlineKeyboardButton('Change directory', callback_data='chdir_3'))
    markup.add(telebot.types.InlineKeyboardButton('Edit directory or file on that path', callback_data='edit_3'))
    new_path = os.path.abspath(os.path.join(current_path, path))
    try:
        os.chdir(new_path)
    except FileNotFoundError:
        pass
    current_path = os.getcwd()
    bot.send_message(message.chat.id, f'Current path: {current_path}', reply_markup=markup)
    return

@bot.callback_query_handler(func=lambda call: call.data in ['previous', 'start'])
def dir_callback(call):
    global current_path
    if call.data == 'previous':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Show disks', callback_data='disks'))
        markup.add(telebot.types.InlineKeyboardButton('Show directories on that disk', callback_data='directories'))
        markup.add(telebot.types.InlineKeyboardButton('Change disk', callback_data='cd'))
        markup.add(telebot.types.InlineKeyboardButton('Change directory', callback_data='chdir_2'))
        markup.add(telebot.types.InlineKeyboardButton('Edit directory or file on that path', callback_data='edit_2'))
        parent_path = os.path.abspath(os.path.join(current_path, '..'))
        current_path = parent_path
        bot.send_message(call.message.chat.id, f'Current path: {current_path}', reply_markup=markup)
        return
    elif call.data == 'start':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton('Show disks', callback_data='disks'))
        markup.add(telebot.types.InlineKeyboardButton('Show directories on that disk', callback_data='directories'))
        markup.add(telebot.types.InlineKeyboardButton('Change disk', callback_data='cd'))
        markup.add(telebot.types.InlineKeyboardButton('Change directory', callback_data='chdir_4'))
        markup.add(telebot.types.InlineKeyboardButton('Edit directory or file on that path', callback_data='edit_4'))
        os.chdir(f'{disk}')
        current_path = os.getcwd()
        bot.send_message(call.message.chat.id, f'Current path: {current_path.upper()}', reply_markup=markup)

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