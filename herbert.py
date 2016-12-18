from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, InlineQueryHandler, InlineQueryResultArticle, InputTextMessageContent)
import logging
from ipwhois import IPWhois
import socket
import string
from pprint import pprint
TOKEN = '308054947:AAGASs5jNePJjE_0SoPlzIx9ucBU40F-KZ8'
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Passami un'indirizzo ip....")


def ip_lookup(bot, update):
	if( is_valid_ipv4_address(update.message.text) ):
		bot.sendMessage(chat_id=update.message.chat_id, text="Sto cercando.....")
		obj = IPWhois(update.message.text)
		res = obj.lookup_whois()
		formatted = res
		info_str = str(formatted)
		final_out = info_str.replace(",", "\n").replace("{", "").replace("}", "")
		
		update.message.reply_text(final_out)
		
	else:
		bot.sendMessage(chat_id=update.message.chat_id, text="L'indirizzo ip non e valido.")	

lookup_handler = MessageHandler(Filters.text, ip_lookup)
dispatcher.add_handler(lookup_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()