from telegram.ext import *
from PIL import Image
import logging
import time
import RMI_imgs_v3 as imgs
import random


TOKEN = '1218474911:AAEiT0h6irCpll7ByeYkS4Kzlow-NyGOi7U'


def get_photo(update, context):

    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download('photo.jpg')
    if update.message.caption == None or len(update.message.caption) != 5:
        color = random.choice((1, 2, 3, 4, 5, 6, 7, 8, 9))
        cap = [str(color), 3, 1]
    else:
        cap = update.message.caption.split(' ')
    imgs.bot(cap[0], int(cap[1]), int(cap[2]))
    time.sleep(2)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('final.jpg', 'rb'))
    if update.effective_chat.id != 258871997 :
        context.bot.send_photo(chat_id=258871997, photo=open('final.jpg', 'rb'))




def main():
    updater = Updater(token = TOKEN, use_context=True)

    logging.basicConfig(filename = 'C:/Users/ybsh1/Desktop/botlog.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.WARNING)


    updater.dispatcher.add_handler(MessageHandler(Filters.photo or Filters.caption, get_photo))




    updater.start_polling()

if __name__ == '__main__':
    main()
