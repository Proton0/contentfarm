import random
import cv2
import numpy as np
import os
from multiprocessing import cpu_count
import logging
import time
from tqdm import tqdm
from moviepy.video.fx import fadein
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import concurrent.futures
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


def process_frame(args):
    try:
        frame, intensity, trollface = args
        i = time.perf_counter()
        logging.debug("Calling apply_effects")
        r = effects.apply_effects((frame, intensity, trollface))
        logging.debug(f"Frame processed in {time.perf_counter() - i:.2f} seconds")
        logging.debug("Effects processed")
        return r
    except Exception as e:
        logging.error(f"Failed to process the frame due to {e}")
        return None



def process_frames(frames, intensity):
    global trollface
    processed_frames = []
    logging.debug("Starting frame processing")

    try:
        if config["use_multiprocessing"]:
            timeout_seconds = config.get("multiprocessing_timeout", 30)
            if config["multiprocessing_count"] == 0:
                config["multiprocessing_count"] = cpu_count()
                logging.debug(
                    f"Using {config['multiprocessing_count']} processes for multiprocessing"
                )
            with concurrent.futures.ProcessPoolExecutor(max_workers=config["multiprocessing_count"]) as executor:
                future_to_frame = {executor.submit(process_frame, (frame, intensity, trollface)): frame for frame in frames}
                start_time = time.time()
                for future in concurrent.futures.as_completed(future_to_frame):
                    if time.time() - start_time >= timeout_seconds:
                        logging.error("Multiprocessing timeout. Try to decrease batch size or increase timeout")
                        executor.shutdown(wait=False)  # Terminate the worker processes immediately
                        return
                    try:
                        result = future.result(timeout=1)
                        processed_frames.append(result) # put result in processed frames
                    except concurrent.futures.TimeoutError:
                        logging.error("Multiprocessing timeout. Try to decrease batch size or increase timeout")
                        executor.shutdown(wait=False)  # Terminate the worker processes immediately
                        return
                    except Exception as e:
                        logging.error(f"Error processing frame: {e}")

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

    except Exception as e:
        logging.error(f"Failed to process frames due to {e}")
        exit(1)

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