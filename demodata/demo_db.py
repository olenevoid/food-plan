import json


DEMO_DATA = 'demodata/demo_db.json'


def get_recipies():
    with open(DEMO_DATA, 'r') as file:
        recipes = json.load(file)

    return recipes


if __name__ == "__main__":
    pass
    #print(get_recipies())
