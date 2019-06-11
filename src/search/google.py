from google_images_search import GoogleImagesSearch
from src.search.auth import api_token, web_cx_id


def return_searched_img_path(s_topic):
    """
    Returns the first image of a given s_topic in Google Images
    :param s_topic: the topic to search for in Google Images
    :return: the path to the downloaded image
    """
    l_imgs = search_image(s_topic, 1)
    return l_imgs[0].path


def search_image(s_topic, n_images, img_format="png", download_path="resources/in/google"):
    """
    Searches n images for the given topic s_topic
    :param s_topic: the topic to search for in Google Images
    :param n_images: number of images to search (max 50)
    :param img_format: image format to search for
    :param download_path: path where the downloaded images will be stored in local host
    :return: downloads and returns a list of results
    """
    gis = GoogleImagesSearch(api_token, web_cx_id)

    query = {
        'q': s_topic,
        'num': n_images,
        # 'safe': 'medium',
        'fileType': img_format,
        # 'imgType': 'photo',
        # 'imgSize': 'medium',
        # 'searchType': 'image',
        # 'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow'
    }

    gis.search(query, path_to_dir=download_path)
    return gis.results()
