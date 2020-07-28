from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
from telegram.ext import *
import bot_token
import RMI_imgs as imgs
import logging
import json





GET_PHOTO, REPLACE_PHOTO, GET_COLOR, GET_TEXT, GET_QUOTED = range(5)


def start(update, context):
    update.message.reply_text('אנא שלח תמונה\nבכדי להשתמש בתמונה האחרונה ששלחת שלח /skip',
    reply_markup=ReplyKeyboardRemove())
    return GET_PHOTO


def get_photo(update, context):

    file_name = update.effective_user.id
    context.user_data['file_name'] = file_name

    reply_keyboard = [['ירוק', 'כחול', 'אדום'],
    ['ברונזה', 'כסף', 'זהב'],
    ['עוד סגול', 'סגול', 'טורקיז'],
    ['אקראי']]

    photo_file = update.message.photo[-1].get_file()
    photo_file.download('{}.jpg'.format(file_name))

    if imgs.get_size('{}.jpg'.format(file_name)) < 480:
        update.message.reply_text('התמונה באיכות ממש לא טובה אנא שלח תמונה אחרת!')
        return GET_PHOTO
    elif imgs.get_size('{}.jpg'.format(file_name)) < 960:
        update.message.reply_text(
        'יש לך תמונה באיכות יותר טובה בשבילי?',
        reply_markup=ReplyKeyboardMarkup([['לא', 'כן']], resize_keyboard=True))
        return REPLACE_PHOTO

    update.message.reply_text(
    'מעולה, איזה צבע תרצה?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

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
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return GET_COLOR


def skip_photo(update, context):

    file_name = update.effective_user.id
    context.user_data['file_name'] = file_name

    reply_keyboard = [['ירוק', 'כחול', 'אדום'],
    ['ברונזה', 'כסף', 'זהב'],
    ['עוד סגול', 'סגול', 'טורקיז'],
    ['אקראי']]

    update.message.reply_text(
    'אוקיי, איזה צבע תרצה?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

    return GET_COLOR


def get_color(update, context):

    color = update.message.text
    context.user_data['color'] = color

    update.message.reply_text('אוקיי, שלח לי את הטקסט שברצונך להוסיף', reply_markup=ReplyKeyboardRemove())

    return GET_TEXT


def get_text(update, context):

    text = update.message.text
    context.user_data['text'] = text

    update.message.reply_text('וואלה? מי אמר את זה?')

    return GET_QUOTED


def get_quoted(update, context):

    quoted = update.message.text
    context.user_data['quoted'] = quoted

    context.bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)

    img = imgs.bot(tuple(context.user_data.values()))

    context.bot.send_photo(chat_id=update.effective_user.id, photo=open('{}.jpg'.format(img), 'rb'))
    if update.effective_user.id != 258871997:
        context.bot.send_photo(chat_id=258871997, photo=open('{}.jpg'.format(img), 'rb'), caption='מאת @{}'.format(update.effective_user.username))


    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('בוטל! שלח /start כדי להתחיל שוב.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def no_entry(update, context):
    update.message.reply_text('אתה לא מורשה!')
    return ConversationHandler.END



app = Flask(__name__)
def main():


    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    logger = logging.getLogger(__name__)


    bot = Bot(bot_token.TOKEN)
    dp = Dispatcher(bot, None, workers=0, use_context=True)

    conv_handler = ConversationHandler(
    entry_points=[MessageHandler(~Filters.chat([258871997, 26697264, 313461563]), no_entry), CommandHandler('start', start)],
    states={
    GET_PHOTO: [MessageHandler(Filters.photo, get_photo), CommandHandler('skip', skip_photo)],
    REPLACE_PHOTO: [MessageHandler(Filters.regex('^(כן|לא)$'), replace_photo)],
    GET_COLOR: [MessageHandler(Filters.regex('^(אדום|ירוק|כחול|זהב|כסף|ברונזה|טורקיז|סגול|עוד סגול|אקראי)$'), get_color)],
    GET_TEXT: [MessageHandler(Filters.text & (~Filters.command), get_text)],
    GET_QUOTED: [MessageHandler(Filters.text & (~Filters.command), get_quoted)]},
    fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True)

    dp.add_handler(conv_handler)

    bot.delete_webhook()
    url = bot_token.URL + '/' + bot_token.TOKEN
    bot.set_webhook(url=url)

    @app.route('/' + bot_token.TOKEN, methods=['POST'])
    def webhook():
        json_string = request.stream.read().decode('utf-8')
        update = Update.de_json(json.loads(json_string), bot)
        dp.process_update(update)
        return 'ok', 200




if __name__ == 'main':
    main()

#By t.me/yehuda100
