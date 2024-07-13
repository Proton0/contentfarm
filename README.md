
# Sigma Trollface Content Farm Maker
A simple python script which makes a super sigma trollface edit that you can use to content farm

## Changelogs (v1.5-> 1.6)
- Fixed bug (code was repeated for some reason)
- Added Configurator UI

**If you are going to use this tool for contentfarming. Dont (its bad)**

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
```json lines
{
  // DEBUG levels
  // 10 - Debug
  // 20 - Info
  // 30 - Warning
  // 40 - Error
  // 50 - Critical
  "debug_level": 10, // see above for details
  "noise_intensity": 0.2, // Noise Intensity
  "mute_original_audio": true, // Will the audio be muted?
  "trollface_left_x": 0.05,
  "trollface_left_y": 0.05,
  "use_trollface": true, // Enable Trollface
  "use_cascade": true, // Enable face detection
  "cascade": "haarcascade_frontalface_default.xml", // Face detection model
  "trollface_folder": "resources/trollfaces", // Trollface folder
  "choose_trollface": "resourcestrollfaces/Trollface_non-free.png", // Choose trollface
  "audio_file": "resources/audios/audio0.wav", // Audio file. Will be ignored if pick_random_audio is true
  "pick_random_audio": true, // Picks a random audio from resources/audio.json
  "random_audio_json": "resources/audio.json", // Audio.json file
  "output_file": "output.mp4", // Output file
  "batch_size": 32, // Batch size for multiprocessing
  "freeze_frame_duration": 4, // How long until the freeze frame ends (will be ignored if pick_random_audio is true)
  "start_frame": 16, // How many seconds until the edit starts (will be ignored if pick_random_audio is true)
  "threads": 8, // How many threads is used for movie.py
  "trollface_size": 0.3, // Trollface size
  "use_multiprocessing": true, // Use multiprocessing for open-cv processing
  "freeze_video": true, // Freeze the video when the edit starts (freeze-frame)
  "face": 0, // What face will be used for trollface
  "use_top_left_for_trollface": true, // Use top left for trollface (will be ignored if put_trollface_in_middle is true and a face is detected)
  "change_trollface_size_for_face": true, // Change the trollface size so its the same as the face
  "watermark_text": "contentfarm V1 - Made By vproton0", // Watermark
  "fontscale": 1, // Watermark font scale
  "thickness": 2, // Watermark thickness
  "put_watermark_in_top_left": false, // Put the watermark in top left?
  "watermark_space": 10, // Watermark space
  "watermark_color": [255,255,255], // Watermark color
  "use_multiple_trollfaces": false, // Use multiple trollfaces
  "glitch_cut_chance": 6, // Chance of the video being cut
  "allow_drawing_lines": true, // Allow drawing lines for glitch
  "allow_glitch_cut": true, // Allow the video being cut
  "draw_line_chance": 4, // Chance of a line being drawn in the video
  "line_color": [0,0,0], // Line color
  "allow_pixelation": true, // Allows pixelation
  "motion_blur_size_max": 5, // Max motion blur size
  "motion_blur_size_min": 1, // Min motion blur size
  "pixelation_chance": 4, // Pixelation chance
  "allow_color_distortion": true, // Allows color distortion
  "color_distortion_chance": 2, // Color distortion chance
  "allow_recursive_glitch": true, // Re-runs the glitch() function
  "recursive_glitch_chance": 4, // Chance of re-running the glitch() function
  "allow_glitch": true, // Allows the glitch
  "glitch_chance": 2, // The chance of the glitch happening
  "put_trollface_in_middle": true, // Put the trollface in the middle (will be ignored if a face is detected)
  "middle_space": -64, // How much will be added in both X and Y coordinates
  "trollface_x": 0, // Trollface X (If this value is anything other then 0 then ANY trollface related values will be ignored)
  "trollface_y": 0, // Trollface Y ((If this value is anything other then 0 then ANY trollface related values will be ignored)
  "audio_codec": "pcm_s32le", // Audio codec (recommended to not change)
  "codec": "libx264", // Video codec (recommended to not change)
  "fadein_duration": 3, // Fade-in duration
  "video": "mr.mp4", // Video (will not ask the user for a video if this is set)
  "timestamp": 509, // same as video but for duration
  "pixelation_intensity": 2 // pixelation intensity
}
```


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