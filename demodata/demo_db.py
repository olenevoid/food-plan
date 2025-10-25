import json
import os

DEMO_DATA = 'demodata/demo_db.json'
IMAGE_BASE_PATH = "demodata/images"


def get_recipies():
    with open(DEMO_DATA, "r", encoding="utf-8") as file:
        recipes = json.load(file)

    return recipes


def get_image_path(image_filename):
    return os.path.join(IMAGE_BASE_PATH, image_filename)


if __name__ == "__main__":
    pass
    #print(get_recipies())
