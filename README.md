
# Sigma Trollface Content Farm Maker
A simple python script which makes a super sigma trollface edit that you can use to content farm

## Changelogs (v1.2 -> v1.3)
- Fixed multiprocessing (finally)
- Added more sounds
- Added more trollfaces
- un-spaghetti code

## Run Locally

Clone the project

```bash
  git clone https://github.com/proton0/contentfarm
```

Go to the project directory

```bash
  cd contentfarm
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the script

```bash
    python3 main.py
```


## Configuration
All of the configuration is in `config.json`

Default configuration
```json
{
  "noise_intensity": 0.2,
  "mute_original_audio": true,
  "trollface_left_x": 0.05,
  "trollface_left_y": 0.05,
  "use_trollface": true,
  "use_cascade": true,
  "cascade": "haarcascade_frontalface_default.xml",
  "trollface_folder": "resources/trollfaces",
  "choose_trollface": "resourcestrollfaces/Trollface_non-free.png",
  "audio_file": "resources/audios/audio0.wav",
  "pick_random_audio": true,
  "random_audio_json": "resources/audio.json",
  "output_file": "output.mp4",
  "batch_size": 32,
  "freeze_frame_duration": 4,
  "start_frame": 16,
  "threads": 8,
  "trollface_size": 0.3,
  "use_multiprocessing": true,
  "freeze_video": true,
  "face": 0,
  "use_top_left_for_trollface": true,
  "change_trollface_size_for_face": true,
  "watermark_text": "contentfarm V1 - Made By vproton0",
  "fontscale": 1,
  "thickness": 2,
  "put_watermark_in_top_left": false,
  "watermark_space": 10,
  "watermark_color": [255,255,255],
  "use_multiple_trollfaces": false,
  "glitch_cut_chance": 6,
  "allow_drawing_lines": true,
  "allow_glitch_cut": true,
  "draw_line_chance": 4,
  "line_color": [0,0,0],
  "allow_pixelation": true,
  "motion_blur_size_max": 5,
  "motion_blur_size_min": 1,
  "pixelation_chance": 4,
  "allow_color_distortion": true,
  "color_distortion_chance": 2,
  "allow_recursive_glitch": true,
  "recursive_glitch_chance": 4,
  "allow_glitch": true,
  "glitch_chance": 2,
  "put_trollface_in_middle": true,
  "middle_space": -64,
  "trollface_x": 0,
  "trollface_y": 0,
  "audio_codec": "pcm_s32le",
  "codec": "libx264",
  "fadein_duration": 3,
  "video": "mr.mp4",
  "timestamp": 509,
  "pixelation_intensity": 2
}
```

`start_frame` is how many seconds it goes before the timestamp / freezeframe

`threads` is movie.py exporting (`use_multiprocessing` is for opencv processing)

When setting `trollface_x` or `trollface_y` to any value. It will ignore any other trollface related configs

## Audio Configuration
Default audio config:
```json
[
  {
    "audio_file": "resources/audios/audio0.wav",
    "start_frame": 16,
    "freeze_frame_duration": 4
  },
  {
    "audio_file": "resources/audios/audio1.wav",
    "start_frame": 10,
    "freeze_frame_duration": 9
  },
  {
    "audio_file": "resources/audios/audio2.wav",
    "start_frame": 8,
    "freeze_frame_duration": 12
  },
  {
    "audio_file": "resources/audios/audio3.wav",
    "start_frame": 10 ,
    "freeze_frame_duration": 5
  },
  {
    "audio_file": "resources/audios/audio4.wav",
    "start_frame": 7,
    "freeze_frame_duration": 10
  }
]
```

`start_frame` is the timestamp where the edit starts

`freeze_frame_duration` is how long the freeze-frame is