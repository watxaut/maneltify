import json
import logging
import random
import time
from io import BytesIO

import urllib.request
import src.gimp as gimp
import src.config as config

logger = logging.getLogger('Adritify_bot')


def load_json_params(json_path):
    f = open(json_path, "r")
    l_params = json.load(f)
    f.close()
    return l_params


def start(bot, update):
    logger.info('He recibido un comando start')
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Soy Adritify, generador de pesadillas. Para empezar, escribe '/tothemoon' o '/onlyfacepls'"
    )


def create_montage(background_img, only_face=False):

    # load json file for faces and get one image params
    l_faces = load_json_params(config.JSON_FACES_PATH)

    img_bytes_io = BytesIO()
    img_bytes_io.name = "i_{}.jpeg".format(str(time.time()).replace(".", "_"))

    try:
        im_out = gimp.manelitify(background_img, l_faces, only_face, config.JSON_FACES_PATH)
    except:  # something wrong with the image jej
        logger.error('Something wrong with image: "{}"'.format(background_img["rel_path"]))
        return None

    im_out.save(img_bytes_io)
    img_bytes_io.seek(0)

    return img_bytes_io


def input_received(bot, update):
    if update.message.text is not None:
        print("msg", update.message.text)
        update.message.reply_text("OK")
    elif update.message.photo is not None and len(update.message.photo) > 0:
        file_path = update.message.photo[-1].get_file()['file_path']
        local_img_path = "tmp/img.png"
        urllib.request.urlretrieve(file_path, local_img_path)

        logger.info('Processing image')

        img_bytes_io = create_montage(local_img_path, only_face=False)
        if img_bytes_io is None:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Something wrong with the image jiji. Try again!"
            )
        else:
            bot.send_photo(update.message.chat_id, photo=img_bytes_io)

        # delete image
        img_bytes_io.close()
        img_bytes_io = None

    else:
        update.message.reply_text('Me no understando')
