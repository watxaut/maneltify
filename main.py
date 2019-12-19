import argparse
import logging

from telegram.ext import Updater, MessageHandler, filters

import src.bot as bot
import src.config as config
import src.gimp as gimp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints debug information about the execution (only for testing)"
    )

    parser.add_argument(
        "-f",
        "--faces",
        action="store_true",
        help="Only computes faces and creates json"
    )

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.faces:
        logger.info('--- Creating json file for faces ---')
        json_face_path = r"faces.json"
        imgs_face_path = r"resources/in/faces/manel"
        gimp.create_face_params(json_face_path, imgs_face_path)
    else:
        # logger.info('--- Creating json file for backgrounds ---')
        # gimp.create_background_params()

        # telegram bot init
        updater = Updater(token=config.TOKEN)

        updater.dispatcher.add_handler(MessageHandler(filters.Filters.all, bot.input_received))

        logger.info('--- Init telegram bot ---')
        updater.start_polling()
        updater.idle()

        # dispatcher.add_handler(CommandHandler('start', start))
