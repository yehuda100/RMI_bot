from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
from telegram.ext import *
import bot_token
import RMI_imgs_v4 as imgs
import logging




GET_PHOTO, REPLACE_PHOTO, GET_COLOR, GET_TEXT, GET_QUOTED = range(5)
COLOR, TEXT, QUOTED = '', '', ''


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

    if imgs.get_size('photo.jpg') < 480:
        update.message.reply_text('התמונה באיכות ממש לא טובה אנא שלח תמונה אחרת!')
        return GET_PHOTO
    elif imgs.get_size('photo.jpg') < 960:
        update.message.reply_text(
        'יש לך תמונה באיכות יותר טובה בשבילי?',
        reply_markup=ReplyKeyboardMarkup([['לא', 'כן']], one_time_keyboard=True, resize_keyboard=True))
        return REPLACE_PHOTO

    update.message.reply_text(
    'מעולה, איזה צבע תרצה?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return GET_COLOR


def replace_photo(update, context):
    reply_keyboard = [['ירוק', 'כחול', 'אדום'],
    ['ברונזה', 'כסף', 'זהב'],
    ['עוד סגול', 'סגול', 'טורקיז'],
    ['אקראי']]

    if update.message.text == 'כן':
        update.message.reply_text('יאללה שלח!', reply_markup=ReplyKeyboardRemove())
        return GET_PHOTO
    else:
        update.message.reply_text(
        'סעמק, איזה צבע אתה רוצה?',
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

    global COLOR
    COLOR = update.message.text

    update.message.reply_text('אוקיי, שלח לי את הטקסט שברצונך להוסיף', reply_markup=ReplyKeyboardRemove())

    return GET_TEXT


def get_text(update, context):

    global TEXT
    TEXT = update.message.text

    update.message.reply_text('וואלה? מי אמר את זה?')

    return GET_QUOTED


def get_quoted(update, context):
    global COLOR
    global TEXT
    global QUOTED
    QUOTED = update.message.text

    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)

    img = imgs.bot(COLOR, TEXT, QUOTED)

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('{}.jpg'.format(img), 'rb'))
    if update.effective_chat.id != 258871997:
        context.bot.send_photo(chat_id=258871997, photo=open('{}.jpg'.format(img), 'rb'))


    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('בוטל! שלח /start כדי להתחיל שוב.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def no_entry(update, context):
    update.message.reply_text('אתה לא מורשה!')


def main():


    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    logger = logging.getLogger(__name__)

    updater = Updater(bot_token.TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
    entry_points=[MessageHandler(~Filters.chat([258871997, 26697264]), no_entry), CommandHandler('start', start)],
    states={
    GET_PHOTO: [MessageHandler(Filters.photo, get_photo), CommandHandler('skip', skip_photo)],
    REPLACE_PHOTO: [MessageHandler(Filters.regex('^(כן|לא)$'), replace_photo)],
    GET_COLOR: [MessageHandler(Filters.regex('^(אדום|ירוק|כחול|זהב|כסף|ברונזה|טורקיז|סגול|עוד סגול|אקראי)$'), get_color)],
    GET_TEXT: [MessageHandler(Filters.text & (~Filters.command), get_text)],
    GET_QUOTED: [MessageHandler(Filters.text & (~Filters.command), get_quoted)]},
    fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

#By t.me/yehuda100
