from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
import RMI_imgs_v3 as imgs
import logging


TOKEN = '1218474911:AAEiT0h6irCpll7ByeYkS4Kzlow-NyGOi7U'
GET_PHOTO, GET_COLOR, GET_ADD, GET_BANNER = range(4)
COLOR, ADD, BANNER = '', '', ''


def start(update, context):
    update.message.reply_text('אנא שלח תמונה\nבכדי להשתמש בתמונה האחרונה ששלחת שלח /skip')

    return GET_PHOTO


def get_photo(update, context):
    reply_keyboard = [['ירוק', 'כחול', 'אדום'],
    ['ברונזה', 'כסף', 'זהב'],
    ['עוד סגול', 'סגול', 'טורקיז'],
    ['אקראי']]

    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo.jpg')

    update.message.reply_text(
    'מעולה, איזה צבע תרצה?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return GET_COLOR


def skip_photo(update, context):
    reply_keyboard = [['ירוק', 'כחול', 'אדום'],
    ['ברונזה', 'כסף', 'זהב'],
    ['עוד סגול', 'סגול', 'טורקיז'],
    ['אקראי']]

    update.message.reply_text(
    'מעולה, איזה צבע תרצה?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return GET_COLOR


def get_color(update, context):
    reply_keyboard = [['קצת', 'איפשהו באמצע', 'הרבה']]

    global COLOR
    COLOR = update.message.text

    update.message.reply_text(
    'אוקיי, כמה מקום לטקסט תרצה להוסיף?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return GET_ADD


def get_add(update, context):
    reply_keyboard = [['קטן', 'בינוני', 'גדול']]

    global ADD
    ADD = update.message.text

    update.message.reply_text(
    'סבבה, איזה גודל באנר לשים?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return GET_BANNER


def get_banner(update, context):
    global COLOR
    global ADD
    global BANNER
    BANNER = update.message.text

    img = imgs.bot(COLOR, ADD, BANNER)

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('{}.jpg'.format(img), 'rb'), reply_markup=ReplyKeyboardRemove())
    if update.effective_chat.id != 258871997:
        context.bot.send_photo(chat_id=258871997, photo=open('{}.jpg'.format(img), 'rb'))


    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('בוטל! שלח /start כדי להתחיל שוב.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END





def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    logger = logging.getLogger(__name__)

    updater = Updater('1218474911:AAEiT0h6irCpll7ByeYkS4Kzlow-NyGOi7U', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    GET_PHOTO: [MessageHandler(Filters.photo, get_photo), CommandHandler('skip', skip_photo)],
    GET_COLOR: [MessageHandler(Filters.regex('^(אדום|ירוק|כחול|זהב|כסף|ברונזה|טורקיז|סגול|עוד סגול|אקראי)$'), get_color)],
    GET_ADD: [MessageHandler(Filters.regex('^(הרבה|קצת|איפשהו באמצע)$'), get_add)],
    GET_BANNER: [MessageHandler(Filters.regex('^(גדול|בינוני|קטן)$'), get_banner)]},
    fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

#By t.me/yehuda100
