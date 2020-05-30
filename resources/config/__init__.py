import json


def get_prefix():
    with open("resources/config/config.json", "r") as config:
        prefix = json.loads(config.read())["prefix"]
    return prefix


def change_prefix(prefix):
    with open("resources/config/config.json", "r+") as config:
        content = json.loads(config.read())
        content["prefix"] = prefix
        config.seek(0)
        config.write(json.dumps(content))


def get_token():
    try:
        with open("resources/config/bot_token", "r") as token_file:
            token = token_file.read().strip()
    except FileNotFoundError:
        print("missing bot_token file in resources/config/")
        exit(1)
    return token


if __name__ == '__main__':
    print(change_prefix("."))
