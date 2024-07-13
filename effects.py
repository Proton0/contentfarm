import json5 as json
import random
import logging
import cv2
import os
import numpy as np

with open("config.jsonc", "r") as f:
    config = json.load(f)
logging.basicConfig(
    level=config["debug_level"],
    format="%(asctime)s [%(levelname)s] [%(funcName)s] [%(processName)s] %(message)s",
)


# Function to add dynamic noise to an image with changing intensity
def add_dynamic_noise(image, intensity):
    logging.debug("Adding dynamic noise")
    h, w, _ = image.shape
    noise = np.random.normal(scale=intensity, size=(h, w, 3)) * 255
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image


def glitch(frame):
    if (
        random.randint(1, config["glitch_cut_chance"]) == 1
        and config["allow_glitch_cut"]
    ):
        # Pick a random y axis
        y = random.randint(0, frame.shape[0])
        logging.debug(f"Cutting frame by {y}")

        # Replace the lower half with black
        frame[y:, :] = 0
    else:
        # Generate random coordinates within the frame
        start_point = (
            random.randint(0, frame.shape[1]),
            random.randint(0, frame.shape[0]),
        )
        end_point = (
            random.randint(0, frame.shape[1]),
            random.randint(0, frame.shape[0]),
        )

        if (
            random.randint(1, config["draw_line_chance"]) == 1
            and config["allow_drawing_lines"]
        ):
            # Draw a line
            logging.debug("drawing line")
            cv2.line(
                frame,
                start_point,
                (end_point[0], start_point[1]),
                config["line_color"],
                random.randint(1, 5),
            )

        # Bad internet glitch: pixelation and noise
        if (
            random.randint(1, config["pixelation_chance"]) == 1
            and config["allow_pixelation"]
        ):
            # Pixelation
            logging.debug("pixelation glitch")
            temp = cv2.resize(
                frame,
                (
                    int(frame.shape[1] / config["pixelation_intensity"]),
                    int(frame.shape[0] / config["pixelation_intensity"]),
                ),
            )
            frame = cv2.resize(temp, (int(frame.shape[1]), int(frame.shape[0])))

            # Noise
            noise = np.random.normal(0, 1, frame.shape).astype(np.uint8)
            frame = cv2.add(frame, noise)

        # Cheap webcam glitch: color distortion and motion blur
        if (
            random.randint(1, config["color_distortion_chance"]) == 1
            and config["allow_color_distortion"]
        ):
            logging.debug("color distortion")
            # Color distortion
            for channel in range(frame.shape[2]):
                logging.debug("distorting color")
                frame[:, :, channel] = np.roll(
                    frame[:, :, channel], random.randint(-5, 5)
                )

            # Motion blur
            size = random.randint(
                config["motion_blur_size_min"], config["motion_blur_size_max"]
            )
            kernel_motion_blur = np.zeros((size, size))
            kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
            kernel_motion_blur = kernel_motion_blur / size
            frame = cv2.filter2D(frame, -1, kernel_motion_blur)
            logging.debug("created motion blur")

        if (
            random.randint(1, config["recursive_glitch_chance"]) == 1
            and config["allow_recursive_glitch"]
        ):
            glitch(frame)
        return frame

def check_if_opencv_compatible(c):
    try:
        if os.path.isfile("../../_opencv_version"):
            with open("../../_opencv_version", "r") as f:
                opencv_version = f.read()

                if int(opencv_version) >= 10:
                    return False # Too new
                else:
                    with open("../../_opencv_version", "w") as z:
                        z.write(str(int(opencv_version) + 1))
                        z.close()
                        return True  # good version
                    return True # good
        else:
            with open("../../_opencv_version", "w") as f:
                f.write(str(0))
                f.close()
                return True # good version
    except Exception as e:
        return False # Opencv not compatible (too old for the file to be created)
    return False

def overlay_trollface(a):
    frame, trollface = a
    logging.debug("Detecting faces and overlaying trollface")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + config["cascade"])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        logging.debug("No faces detected, placing trollface in middle")
        x, y = int(config["trollface_left_x"] * frame.shape[1]), int(
            config["trollface_left_y"] * frame.shape[0]
        )
    else:
        logging.debug(f"Faces detected: {faces}")
        x, y, w, h = faces[int(config["face"])]
        if config["use_top_left_for_trollface"]:
            logging.debug("using top left face position for trollface")
        else:
            logging.debug("using center position")
            x, y = x + w // 2, y + h // 2

    if config["trollface_x"] != 0 and config["config_y"] != 0:
        logging.debug("using custom trollface x and y")
        x = int(config["trollface_x"])
        y = int(config["trollface_y"])

    trollface_img = cv2.imread(trollface, cv2.IMREAD_UNCHANGED)

    trollface_width = int(
        min(frame.shape[1], frame.shape[0]) * config["trollface_size"]
    )
    trollface_height = int(
        trollface_width * trollface_img.shape[0] / trollface_img.shape[1]
    )

    if config["change_trollface_size_for_face"] and len(faces) != 0:
        logging.debug(
            "trollface size will be changed according to width and height of the face"
        )
        trollface_width = w
        trollface_height = h
    elif config["put_trollface_in_middle"]:
        logging.debug("putting trollface in middle")
        x = int(frame.shape[1] // 2 - trollface_width // 2 + config["middle_space"])
        y = int(frame.shape[0] // 2 - trollface_height // 2 + config["middle_space"])
    else:
        logging.debug("using original trollface width and height")

    trollface_img = cv2.resize(trollface_img, (trollface_width, trollface_height))

    if trollface_img.shape[2] == 4:  # Check if image has alpha channel
        for c in range(3):
            frame[y : y + trollface_height, x : x + trollface_width, c] = trollface_img[
                :, :, c
            ] * (trollface_img[:, :, 3] / 255.0) + frame[
                y : y + trollface_height, x : x + trollface_width, c
            ] * (
                1.0 - trollface_img[:, :, 3] / 255.0
            )
    else:
        for c in range(3):
            frame[y : y + trollface_height, x : x + trollface_width, c] = trollface_img[
                :, :, c
            ]
    # glitch effect
    if random.randint(1, config["glitch_chance"]) == 1 and config["allow_glitch"]:
        frame = glitch(frame)
    return frame


def apply_effects(args):
    frame, intensity, trollface = args
    logging.debug(f"Processing frame with intensity {intensity}")

    # Create a circular vignette mask
    height, width = frame.shape[:2]
    mask = np.zeros((height, width), dtype=np.float32)
    cv2.circle(
        mask, (int(width / 2), int(height / 2)), int(min(width, height) * 0.6), 1, -1
    )
    vignette = cv2.GaussianBlur(mask, (0, 0), int(min(width, height) * 0.3))
    vignette = np.expand_dims(vignette, axis=2)

    frame_vignette = (frame * vignette).astype(np.uint8)
    frame_with_noise = add_dynamic_noise(frame_vignette, intensity)
    frame_with_trollface = overlay_trollface((frame_with_noise, trollface))

    # Add watermark text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = config["watermark_text"]
    text_size = cv2.getTextSize(text, font, config["fontscale"], config["thickness"])[0]
    if config["put_watermark_in_top_left"]:
        logging.info("putting watermark in top left")
        text_x = config["watermark_space"]
        text_y = config["watermark_space"]
    else:
        logging.info("putting watermark in bottom right")
        text_x = frame.shape[1] - text_size[0] - config["watermark_space"]
        text_y = frame.shape[0] - config["watermark_space"]
    cv2.putText(
        frame_with_trollface,
        text,
        (text_x, text_y),
        font,
        config["fontscale"],
        config["watermark_color"],
        config["thickness"],
        cv2.LINE_AA,
    )

    logging.debug("Effects applied to frame")
    return frame_with_trollface
