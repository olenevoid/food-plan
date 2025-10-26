import json
import os

DEMO_DATA = "demodata/demo_db.json"
NEW_DEMO_DATA = "demodata/new_demo_db.json"
IMAGE_BASE_PATH = "demodata/images"


def get_recipies():
    with open(NEW_DEMO_DATA, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def get_users():
    with open(NEW_DEMO_DATA, "r", encoding="utf-8") as file:
        data = json.load(file)

    return []


def get_image_path(image_filename):
    if image_filename.startswith('/'):
        image_filename = image_filename.lstrip('/')
        if image_filename.startswith('demodata/'):
            image_filename = image_filename[9:]
    return os.path.join(IMAGE_BASE_PATH, image_filename)


if __name__ == "__main__":
    pass
    # print(get_recipies())
