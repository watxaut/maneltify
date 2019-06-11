from telegram.ext import Updater, CommandHandler
from src.bot.auth import token
from src.bot.bot import start, montage
import src.gimp.gimp as gimp

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Adritify_bot')


if __name__ == '__main__':

    logger.info('--- Loading faces ---')
    gimp.l_faces = gimp.load_face_params()

    logger.info('--- Loading backgrounds ---')
    gimp.l_backgrounds = gimp.load_background_params()

    # telegram bot init
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # adds the functions to the bot
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('tothemoon', montage))
    # dispatcher.add_handler(CommandHandler('imfeelinglucky', lucky))
    dispatcher.add_handler(CommandHandler('onlyfacepls', montage))

    logger.info('--- Starting bot ---')

    # starts receiving calls
    updater.start_polling()
    updater.idle()
