import cv2
import numpy as np
import os
import random
import logging
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import multiprocessing
import json

freezeframe = None
# Load configuration from config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(funcName)s] [%(processName)s] %(message)s",
)


# Function to get a random trollface image path from the folder
def get_random_trollface():
    if config["choose_trollface"] != "":
        logging.debug("using custom trollface")
        if os.path.isfile(config["choose_trollface"]):
            return config["choose_trollface"]
        else:
            logging.error("Custom trollface not found. Chosing random trollface from folder")

    trollface_files = os.listdir(config["trollface_folder"])

    if len(trollface_files) == 0:
        logging.error("No trollface images found in the folder")
        exit(1)

    random_trollface = random.choice(trollface_files)
    logging.debug(f"Selected trollface: {random_trollface}")
    return os.path.join(config["trollface_folder"], random_trollface)


trollface = get_random_trollface()


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
            temp = cv2.resize(frame, (50, 50))
            frame = cv2.resize(temp, (frame.shape[1], frame.shape[0]))

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
            size = random.randint(1, 5)
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


# Function to detect faces and overlay the trollface
def overlay_trollface(frame):
    logging.debug("Detecting faces and overlaying trollface")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + config["cascade_path"])
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


# Function to apply vignette effect and overlay trollface and watermark
def apply_effects(args):
    frame, intensity = args
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
    frame_with_trollface = overlay_trollface(frame_with_noise)

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


# Function to process frames in parallel
def process_frames(frames, intensity):
    logging.debug("Starting frame processing")
    if config["use_multiprocessing"]:
        with multiprocessing.Pool() as pool:
            processed_frames = list(
                tqdm(
                    pool.imap(apply_effects, [(frame, intensity) for frame in frames]),
                    total=len(frames),
                    desc="Applying effects",
                )
            )
    else:
        logging.warning(
            "Multiprocessing is disabled. Video processing will be VERY VERY slow"
        )
        processed_frames = [
            apply_effects((frame, intensity))
            for frame in tqdm(frames, desc="Applying effects")
        ]
    logging.debug("Frame processing complete")
    return processed_frames


if __name__ == "__main__":
    # Ask the user
    video_path = input("Enter the video file path: ")
    timestamp = int(
        input(
            "Enter the timestamp (in seconds) where the sigma trollface edit starts: "
        )
    )

    # Load the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logging.debug(f"Video loaded: {video_path}, FPS: {fps}, Frame count: {frame_count}")

    # Calculate the frame number
    timestamp_frame = int(timestamp * fps)
    start_frame = max(0, timestamp_frame - int(config["start_frame"] * fps))
    end_frame = timestamp_frame
    logging.debug(
        f"Timestamp frame: {timestamp_frame}, Start frame: {start_frame}, End frame: {end_frame}"
    )

    # Prepare for writing the video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        "temp_video.mp4", fourcc, fps, (int(cap.get(3)), int(cap.get(4)))
    )

    # Read and write the frames for the last 16 seconds with tqdm progress bar
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for _ in tqdm(
        range(start_frame, end_frame), desc="Processing video frames", unit="frames"
    ):
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to read frame")
            break
        out.write(frame)
    logging.debug("Initial video frames processed")

    # Freeze-frame for 4 seconds with dynamic effects
    freeze_frame_duration = config["freeze_frame_duration"]
    freeze_frame_count = int(freeze_frame_duration * fps)

    # Initialize frames list for freeze frames
    freeze_frames = []

    # Read and process freeze frames in batches for parallel processing
    batch_size = config["batch_size"]
    frames_batch = []

    cap.set(
        cv2.CAP_PROP_POS_FRAMES, end_frame
    )  # Set to the end frame for freeze frames

    for _ in tqdm(range(freeze_frame_count), desc="Generating freeze-frame"):
        if config["freeze_video"] and freezeframe is not None:
            logging.debug("using timestamp frame due to freeze_video in config.json")
            frame = freezeframe
        else:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to read frame")
                break
            freezeframe = frame
        frames_batch.append(frame)

        # Process frames batch
        if len(frames_batch) >= batch_size:
            logging.debug(f"Processing batch of {batch_size} frames")
            freeze_frames.extend(
                process_frames(frames_batch, config["noise_intensity"])
            )
            frames_batch = []

    # Process any remaining frames in the batch
    if frames_batch:
        logging.debug(f"Processing remaining batch of {len(frames_batch)} frames")
        freeze_frames.extend(process_frames(frames_batch, config["noise_intensity"]))

    # Write freeze frames to output video
    for frame in tqdm(freeze_frames, desc="Writing freeze-frame"):
        out.write(frame)
    logging.debug("Freeze frames written to output video")

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.debug("Resources released")

    # Add audio using moviepy
    video_clip = VideoFileClip("temp_video.mp4")
    if config["mute_original_audio"]:
        video_clip = video_clip.without_audio()

    audio_clip = AudioFileClip(config["audio_file"])

    # Check if the audio is shorter than the video and loop/pad if necessary
    if audio_clip.duration < video_clip.duration:
        loops = int(np.ceil(video_clip.duration / audio_clip.duration))
        audio_clip = concatenate_audioclips([audio_clip] * loops).set_duration(
            video_clip.duration
        )

    # Combine video and audio
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(
        config["output_file"],
        codec=config["codec"],
        audio_codec=config["audio_codec"],
        threads=config["threads"]
    )

    os.remove("temp_video.mp4")

    logging.debug("Video generation complete")
    print("Generated")
