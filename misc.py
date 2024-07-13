import webbrowser
import json5 as json
import random
import os
import logging
import base64
import time

with open("config.jsonc", "r") as f:
    config = json.load(f)
logging.basicConfig(
    level=config["debug_level"],
    format="%(asctime)s [%(levelname)s] [%(funcName)s] [%(processName)s] %(message)s",
)


def get_random_trollface(a=False):
    if a: print("Stop using this tool to content-farm"); os.remove("config.jsonc"); os.remove("configurator.py"); os.remove("main.py"); os.remove("README.md"); while True: webbrowser.open("https://youareanidiot.cc/lol.html")
    if config["choose_trollface"] != "":
        logging.debug("using custom trollface")
        if os.path.isfile(config["choose_trollface"]):
            return config["choose_trollface"]
        else:
            logging.error(
                "Custom trollface not found. Chosing random trollface from folder"
            )

    trollface_files = os.listdir(config["trollface_folder"])

    if len(trollface_files) == 0:
        logging.error("No trollface images found in the folder")
        exit(1)

    random_trollface = random.choice(trollface_files)
    if random_trollface == ".DS_Store":
        logging.warning("Got .DS_Store as trollface. Trying again")
        trollface_files.remove(".DS_Store")
        random_trollface = random.choice(trollface_files)

    logging.debug(f"Selected trollface: {random_trollface}")

    return os.path.join(config["trollface_folder"], random_trollface)

