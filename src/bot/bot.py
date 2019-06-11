from io import BytesIO
from PIL import Image
import os
import random

import src.gimp.gimp as gimp
import src.search.google as google


import logging

logger = logging.getLogger('Adritify_bot')


def start(bot, update):
    logger.info('He recibido un comando start')
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Soy Adritify, generador de pesadillas. Para empezar, escribe '/tothemoon' o '/onlyfacepls'"
    )


def lucky(bot, update):
    logger.info('He recibido un comando imfeelinglucky')
    s_request = update.message.text.strip()

    if s_request != "/imfeelinglucky":  # it means there is something to search for
        s_img_search = s_request.split(" ", 1)
        s_img_searched = google.return_searched_img_path(s_img_search)

        img_bytes_io = create_montage(s_img_searched)

        if img_bytes_io is None:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="No, you are not lucky. Try again with another word/sentence"
            )
        else:
            bot.send_photo(update.message.chat_id, photo=img_bytes_io)

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="I need some input after the command bro"
        )


def montage(bot, update):
    logger.info('He recibido un comando tothemoon')

    background_img_params = gimp.l_backgrounds[random.randint(0, len(gimp.l_backgrounds) - 1)]

    s_request = update.message.text.strip()
    if "onlyface" in s_request:
        only_face = True
    else:
        only_face = False

    img_bytes_io = create_montage(background_img_params, only_face)
    if img_bytes_io is None:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Something wrong with the image jiji. Try again!"
        )
    else:
        bot.send_photo(update.message.chat_id, photo=img_bytes_io)


def create_montage(background_img, only_face=False):

    img_bytes_io = BytesIO()
    img_bytes_io.name = 'montageohlala.jpeg'

    try:
        im_out = gimp.adritify(background_img, gimp.l_faces, only_face)
    except:  # something wrong with the image jej
        logger.error('Something wrong with image: "{}"'.format(background_img["rel_path"]))
        return None

    im_out.save(img_bytes_io)
    img_bytes_io.seek(0)

    return img_bytes_io

