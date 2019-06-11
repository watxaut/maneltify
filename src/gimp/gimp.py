import face_recognition
from PIL import Image
import os
import random

import logging

logger = logging.getLogger('Adritify_bot')


def load_face_params():
    """
    Loads all faces in 'resources/in/faces', calculates their bounding box and puts the bb and the path into a list
    :return: list of dictionaries of {bb, path}
    """

    l_img = []
    l_name_img = os.listdir("resources/in/faces")
    for s_name in l_name_img:

        # get rid of tests and .md files
        if not s_name.startswith("_") and not s_name.endswith(".md"):
            im_face_path = "resources/in/faces/{}".format(s_name)
            im_face = face_recognition.load_image_file(im_face_path)
            l_faces = face_recognition.face_locations(im_face)

            # if a face is detected (should only be one)
            if l_faces:
                t_face = l_faces[0]  # only one face
                l_img.append({"rel_path": im_face_path, "t_face": t_face})
            else:
                logger.info(
                    "Image '{}' has no face :( Try to make the frame a little bigger without resizing the face".format(
                        s_name)
                )
    return l_img


def check_return_png_path(im_path, root_folder='resources/in/backgrounds'):
    """
    Checks the image is in png and if not, converts it to png, saves it in the same folder and returns the new im path.
    If it is, returns the same path
    :param im_path:
    :param root_folder:
    :return:
    """
    if not im_path.endswith(".png"):
        im_name = im_path.replace("\\", "/").split("/")[-1].split(".")[0]

        im_jpg = Image.open(im_path)
        im_path = "{}/{}.png".format(root_folder, im_name)
        try:
            im_jpg.save(im_path)
            return im_path
        except IOError:
            raise
    else:
        return im_path


def adritify(im_path, l_img_faces, only_face):
    """

    :param im_path:
    :param l_img_faces:
    :param only_face:
    :return:
    """

    im_path_new = check_return_png_path(im_path)                    # check background image png format
    im_base = face_recognition.load_image_file(im_path_new)         # load face_recognition PIL background image
    t_face_locations = face_recognition.face_locations(im_base)     # get tuple with face locations

    # reload images again because yes (I was having problems with that method so I opened it again using PIL)
    im_base = Image.open(im_path_new)

    f_factor = 1.1  # multiplies width and creates the width of the new face

    # face with this method gets pasted to high. The greater it is, the lower the face will be pasted
    f_moderate_height = 0.15

    for l_face in t_face_locations:

        # get image props
        upper, right, lower, left = l_face
        width = right - left
        height = lower - upper

        # get a random face from the list of faces
        i = random.randint(0, len(l_img_faces) - 1)
        d_face = l_img_faces[i]

        # load face
        im_face = Image.open(d_face["rel_path"])

        # get face props
        f_upper, f_right, f_lower, f_left = d_face["t_face"]
        face_width = f_right - f_left
        face_height = f_lower - f_upper

        if not only_face:  # if the full face is needed (with hair)

            # calculate the aspect ratio of the face to keep it the same when resizing
            k_aspect_ratio_face = im_face.size[0] / im_face.size[1]

            # calculate how big (or small) is the face compared with the one in the image
            k_factor_width = face_width / width
            face_new_width = int(im_face.size[0] / k_factor_width * f_factor)
            face_new_height = int(face_new_width / k_aspect_ratio_face)

            # calculate the point to paste the image
            p1 = [int(left - (face_new_width / face_width * f_left)),
                  int((upper - (face_new_height / face_height) * f_upper))]
            p1[1] = p1[1] + int(face_new_height * f_moderate_height)
            p1 = tuple(p1)

            # resize the face and paste it into the background image
            im_face_aux = im_face.resize((face_new_width, face_new_height), Image.ANTIALIAS)
            im_base.paste(im_face_aux, p1, im_face_aux)

        else:  # if only the face needs to get pasted it's easier

            # just crop the new face, resize it to match the background face and paste it
            im_face = im_face.crop((f_left, f_upper, f_right, f_lower))

            im_face_aux = im_face.resize((width, height), Image.ANTIALIAS)
            im_base.paste(im_face_aux, (left, upper), im_face_aux)

    return im_base
