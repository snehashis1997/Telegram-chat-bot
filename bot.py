import requests as requests
import random
import json
import telebot
from telebot import types
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep

url = "https://api.telegram.org/bot1169572672:AAGRtTwnzVHkc2PEzDm_nyTgmtO0w5B_0rs/"
token = "1169572672:AAGRtTwnzVHkc2PEzDm_nyTgmtO0w5B_0rs"
filename = r"C:\Users\user\Desktop\logy ai\telegrambot.json"
global update_id

bot = telebot.TeleBot(token)
data = {}

# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url + "sendMessage", data=params)
    return response


# create main function for navigate or reply message back
def main():

    try:
        update_id = last_update(url)["update_id"]
    except IndexError:
        update_id = None

    #update_id = last_update(url)["update_id"]
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while update_id > 1:

        try:
            update = last_update(url)
            if update_id == update["update_id"]:

                if get_message_text(update).lower() == "/start" or get_message_text(update).lower() == "hi" or get_message_text(update).lower() == "hello":
                    bot.send_message(get_chat_id(update), 'Hello Welcome to our bot.')
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update).lower() == "i want to book an appointment":

                    keyboard = types.ReplyKeyboardMarkup(True)
                    keyboard.row('general', 'specialist')
                    bot.send_message(get_chat_id(update), text="would you like to book a", reply_markup=keyboard)
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update).lower() == "specialist":

                    keyboard = types.ReplyKeyboardMarkup(True)
                    keyboard.row('gyno', 'ent', 'ortho')
                    bot.send_message(get_chat_id(update), text="which specialist", reply_markup=keyboard)
                    #bot.send_message(get_chat_id(update), 'which specialist 1.gyno 2.ent 3.ortho')
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update).lower() == "ortho" or get_message_text(update).lower() == "gyno" or get_message_text(update).lower() == "ent" or get_message_text(update).lower() == "general":
                
                    keyboard = types.ReplyKeyboardMarkup(True)
                    keyboard.row('yes', 'no')
                    bot.send_message(get_chat_id(update), text="you are in the 5th in waiting list.are you waiting or not", reply_markup=keyboard)
                    temp = update_id
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update).lower() == "yes" and update_id == temp + 1:
                    bot.send_message(get_chat_id(update), 'okay here is the payment link pls pay, thank you for the payment here is the link online consultation',reply_markup=types.ReplyKeyboardRemove())
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update).lower() == "no" and update_id == temp + 1:
                    #keyboard = types.ReplyKeyboardMarkup(True)
                    keyboard.row('yes', 'no')
                    bot.send_message(get_chat_id(update), text="would you like to see the doctor later?", reply_markup=keyboard)
                    #send_message(get_chat_id(update), 'would you like to see the doctor later?')
                    temp1 = update_id
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update).lower() == "yes" and update_id == temp1 + 1:

                    #keyboard = telebot.types.ReplyKeyboardMarkup(True)
                    keyboard.row('15-08', '19-08',"20-08")
                    bot.send_message(get_chat_id(update), text="thses are the possible date and time of the appoitment please choose one", reply_markup=keyboard)
                    #keyboard = types.ReplyKeyboardRemove(selective=False)
                    data[update_id] = get_message_text(update).lower()

                elif get_message_text(update) == "19-08" or get_message_text(update) == "02-08" or get_message_text(update) == "15-08":
                   
                    bot.send_message(get_chat_id(update), 'okay here is the payment link pls pay, thank you for the payment here is the link online consultation',reply_markup=types.ReplyKeyboardRemove())
                    update_id = 0
                    data[update_id] = get_message_text(update).lower()
            
                else:

                    bot.send_message(get_chat_id(update), 'okay bye..see you again',reply_markup=types.ReplyKeyboardRemove())
                    update_id = 0
                    data[update_id] = get_message_text(update).lower()

                update_id += 1

        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1



# call the function to make it reply
main()
with open(filename, "w") as outfile:  
    json.dump(data, outfile) 
