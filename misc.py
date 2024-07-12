import json
import random
import os
import cv2
import logging

with open("config.json", "r") as f:
    config = json.load(f)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(funcName)s] [%(processName)s] %(message)s",
)


def get_random_trollface():
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
