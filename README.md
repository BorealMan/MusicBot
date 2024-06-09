# MusicQT

An open source discord bot implemented in python.

## Features:

- Runs on multiple discord servers.
- Allows you to add songs to queue.
- Add song by URL or search for it on YouTube.

## Requirements:

# Install Requirements With pip

```
pip install -r requirements.txt
```

- Python 3.8 or higher
  - Discord.py
  - Discord.py[voice]
  - yt-dlp

## Additional Info:

A Raspberry Pi 4 runs this great.

Includes a musicbot.service file to easily host on linux.

## Installation Instructions

#### Create Config File

You must create a config.py file with the following values:

```
TOKEN = "ENTER YOUR TOKEN"
SITE_URL = "OPTIONAL -- ENTER YOUR SITE URL -- DEFAULT IS THIS GITHUB"
```

#### Get An API Token

To get an API Token you must have a discord account and go to their [developer site](https://discord.com/developers/applications).

If you have never done it before use a [guide](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/).

Once you have an API Token and you have installed the required python libraries via pip, you will need to create a link with voice and messaging permissions via discord's developer site.

#### Running The Bot

Once you have installed everything and added the config.py with a TOKEN run the main.py file.

## Hosting on linux

If you have never done this you will want to use a [guide](https://linuxhandbook.com/create-systemd-services/).

Make sure that this line points to where you installed this repository:

```
ExecStart=/usr/bin/python3 /home/pi/YOUR_PATH
```
