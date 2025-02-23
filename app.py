from telebot import TeleBot, types, logger
import logging


logger.setLevel(logging.INFO)

GROUP_ID = -4795901629
CHANNEL_ID = -1002204939637
BOT_TOKEN = "7812420366:AAHDKRJ1FfT-dEDnrqRr4bFKiPO0RjOeKf0"

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['generate'])
def generate(message: types.Message):
    if message.from_user.id == 6098825037 or message.from_user.id == 7077167971:
        invite_link = bot.create_chat_invite_link(chat_id=CHANNEL_ID, creates_join_request=True)
        bot.send_message(message.chat.id, invite_link.invite_link)

@bot.chat_join_request_handler()
def send_chat_join_request(request: types.ChatJoinRequest):
    print(request)
    bot.send_message(chat_id=GROUP_ID, text=f"user: {request.from_user.full_name}\nusername: {request.from_user.username}\n{request.invite_link.invite_link}")


bot.infinity_polling()
