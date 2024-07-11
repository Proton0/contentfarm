
# Sigma Trollface Content Farm Maker
A simple python script which makes a super sigma trollface edit that you can use to content farm



## Run Locally

Clone the project

```bash
  git clone https://github.com/proton0/sigma-contentfarm
```

Go to the project directory

```bash
  cd sigma-contentfarm
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
  "cascade_path": "haarcascade_frontalface_default.xml",
  "trollface_folder": "trollfaces",
  "audio_file": "audio.wav",
  "output_file": "output.mp4",
  "batch_size": 16,
  "freeze_frame_duration": 4,
  "start_frame": 16,
  "codec": "libx264",
  "threads": 8,
  "trollface_size": 0.2,
  "use_multiprocessing": false,
  "freeze_video": true,
  "face": 0,
  "use_top_left_for_trollface": true,
  "change_trollface_size_for_face": true,
  "watermark_text": "vproton0",
  "fontscale": 1,
  "thickness": 2,
  "put_watermark_in_top_left": false,
  "watermark_space": 10,
  "watermark_color": [255,255,255],
  "use_multiple_trollfaces": false
}
```

`start_frame` is how many seconds it goes before the timestamp / freezeframe
`threads` is movie.py exporting (`use_multiprocessing` is for opencv processing)