# -*- coding: utf-8 -*-
from django_telegrambot.apps import DjangoTelegramBot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler,Handler,CallbackQueryHandler)

import logging
from .models import *

# Enable logging


logger = logging.getLogger(__name__)
from django.db.models import ObjectDoesNotExist

GENDER, PHOTO, LOCATION, BIO = range(4)



def send_notification(bot, update):
    bot.send_message(chat_id='66489748', text="Проба")


def start(bot, update):
    update.message.reply_text(
        'Добрый день, для начала введите свой домен\nПример: example.com')

    return GENDER


def gender(bot, update):
    user = update.message.from_user
    try:
        site = PartnerSite.objects.get(site__url=update.message.text)
        try:
            telegram_user = PartnerSiteTelegram.objects.get(chat_id=update.message.chat_id, partner_site=site)
            update.message.reply_text('Ваш сайт уже есть в базе')
        except ObjectDoesNotExist:
            telegram_user = PartnerSiteTelegram.objects.create(chat_id=update.message.chat_id, partner_site=site)
            telegram_user.save()
            logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
            update.message.reply_text('Отлично %s , сайт %s добавлен' % (user.first_name, site.site.url))
    except ObjectDoesNotExist:
        update.message.reply_text('Извините, ваш сайт не найден')


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s" % (user.first_name, 'user_photo.jpg'))
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f"
                % (user.first_name, user_location.latitude, user_location.longitude))
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location." % user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


from telegram import MessageEntity
def echo(bot, update):
    bot.send_message(chat_id='66489748', text="Проба")

def send():
    dp = DjangoTelegramBot.dispatcher
    dp.bot.send_message(chat_id='66489748', text="Проба")

def main():
    dp = DjangoTelegramBot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [MessageHandler((Filters.entity(MessageEntity.URL) |
                                     Filters.entity(MessageEntity.TEXT_LINK)), gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, send_notification)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
